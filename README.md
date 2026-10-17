# Musica · 听歌猜曲（Windows）

v0.2.0。只导入 MP3，文件名“歌手-歌曲名”；主持人从手机答案表按永久编号查询，电脑揭晓前不显示答案。测试不记题，正式活动跨轮去重，退出可恢复。

## 主持人拿到发行包后

解压 releases/Musica-Windows-x64-v0.2.0.zip，双击其中 Musica.exe。无需 Python、pip、开发环境或额外播放器；不需要管理员权限。目标 Windows 10/11 x64，本机 Windows 11 验证。首次启动解包内置环境，可能稍慢。

项目内使用可双击“启动 Musica.cmd”，与现有根目录 data 共用曲库。发行包不包含个人歌曲和数据库。

说明书 PDF、TeX 和独立图片在 docs/manual。常规顺序：导入并核对 → 导出手机 HTML 答案表 → 测试试听 → 正式开始 → 结束本轮/下一轮 → 结束活动。

## 数据与升级

本项目 data 保留已有歌曲、编号和活动。独立发行程序在 EXE 旁生成 data/config；备份前退出程序，整体复制 data。升级只替换程序，不用空白数据覆盖原 data。exports 保存已导出的个人答案表，不进入公共发行包。

Mac 独立项目：同级 MusicaMac，不依赖本 Windows 项目。Mac 项目已有首次配置与原生 .app 构建流程；本机不能构建或验证 Mac 应用，尚未交付 Mac 原生二进制。

## 维护目录

- src：核心、适配器、流程、界面；run.py 为入口。
- tests：21 项回归及静音 MP3；不使用私人歌曲。
- scripts：build_windows.ps1 打包，verify.py 选择私有解释器，capture_manual.py 生成隔离截图。
- packaging：发行快速说明；docs：架构、接口、验证和图文说明书。
- releases：当前发行文件；archive/legacy-v0.1：历史 EXE/中间构建，已从启动路径移除。
- .venv：本机维护环境，不发给主持人；.engineering：契约与检查证据。

维护者使用 Python 3.12+ 和 requirements-build.txt，运行 scripts/build_windows.ps1。开发检查：激活 .venv 后 python scripts/verify.py。当前本机 Python 3.14.6。说明书用 XeLaTeX 编译，配图脚本额外需要 Pillow；不属于程序运行依赖。
