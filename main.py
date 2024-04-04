import functools
import pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.platform.page import get_static_index_content
from tornado.web import create_signed_value, decode_signed_value


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
    import os
    os.system("echo '0' > /Users/coreylin/Desktop/topic/sidecar/num")
    os.system("echo '1' > /Users/coreylin/Desktop/topic/sidecar/connect_flag")
    os.system("sh /Users/coreylin/Desktop/topic/sidecar/run.sh health_check")
    return index()


@login_required
def disconnect_ipad():
    """ 断开 ipad

    触发随航断开 ipad
    """
    import os
    os.system("echo '0' > /Users/coreylin/Desktop/topic/sidecar/num")
    os.system("echo '0' > /Users/coreylin/Desktop/topic/sidecar/connect_flag")
    os.system("sh /Users/coreylin/Desktop/topic/sidecar/run.sh health_check")
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

def on_link_click():
    put_text('链接被点击了！')
    import time
    time.sleep(5)
    return index()

@login_required
def index():
    """ 首页
    """
    # applications = {f.__name__: f for f in apps if f.__name__ not in ['index']}
    # content = get_static_index_content(applications)
    put_markdown("# Welcome to visit MacMini server")
    put_markdown("---")
    # put_markdown("- [首页](#)")
    put_markdown("- [连接 ipad](?app=connect_ipad)")
    put_markdown("- [断开 ipad](?app=disconnect_ipad)")
    # put_markdown("- [退出登录](?app=logout)")
    # put_link('点击这里', app='logout')
    # put_html(content)


if __name__ == '__main__':
    apps = [index, connect_ipad, disconnect_ipad, logout]
    pywebio.start_server(apps, port=80)
