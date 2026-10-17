# 验证

自动验收：名称解析/分组；测试不记题；跨轮去重；重播幂等；用尽提示；失败不记；重启恢复；新场重置；HTML 转义与 CSV 编号；真实 MP3 验证、重复导入、去标签/原文件不改；GUI 揭晓/切题/正式管理锁定；打包空库启动。

测试使用隔离临时目录和无音乐内容的短 MP3，不使用私人歌曲或正式 data。播放器使用静音驱动验证；真实扬声器听感和手机浏览器体验待用户拿到歌曲后确认。

project-engineering CLI verify/check/report 保存证据；宿主自动钩子本轮未经证明运行。实际结果交付时追加。

## 2026-10-17 本机执行结果

- Windows 11 x64 / Python 3.14.6；acceptance 17 项全部通过，日志 `.engineering/logs/c1514c6cdad166c1.log`，摘要见 `.engineering/verification.json`。
- 批量导入预览实测：缺失字段补全、相同文件跳过、坏 MP3 报错且保留错误状态；播放错误不把底层路径带入公开界面。
- 原始文件 SHA256 不变，编号副本无 ID3；静音音频夹具包含约 3 秒有效 MP3 帧。夹具由本机 ffmpeg anullsrc + libmp3lame 生成，仅供开发测试，不进入用户曲库。
- 本机默认声音设备以零音量成功开始播放，记录 `.engineering/native-audio.json`。不据此声称真人听感已验证。
- PyInstaller 6.22.3 生成 dist/Musica/Musica.exe；实际进程启动、主窗口标题、窗口句柄与 EXE SHA256 见 `.engineering/package-smoke.json`。本次独立版窗口已启动，使用空曲库，等待用户导入。
- 测试、正式、导入预览截图见 `.engineering/previews`，人工检查无重叠、无截断；正式界面只显示编号和中性文案。未验证其他电脑和其他 DPI 缩放比例。
- 用户实际歌曲的音频质量/中文文件名兼容性及手机浏览器打开答案表的体验待下一轮使用验证。无 C 迁移和 KITS 归档验收要求。

## 文件名提取修复

支持 `歌手-歌曲名.mp3`，继续兼容 `歌手 - 歌曲名.mp3`；按上述分隔符只拆一次，保留歌名其余内容。使用截图中可见的十个文件名和导入预览做回归验证，acceptance 共 19 项通过；增量工程检查无问题。

新可执行文件为 dist/Musica/Musica-0.1.1.exe，原启动器已优先选择它，共用原 data。旧程序正在使用，未强制关闭；主持人关闭旧窗口后重新启动并重新选择文件，才能使用新的解析规则。

## v0.1.2：统一入口和明亮配色

19 项验收测试通过；额外使用 PyInstaller CArchiveReader 从真正交付的 EXE 提取并执行解析代码，18 个文件名案例通过，确认内置 APP_VERSION=0.1.2、奶油白背景，证据 `.engineering/packaged-parser-v012.json`。本次支持常见 Unicode 横线。导入预览使用截图中可见名称检查，全部自动填入歌手、歌曲名并显示待导入，截图 `.engineering/previews/v012-import.png`。

原 Musica.exe 和旧命名 Musica-0.1.1.exe 已覆盖为同一新版二进制；启动器统一启动 Musica.exe。标题显示版本，便于识别。用户曲库未迁移或改写。上节 0.1.1 发布说明为历史记录。

## v0.1.3：答案文字层级

编号从 68pt 改为 24pt；揭晓后歌名为 38pt 加粗，歌手为 23pt；未揭晓的提示保持原大小且不显示答案。19 项验收测试通过，增量检查无问题。截图 `.engineering/previews/v013-reveal.png` 检查了中文歌名与歌手的显示层级、按钮位置。独立版打包为 Musica-0.1.3.exe；当前旧版未强制退出，启动器已优先选择新版本。

## v0.2.0 整理与部署

旧构建移至 archive，个人 data/exports 保留。Windows 与独立 Mac 项目各 21 项回归通过。Mac 的 .command 经 bash -n 检查；通用测试在 Windows 执行，不等同 macOS 原生验证。TeX说明书为8页、4张独立演示截图，XeLaTeX编译，无 overfull 警告，逐页渲染检查。Windows 独立启动证据与最终发行清单在 .engineering/release-v020.json。
