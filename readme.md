# ipad + mac mini 自动随航

## Feature

sidecar：
- 通过 sidecar 脚本，实现 mac mini 自动随航连接到 ipad（镜像模式）
- 通过 run_sidecar 脚本，实现判断当前是否已经连接到 ipad，实现 连接/断开 可配置，且断开后可以自动重连
- 通过 run 脚本，实现对 run_sidecar 脚本的监控，实现脚本可重入

local_svr:
- 启动web服务，实现在局域网内通过 web 页面上触发连接/断开
- 通过 run 脚本，实现对 main 脚本的监控，实现脚本可重入

crontab : 最后用 crontab，保障 local_svr 是启动的
```shell
* * * * * sh /path/to/local_svr/run.sh 
```

## 效果

- 在 ipad 上就可以触发连接或者断开连接，不需要事先连接到 mac mini
- ipad 断开后，可以自动重连
- mac mini 只需要确保电脑开启，即使电脑在锁屏登录界面，也可以自动连接

## 需要配置

ipad + mac mini + 蓝牙键盘（带触控板）
ipad + mac mini + 妙控键盘 + 蓝牙鼠标

MacOS:
- ventura 13.6 (使用sidecar脚本 sidecar_13_6.applescript)
- sonoma 14.4.1 (使用sidecar脚本 sidecar_14_4.applescript)
## 前提条件

mac mini 开启 + ipad & mac mini 在同一局域网