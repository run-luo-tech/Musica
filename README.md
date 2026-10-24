# Musica · 听歌猜曲（Windows）

v0.3.1。新增主界面 Logo、窗口与程序图标，打开程序即可看到。支持点击和拖动播放进度，播放前可预选起播位置。只导入 MP3，文件名“歌手-歌曲名”；主持人从手机答案表按永久编号查询，电脑揭晓前不显示答案。测试不记题，正式活动跨轮去重，退出可恢复。

## 主持人拿到发行包后

从 [GitHub Releases](https://github.com/run-luo-tech/Musica/releases/latest) 下载 **Musica-Setup-0.3.1.exe**，运行后从开始菜单打开。新装和升级使用同一个安装包，无需 Python、pip、开发环境或额外播放器，不需要管理员权限。目标 Windows 10/11 x64，本机 Windows 11 验证。首次启动解包内置环境，可能稍慢。

也可下载 Musica-Windows-x64-v0.3.1.zip，完整解压后双击 Musica.exe，保留便携使用方式。GitHub 的 Source code ZIP 是开发源码，普通用户应选择 Setup 或便携 ZIP。

项目内使用可双击“启动 Musica.cmd”，与现有根目录 data 共用曲库。发行包不包含个人歌曲和数据库。

说明书 PDF、TeX 和独立图片在 docs/manual。常规顺序：导入并核对 → 导出手机 HTML 答案表 → 测试试听 → 正式开始 → 结束本轮/下一轮 → 结束活动。

## 数据与升级

**从 v0.2.0 便携版升级：**先退出旧程序并备份 data。在新版安装器的安装位置页面，选择原 Musica.exe 所在文件夹（里面应有 data），直接覆盖升级。安装包若与旧 EXE、data/library.db 放在同一文件夹，会自动预选它；不会搜索整块磁盘。首次选对后，以后的安装版升级自动沿用已登记位置。

新装默认目录为 `%LOCALAPPDATA%/Programs/Musica`，歌曲、编号、活动记录和个人设置仍在 EXE 旁的 data/config，安装和升级不会写入这些目录；卸载也保留用户生成的数据。升级后可继续恢复未完成活动。若误装到新目录，退出程序后将旧 data/config 整体复制到新 EXE 旁，再打开。exports 是用户导出的个人答案表，不进入公共发行包。

进度条：点击或拖动松开后定位，播放中继续播放，暂停中保持暂停；未开始播放时只预选起点、不记题。方向键调整 5 秒，Home 回开头、End 到末尾附近；重新播放从头开始。MP3 的定位精度取决于编码，不承诺逐采样精确。

Mac 独立项目：[MusicaMac](https://github.com/run-luo-tech/MusicaMac)，不依赖本 Windows 项目。Mac v0.3.1 提供 Apple Silicon / Intel 原生 DMG 和 ZIP，下载见其 [Releases](https://github.com/run-luo-tech/MusicaMac/releases/latest)。退出旧版后替换 Musica.app，保留 Application Support 中的歌曲、活动与配置。

## 维护目录

- src：核心、适配器、流程、界面；run.py 为入口。
- tests：播放定位、计题规则、界面与曲库回归及静音 MP3；不使用私人歌曲。
- scripts：build_windows.ps1 打包，verify.py 选择私有解释器，capture_manual.py 生成隔离截图。
- packaging：发行快速说明；docs：架构、接口、验证和图文说明书。
- releases：当前发行文件；archive/legacy-v0.1：历史 EXE/中间构建，已从启动路径移除。
- .venv：本机维护环境，不发给主持人；.engineering：契约与检查证据。

维护者使用 Python 3.12+ 和 requirements-build.txt，以及 Inno Setup 6（本次 6.7.3）。先运行 scripts/build_manual.ps1 更新 PDF，再运行 scripts/build_windows.ps1；可用 -Iscc 指定编译器，用 -PortableOnly 仅构建便携包。构建生成 EXE、便携 ZIP 和统一 Setup。开发检查：激活 .venv 后 python scripts/verify.py。当前本机 Python 3.14.6。说明书配图脚本额外需要 Pillow；不属于程序运行依赖。
