"""Exercise the actual Setup in isolated directories, preserving user data.

Refuses to run if a real Musica installation or existing shortcuts are registered.
Run on a Windows build machine after build_windows.ps1.
"""
import ctypes
from contextlib import closing
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import winreg
import zipfile

from src.adapters.library import Library
from src.adapters.store import Store
from src.apps.desktop import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Musica.Windows_is1"
SETUP = ROOT / f"releases/Musica-Setup-{APP_VERSION}.exe"
RESULT = ROOT / f".engineering/installer-v{APP_VERSION}.json"


def registration():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY) as key:
            return {name: winreg.QueryValueEx(key, name)[0]
                    for name in ("InstallLocation", "DisplayVersion")}
    except FileNotFoundError:
        return None


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_setup(folder=None):
    args = [str(SETUP), "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/TASKS="]
    if folder:
        args.append(f"/DIR={folder}")
    result = subprocess.run(args, timeout=90)
    if result.returncode:
        raise RuntimeError(f"Installer returned {result.returncode}")


def uninstall(folder):
    result = subprocess.run([str(folder / "unins000.exe"), "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART"], timeout=60)
    if result.returncode:
        raise RuntimeError(f"Uninstaller returned {result.returncode}")
    deadline = time.monotonic() + 15
    while registration() and time.monotonic() < deadline:
        time.sleep(0.1)
    assert registration() is None, "Uninstall registration remains"


def smoke_window(executable):
    # Only inspect and close the specific test process and its onefile child.
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    enum_proc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    process = subprocess.Popen([str(executable)], cwd=executable.parent)
    found = []
    try:
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            # PyInstaller spawns one child; query only descendants of this PID.
            command = f"Get-CimInstance Win32_Process -Filter 'ParentProcessId={process.pid}' | Select-Object -ExpandProperty ProcessId"
            children = subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True, timeout=15)
            pids = {process.pid} | {int(v) for v in children.stdout.split() if v.isdigit()}

            @enum_proc
            def visit(hwnd, _):
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                if pid.value in pids and user32.IsWindowVisible(hwnd):
                    title = ctypes.create_unicode_buffer(512)
                    user32.GetWindowTextW(hwnd, title, len(title))
                    if f"v{APP_VERSION}" in title.value:
                        found.append((hwnd, title.value))
                return True

            user32.EnumWindows(visit, 0)
            if found:
                break
            if process.poll() is not None:
                raise RuntimeError(f"EXE exited before opening UI: {process.returncode}")
            time.sleep(0.2)
        assert found, "Packaged window did not appear"
        user32.PostMessageW(found[0][0], 0x0010, 0, 0)  # WM_CLOSE, normal cleanup.
        process.wait(timeout=15)
        return found[0][1]
    finally:
        if process.poll() is None:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)


def main():
    assert registration() is None, "A real Musica installation exists; use a clean Windows user for smoke tests"
    shortcut = Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs/Musica.lnk"
    assert not shortcut.exists(), "Existing user shortcut must not be replaced by a test"
    assert SETUP.is_file()
    result = {"version": APP_VERSION, "setup_sha256": digest(SETUP), "checks": []}
    with zipfile.ZipFile(ROOT / f"releases/Musica-Windows-x64-v{APP_VERSION}.zip") as archive:
        names = archive.namelist()
        assert not any(Path(name).parts[0] in {"data", "config", "exports"} for name in names)
        result["public_zip_files"] = names
    with tempfile.TemporaryDirectory(prefix="musica-installer-") as temp:
        work = Path(temp)
        fresh = work / "全新安装"
        portable = work / "旧便携版"
        installed = None
        try:
            run_setup(fresh)
            installed = fresh
            assert registration()["DisplayVersion"] == APP_VERSION
            assert Path(registration()["InstallLocation"]).resolve() == fresh.resolve()
            assert shortcut.is_file()
            assert not (fresh / "data").exists()
            assert not (fresh / "config").exists()
            result["fresh_window"] = smoke_window(fresh / "Musica.exe")
            assert (fresh / "data/library.db").is_file()
            result["checks"].append("fresh install, registration, shortcut and real EXE launch")
            uninstall(fresh)
            installed = None
            assert (fresh / "data/library.db").is_file()
            assert not shortcut.exists()
            result["checks"].append("uninstall keeps user-generated data and removes shortcut")

            portable.mkdir()
            shutil.copy2(ROOT / "releases/Musica-Windows-x64-v0.2.0/Musica.exe", portable / "Musica.exe")
            config = {"schema_version": 1, "volume": 0.23, "selection": "random", "version": "0.2.0"}
            (portable / "config").mkdir()
            (portable / "config/app.json").write_text(json.dumps(config), encoding="utf-8")
            with StoreForTest(portable / "data") as store:
                Library(store).import_mp3(ROOT / "tests/fixtures/silence.mp3", "Synthetic artist", "Upgrade fixture")
                session_id = store.start(config)
                store.record_play(session_id, store.songs()[0])
                original_database = "\n".join(store.db.iterdump())
            (portable / "exports").mkdir()
            (portable / "exports/answer.html").write_text("synthetic answer", encoding="utf-8")
            preserved = {str(path.relative_to(portable)): digest(path)
                         for name in ("data", "config", "exports") for path in (portable / name).rglob("*") if path.is_file()}
            old_digest = digest(portable / "Musica.exe")
            run_setup(portable)
            installed = portable
            assert digest(portable / "Musica.exe") != old_digest
            assert all(digest(portable / name) == value for name, value in preserved.items())
            result["checks"].append("v0.2.0 portable upgrade keeps all data/config/exports bytes")
            result["upgrade_window"] = smoke_window(portable / "Musica.exe")
            with closing(sqlite3.connect(portable / "data/library.db")) as database:
                assert "\n".join(database.iterdump()) == original_database
            # Normal app startup may update SQLite header counters (PRAGMA user_version).
            # Compare the second installer against its immediate input, and compare
            # the database's logical content to the original v0.2.0 data separately.
            before_repeat = {name: digest(portable / name) for name in preserved}
            run_setup()  # No /DIR: must remember the existing registered directory.
            assert Path(registration()["InstallLocation"]).resolve() == portable.resolve()
            assert all(digest(portable / name) == value for name, value in before_repeat.items())
            with StoreForTest(portable / "data") as store:
                assert store.active()["id"] == session_id
                assert len(store.songs()) == 1
                assert len(store.history(session_id)) == 1
            result["checks"].append("repeat install reuses prior directory; library IDs, active session and plays intact")
        finally:
            if installed and (installed / "unins000.exe").exists():
                uninstall(installed)
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


class StoreForTest(Store):
    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


if __name__ == "__main__":
    main()
