"""Musica entry point. Data live beside the source or packaged executable."""
import ctypes
import json
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox
from src.adapters.store import Store
from src.apps.desktop import Desktop, APP_VERSION

DEFAULT = {"schema_version": 1, "volume": 0.65, "selection": "random", "version": APP_VERSION}


def load_config(home):
    path = home / "config" / "app.json"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(DEFAULT, indent=2), encoding="utf-8")
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if (value.get("schema_version") != 1 or value.get("selection") != "random"
            or not isinstance(value.get("volume"), (float, int))
            or isinstance(value.get("volume"), bool)
            or not 0 <= value["volume"] <= 1 or not isinstance(value.get("version"), str)):
        raise ValueError("配置格式错误。")
    value["version"] = APP_VERSION
    return value


def application_home():
    home = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    # All launch methods use the project data, including the packaged binary.
    if getattr(sys, "frozen", False) and home.name == "Musica" and home.parent.name == "dist":
        home = home.parent.parent
    elif (getattr(sys, "frozen", False) and home.parent.name == "releases"
          and (home.parent.parent / "run.py").is_file()):
        home = home.parent.parent
    return home


def main():
    home = application_home()
    lock = None
    if sys.platform == "win32":
        import hashlib
        identity = hashlib.sha256(str(home).casefold().encode()).hexdigest()[:24]
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateMutexW.restype = ctypes.c_void_p
        lock = kernel.CreateMutexW(None, False, "Local\\Musica_" + identity)
        if ctypes.get_last_error() == 183:
            temp = tk.Tk()
            temp.withdraw()
            messagebox.showinfo("Musica", "该曲库的 Musica 已经运行，请切换到已有窗口。")
            temp.destroy()
            return
        if not lock:
            raise OSError("无法创建程序实例锁。")
    root = tk.Tk()
    try:
        config = load_config(home)
        Desktop(root, Store(home / "data"), config)
    except Exception:
        root.withdraw()
        messagebox.showerror("Musica 启动失败", "无法打开配置或曲库。请检查程序目录可写、配置格式正确。")
        root.destroy()
        raise
    root.mainloop()


if __name__ == "__main__":
    main()
