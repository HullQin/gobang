# gobang
400行代码，五子棋双人联机对战，允许观战。前端采用原生html js css，UI基于svg，后端python，无数据库，通信基于websocket。

## 体验地址

http://gobang.hullqin.cn/

## 如何部署
1. 安装python库daphne: `pip install daphne`
2. 运行`run.sh`
3. 打开浏览器，访问本机ip地址，即可看到效果。如果和朋友处于同一wifi，他访问你的ip，也可以查看到效果

## 如何联机对战
直接访问地址，是离线模式，单人控制黑棋白棋。如果在地址后加/xx，那么xx就是房间号，处于同一房间号的两人可联机对战。例如两人可同时进入http://gobang.hullqin.cn/123 。第一个进入房间者执黑，第二个进入房间者执白，其他人进入房间则处于观战模式。如果不小心退出，重新进入房间可恢复战局。
