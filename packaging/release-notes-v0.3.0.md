新增可调整的播放进度，并提供支持新装与升级的统一 Windows 安装包。

## 下载哪个文件

- **Musica-Setup-0.3.0.exe**：推荐。首次安装和旧版升级使用同一个文件，无需 Python 或管理员权限。
- **Musica-Windows-x64-v0.3.0.zip**：便携版，完整解压后运行 Musica.exe。
- GitHub 自动提供的 Source code 是开发源码，普通用户请选择上面的程序包。

## 从 v0.2.0 升级

1. 退出旧版 Musica，备份原文件夹中的 data。
2. 运行新版 Setup，在安装位置页面选择**原 Musica.exe 所在文件夹**（其中应有 data），直接覆盖升级。
3. 从开始菜单打开 v0.3.0，原歌曲、永久编号、活动记录和配置保留，可恢复未完成活动。

安装包若与原 Musica.exe、data/library.db 位于同一文件夹，会自动预选该目录；其他位置需要手动选择一次。后续安装版升级自动沿用已登记的位置。新用户可直接使用默认安装位置。卸载保留用户生成的数据。

## 新功能

- 点击或拖动进度条，松开后跳到目标位置；播放中继续，暂停中保持暂停。
- 播放前可预选起点，实际开始播放才记题；反复定位不会重复计题，也不会揭晓答案。
- 方向键调整 5 秒；Home 回开头，End 到末尾附近。
- “重新播放”从开头开始；切换题目清除旧起点。

## 验证与平台

28 项回归通过。实际安装包验证了全新安装、v0.2.0 便携目录升级、重复安装、数据/配置保留、开始菜单入口、卸载保留数据，以及新版 EXE 启动。说明书已同步更新。

目标为 Windows 10/11 x64，实际验证环境为 Windows 11。MP3 定位精度随编码而异；活动前请在目标电脑试听。本次更新针对 Windows，Mac 项目独立维护。发行包不含私人歌曲、数据库或答案表。

---

**English:** Adds click/drag seeking, preserves playback or pause state, and allows choosing a start position before playback. A single Windows Setup supports fresh installs and upgrades. v0.2.0 portable users should close the app, back up `data`, and select the existing `Musica.exe` folder during installation. Later installed-version upgrades reuse the registered location. Libraries, permanent IDs, game history and settings are retained; uninstalling keeps user data. A portable ZIP remains available. Tested on Windows 11 x64; 28 regression tests and actual install/upgrade smoke checks passed.
