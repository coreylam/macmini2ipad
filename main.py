import functools
import os
import pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.platform.page import get_static_index_content
from tornado.web import create_signed_value, decode_signed_value
from lib.sidecar import SidecarTask


class LocalStorage():
    @staticmethod
    def set(key, value):
        run_js("localStorage.setItem(key, value)", key=key, value=value)

    @staticmethod
    def get(key):
        return eval_js("localStorage.getItem(key)", key=key)

    @staticmethod
    def remove(key):
        print(f"remove {key}")
        run_js("localStorage.removeItem(key)", key=key)

# 定义一个装饰，用于检查用户是否已登录


def login_required(func):
    # 使用 functools.wraps，保持函数名称不变
    @functools.wraps(func)
    def warpper(*args, **kwargs):
        token = LocalStorage().get('token')
        print(f"token = {token}")
        username = decode_signed_value(SECRET, 'token', token, max_age_days=7)
        print(f"username = {username}")
        if not token or not username:  # no token or token validation failed
            return login()
        return func(*args, **kwargs)
    return warpper


def check_user(username, password):
    # 检查用户名密码是否正确
    return True


# 加盐
SECRET = "encryption salt value"


def login():
    """Persistence auth

    Use a to signed token mechanism to generate a token store in user's web browser
    """
    # user = input_group('Login', [
    #     input("Username", name='username'),
    #     input("Password", type=PASSWORD, name='password'),
    # ])

    user = {
        "username": "admin",
        "password": "admin"
    }
    username = user['username']
    if check_user(username, user['password']):
        signed = create_signed_value(
            SECRET, 'token', user['username']).decode("utf-8")
        LocalStorage().set('token', signed)
        LocalStorage().set('username', user['username'])
        return index()
    else:
        toast('Wrong password!', color='error')
        return index()


@login_required
def connect_ipad():
    """ 连接ipad

    触发随航连接ipad
    """
    SidecarTask.connect_ipad()
    # os.system("echo '0' > /Users/coreylin/Desktop/topic/sidecar/num")
    # os.system("echo '1' > /Users/coreylin/Desktop/topic/sidecar/connect_flag")
    # os.system("sh /Users/coreylin/Desktop/topic/sidecar/run.sh health_check")
    toast("已触发连接 iPad", color="success")
    return index()


@login_required
def disconnect_ipad():
    """ 断开 ipad

    触发随航断开 ipad
    """
    SidecarTask.disconnect_ipad()
    # os.system("echo '0' > /Users/coreylin/Desktop/topic/sidecar/num")
    # os.system("echo '0' > /Users/coreylin/Desktop/topic/sidecar/connect_flag")
    # os.system("/bin/sh /Users/coreylin/Desktop/topic/sidecar/run.sh health_check")
    toast("已触发断开 iPad", color="success")
    return index()

@login_required
def stop_ipad_task():
    """ 暂停 ipad 连接/断开 任务

    暂停 ipad 连接/断开 任务
    """
    SidecarTask.disable_task()

    # os.system("echo '9' > /Users/coreylin/Desktop/topic/sidecar/num")
    # os.system("/bin/sh /Users/coreylin/Desktop/topic/sidecar/run.sh health_check")
    toast("已停止自动重连", color="success")
    return index()

@login_required
def logout():
    """ 退出

    退出当前登录状态
    """
    LocalStorage().remove('token')
    toast("Logout Success !!", color='success')
    clear()
    return index()

@login_required
def index():
    """ 首页
    """
    clear()
    put_markdown("# Welcome to visit MacMini server")
    put_markdown("---")
    connect_status = SidecarTask.get_connect_flag()
    task_status = SidecarTask.get_task_status()
    cur_status = SidecarTask.get_current_status()
    put_markdown(f"当前连接状态：{cur_status}")
    put_markdown(f"当前任务配置：{connect_status}")
    put_markdown(f"任务开关: {task_status}")

    options = {
        "请选择功能": index,
        "连接 iPad": connect_ipad,
        "断开 iPad": disconnect_ipad,
        "关闭自动随航": stop_ipad_task
    }
    selected_option = select("Mac2ipad 自动随航功能", options=options)
    print(type(selected_option))
    options[selected_option]()
    # return index()
    # put_markdown("- [退出登录](?app=logout)")
    # put_link('点击这里', app='logout')
    # put_html(content)


if __name__ == '__main__':
    apps = [index, connect_ipad, disconnect_ipad, stop_ipad_task, logout]
    pywebio.start_server(apps, port=80)
