# 架构与交付

apps → pipelines → core/adapters。core 处理歌曲身份、解析、候选选择；adapters 封装 SQLite/MP3/音频/导出；pipelines 管活动与轮次；apps 控制可见内容。状态由 SQLite 持久化，当前候选与揭晓态属于内存。

歌曲永久编号；同歌手同歌名为同一歌曲组，活动内跨轮去重。测试永不写 plays；成功开始播放后立即记录一次，重播幂等。退出保留未结束活动。播放与数据库不是硬件原子事务，突发断电后需核对最后一题。

导入会复制原文件并删除副本 ID3；游戏界面只展示编号，正式状态禁用管理。播放器不注册系统媒体歌名。游戏错误不带答案或原路径。HTML 答案表显式导出，含答案，归主持人私下保管。

交付分离：releases 为不含个人数据的自包含 EXE，archive 仅历史版本，data/exports 属用户内容。run.application_home 在仓库 releases 下复用根 data，离开仓库独立运行时用 EXE 所在目录；对应行为有自动测试。主持人无需开发环境，不捆绑机器上的整个 .venv。

macOS 独立项目位于同级 MusicaMac，格式兼容但不共享相对代码路径，采用用户 Application Support 数据位置与原生打包方案。
