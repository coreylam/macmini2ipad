#!/bin/bash

# check: 单纯检查进程是否存在
check() {
    pid=`pgrep -f "${process_name}"`
    if [ -z "$pid" ]; then
        echo "not running"
    else
        echo "running"
    fi
}

# stop: 停止进程
stop() {
    pid=`pgrep -f "${process_name}"`
    if [ -n "$pid" ]; then
        kill $pid
    fi
}


# start: 启动进程
start() {
    # todo: 需要根据情况自行实现
    # python /data/release/tools/main.py &
    /bin/sh /Users/coreylin/Desktop/topic/sidecar/run_sidecar.sh > /Users/coreylin/Desktop/topic/sidecar/debug.log &
} 

# health_check: 健康检查，但进程不存在时自动拉起
health_check() {
    pid=`pgrep -f "${process_name}"`
    if [ -z "$pid" ]; then
        start
    fi
}

# restart：重启进程
restart() {
    stop
    sleep 3
    start
}

# todo: 进程名字，用于识别进程, 根据要求自行设置
process_name="run_sidecar.sh"
action=$1
case $action in
    start)
        start
        ;;
    stop)
        stop
        ;;
    check)
        check
        ;;
    restart)
        restart
        ;;
    health_check)
        health_check
        ;;
    *)
        echo "Invalid input"
        ;;
esac
