# 两个仓库怎样使用

Windows 项目：https://github.com/run-luo-tech/Musica

Mac 项目：https://github.com/run-luo-tech/MusicaMac

本机目录仍是 E:/AA_PhDocs/HOBBY/Musica 与 E:/AA_PhDocs/HOBBY/MusicaMac；GitHub 仓库地址是云端位置，不需要把本机磁盘路径搬到网页上。两个仓库各自使用 main 主分支、origin 远端。

两个仓库现已按要求改为公开，任何人都可以浏览和克隆已提交的源码与说明书。个人歌曲、数据库和答案表仍只保存在本机，不会因仓库公开而上传。给主持人使用的 EXE/ZIP 可以通过 Releases 分发，也可以直接发送本地发行 ZIP。

## 什么会上传

代码、测试、配置默认值、架构文档、TeX/PDF 使用说明书和演示截图；MP3 只保留开发测试使用的静音夹具。

## 什么留在电脑上

data、exports、.venv、.runtime、archive、build、releases 以及本机验证日志。歌曲、曲库数据库、答案表不会进入提交历史。GitHub 不是歌曲备份；备份仍需退出软件后复制整个 data。

## 以后更新代码

在相应项目目录打开终端，查看并提交自己的改动：

```powershell
git status
git add README.md
git commit -m "Update documentation"
git push
```

git add 后的文件名换成这次实际修改的文件。可以继续让 Codex 帮忙提交。不要使用 force push 覆盖历史。

main 表示默认代码分支；origin 表示自己的 GitHub 仓库。push 是把本地提交上传；pull 是把远端新提交取回。

## 给主持人下载程序

源码放仓库，编译后的文件放 Releases，每次发行建立对应提交的独立标签（本次 v0.3.0），保留历史版本。普通用户下载 Musica-Setup-0.3.0.exe：同一安装包支持新装与升级。v0.2.0 便携用户首次选择原 EXE 目录，后续安装版升级自动沿用原位置。便携 ZIP 继续提供；Source code ZIP 为开发源码。

发布前运行验收测试、构建说明书，再运行 scripts/build_windows.ps1。在未安装 Musica、没有已有 Musica 开始菜单快捷方式的 Windows 测试账户下执行 `python -m scripts.verify_installer`，验证实际安装包的新装、旧便携目录升级、重复安装、数据保留和 EXE 启动；不要把这个隔离验收脚本当作给主持人的升级工具。更新说明记录新增交互、旧版升级步骤与平台验证范围。

Mac .app 还待原生构建。Mac 工作流只有手动触发，不会因为本 Windows 项目的 push 自动运行。

GitHub Releases 官方说明：https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
