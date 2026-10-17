# 两个仓库怎样使用

Windows 项目：https://github.com/run-luo-tech/Musica

Mac 项目：https://github.com/run-luo-tech/MusicaMac

本机目录仍是 E:/AA_PhDocs/HOBBY/Musica 与 E:/AA_PhDocs/HOBBY/MusicaMac；GitHub 仓库地址是云端位置，不需要把本机磁盘路径搬到网页上。两个仓库各自使用 main 主分支、origin 远端。

初次按私有仓库建立。私有仓库仅自己和获授权协作者可见。需要开放源码时可以再改变可见性；私有仓库的下载链接不适合直接发给没有权限的朋友，向朋友发本地发行 ZIP 即可。

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

源码放仓库，编译后的 EXE/ZIP 建议放 Releases，版本号用 v0.2.0 等标签。当前 Windows 便携 ZIP 已在本地 releases，Mac .app 还待原生构建。Mac 工作流只有手动触发，不会因为这次 push 自动运行。

GitHub Releases 官方说明：https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
