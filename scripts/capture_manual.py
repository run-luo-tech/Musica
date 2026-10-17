"""Generate separate manual screenshots from isolated synthetic data (Windows authoring)."""
import ctypes
import os
from pathlib import Path
import tempfile
import tkinter as tk
from types import SimpleNamespace
from PIL import ImageGrab
from src.adapters.store import Store
from src.adapters.library import Library
from src.apps.desktop import Desktop, ImportDialog


def main():
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    root_dir = Path(__file__).resolve().parents[1]
    folder = root_dir / 'docs/manual/images'
    folder.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        root = tk.Tk()
        store = Store(temp)
        library = Library(store)
        library.import_mp3(root_dir / 'tests/fixtures/silence.mp3', '示例歌手', '夏日序曲')
        app = Desktop(root, store, {'volume': 0, 'schema_version': 1, 'selection': 'random', 'version': '0.2.0'})

        def capture(window, name):
            root.update()
            root.after(200, root.quit)
            root.mainloop()
            hwnd = ctypes.windll.user32.GetAncestor(window.winfo_id(), 2)
            ImageGrab.grab(window=hwnd).save(folder / name)

        app.start()
        app.next()
        app.begin_playback()
        capture(root, '01-question.png')
        app.reveal()
        capture(root, '02-answer.png')
        app.audio.stop()
        app.game.end_round()
        app.render()
        capture(root, '03-round-ended.png')
        app.game.finish()
        app.render()
        dialog = ImportDialog(SimpleNamespace(window=root, app=app), ['示例歌手-夏日序曲.mp3', '示例乐队 - 城市夜航.mp3', '未规范命名.mp3'])
        capture(dialog.window, '04-import.png')
        dialog.close()
        library.export_html(folder / 'example-answer-sheet.html')
        app.audio.close()
        store.close()
        root.destroy()


if __name__ == '__main__':
    main()
