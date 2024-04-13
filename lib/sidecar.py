from baselib import system

class SidecarTask(object):
    task_status_path = "/Users/coreylin/Desktop/topic/sidecar/num"
    connect_flag_path = "/Users/coreylin/Desktop/topic/sidecar/connect_flag"

    @classmethod
    def run_sidecar(cls, action="health_check"):
        system.run_cmd(f"sh /Users/coreylin/Desktop/topic/sidecar/run.sh {action}")

    @classmethod
    def read_num(cls, filename):
        with open(filename, "r") as fid:
            data = fid.read()
        return int(data)

    @classmethod
    def write_num(cls, filename, num):
        system.run_cmd(f"echo '{num}' > {filename}")

    @classmethod
    def get_connect_flag(cls):
        connect_flag = cls.read_num(cls.connect_flag_path)
        if connect_flag == 1:
            return "连接 iPad"
        else:
            return "断开 iPad"

    @classmethod
    def set_connect_flag(cls, connect_flag=True):
        cls.write_num(cls.connect_flag_path, int(connect_flag))

    @classmethod
    def enable_task(cls):
        cls.write_num(cls.task_status_path, 0)
        cls.run_sidecar()

    @classmethod
    def disable_task(cls):
        cls.write_num(cls.task_status_path, 9)
        cls.run_sidecar()

    @classmethod
    def get_task_status(cls):
        num = int(cls.read_num(cls.task_status_path))
        if num <= 5:
            return "启用"
        else:
            return "禁用"

    @classmethod
    def connect_ipad(cls):
        cls.set_connect_flag(True)
        cls.enable_task()


    @classmethod
    def disconnect_ipad(cls):
        cls.set_connect_flag(False)
        cls.enable_task()

    @classmethod
    def get_current_status(cls):
        out = system.run_cmd('/usr/sbin/system_profiler SPDisplaysDataType | grep "Sidecar Display" | wc -l')
        if int(out[0].strip()) == 1:
            return "已连接"
        return "未连接"
