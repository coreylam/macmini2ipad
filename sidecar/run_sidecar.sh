function connect_ipad(){
    # flag=`ioreg -lw0 | grep "IODisplay" | grep -o '"IOHIDUserDevice"=[0-9]*' | awk -F= '{print $2}'`
    # system_profiler SPDisplaysDataType 
    echo "===== connect_ipad ======"
    num=$(grep -o '[0-9]\+' /Users/coreylin/Desktop/topic/sidecar/num)

    # 连续失败超过5次，则不再尝试
    if [[ $num -gt 5 ]]; then
        echo "连续失败超过5次，则不再尝试"
        return 0
    fi

    flag=$(system_profiler SPDisplaysDataType | grep "Sidecar Display" | wc -l)
    # echo $flag
    if [[ $flag -eq 0 ]]; then
        echo "未连接 ipad"
        osascript /Applications/sidecar.app
        sleep 5
    fi
    # 检查连接是否成功
    flag=$(system_profiler SPDisplaysDataType | grep "Sidecar Display" | wc -l)
    if [[ $flag -eq 1 ]]; then
        # 连接成功，失败计数器清零
        echo "连接成功，失败计数器清零"
        echo "0" > /Users/coreylin/Desktop/topic/sidecar/num
    else
        # 连接成功，失败计数器加一
        echo "连接失败，失败计数器加一"
        num=$((num + 1))
        echo "$num" > /Users/coreylin/Desktop/topic/sidecar/num
    fi
    echo "===== end connect_ipad ======"
}

function disconnect_ipad(){
    echo "===== disconnect_ipad ======"
    # flag=`ioreg -lw0 | grep "IODisplay" | grep -o '"IOHIDUserDevice"=[0-9]*' | awk -F= '{print $2}'`
    # system_profiler SPDisplaysDataType
    num=$(grep -o '[0-9]\+' /Users/coreylin/Desktop/topic/sidecar/num)

    # 连续失败超过5次，则不再尝试
    if [[ $num -gt 5 ]]; then
        echo "连续失败超过5次，则不再尝试"
        return 0
    fi

    # 尝试断开 ipad 连接
    flag=$(system_profiler SPDisplaysDataType | grep "Sidecar Display" | wc -l)
    # echo $flag
    if [[ $flag -eq 1 ]]; then
        echo "已连接 ipad"
        osascript /Applications/sidecar.app
        sleep 5
    fi
    # 检查断开是否成功
    flag=$(system_profiler SPDisplaysDataType | grep "Sidecar Display" | wc -l)
    if [[ $flag -eq 1 ]]; then
        # 断开失败，失败计数器+1
        echo "断开失败，失败计数器+1"
        num=$((num + 1))
        echo "$num" > /Users/coreylin/Desktop/topic/sidecar/num
    else
        # 断开成功，失败计数器清零
        echo "断开失败，失败计数器+1"
        echo "0" > /Users/coreylin/Desktop/topic/sidecar/num
    fi
    echo "===== disconnect_ipad ======"
}


while true
do
    exp_flag=`cat /Users/coreylin/Desktop/topic/sidecar/connect_flag`
    echo "exp_flag $exp_flag"
    if [[ $exp_flag -eq 1 ]]; then
        connect_ipad
    else
        disconnect_ipad
    fi
    sleep 5
done
