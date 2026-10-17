# 环境与平台

主持人：Windows 10/11 x64，解压即可运行，自带 Python/Tk/pygame-ce/SDL/mutagen/SQLite，无需另装 Python 或播放器。只在普通可写目录存 data，不要求管理员权限。本机 Windows 11 已启动验证，其他 Windows 电脑需活动前试听。

维护者：当前 .venv 使用 Python 3.14.6；依赖固定于 requirements.txt / requirements-build.txt。scripts/build_windows.ps1 输出发布 EXE；scripts/verify.py 避免 Windows subprocess 错误选到系统 Python，优先使用 VIRTUAL_ENV 或根 .venv。

TeX 文档使用本机 TeX Live 2026 / XeLaTeX。独立截图需 Pillow；PDF 检查用 PyMuPDF/Poppler，不加入游戏运行依赖。原工程 C 迁移/KITS 事项按用户范围不适用。

官方依据：https://pyinstaller.org/en/stable/operating-mode.html；https://www.pygame.org/docs/ref/music.html；https://mutagen.readthedocs.io/en/latest/user/gettingstarted.html 。
