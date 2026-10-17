# 配置

app.json：schema_version=1；volume 0..1（默认0.65）；selection=random；应用生效 version 来自代码（当前0.2.0）。正式活动保存生效快照。原项目 data/config 保留；独立EXE在自身目录创建默认配置。

曲库和历史由程序维护，备份前退出后复制整个 data。活动未结束时禁止改曲库。用户答案表在 exports，不打入公共发行包。
