from sshtunnel import SSHTunnelForwarder
import time
from flask import jsonify
import threading, socket
from main import app

# 模块级全局锁，确保多线程访问时互斥操作
tunnel_lock = threading.Lock()
# 定时器线程的全局变量，确保同一时刻只启动一个定时器
timer_lock = threading.Lock()
global_timer_thread = None

def establish_ssh_tunnel_once():
    server = SSHTunnelForwarder(
        (app.config.get('public_ip'), app.config.get('private_port')),  # 连接到 B 的公网 IP 和指定端口
        ssh_username=app.config.get('user_name'),  # 用 C 的用户名登录
        ssh_pkey='~/.ssh/id_rsa',  # 或者使用 ssh_password='你的密码'
        remote_bind_address=('localhost', app.config.get('remote_port')),  # 在 C 机上访问 11433 端口
        local_bind_address=('localhost', app.config.get('local_port'))  # 在 A 机上绑定本地端口 10001
        )

    try:
        server.start()
        print("SSH 隧道已建立：localhost:{} -> localhost:{}".format(
            app.config.get('local_port'), app.config.get('remote_port')))

        # 等待隧道稳定
        time.sleep(1)
        return server

    except Exception as e:
        server.stop()
        print('建立ssh隧道错误：', e)
        raise
        # return jsonify({"error": str(e)}), 500


def establish_ssh_tunnel():
    """
    如果全局隧道不存在或不再活动，则新建一个；否则返回已存在的隧道。
    同时设置 SSH 底层的 keepalive，保持连接活跃。
    """
    global tunnel_lock
    with tunnel_lock:
        current_tunnel = app.config.get('ssh_tunnel')
        if current_tunnel is None :#and check_tunnel_working(current_tunnel):
            # 新建隧道
            app.config['ssh_tunnel'] = start_tunnel()
            # 记录建立时间，用于监控生命周期
            app.config['tunnel_start_time'] = time.time()

            # 隧道建立后，设置 SSH 底层连接的 keepalive 参数
            try:
                # _transport 是 SSHTunnelForwarder 内部使用的 Paramiko Transport 对象
                app.config['ssh_tunnel']._transport.set_keepalive(30)  # 每 30 秒发送一次 keepalive 包
                print("已设置 SSH keepalive 为 30 秒")
            except Exception as e:
                print("设置 SSH keepalive 失败：", e)

        else:
            print("SSH 隧道仍然存在，无需重新建立，复用隧道")
        return app.config.get('ssh_tunnel')



def start_tunnel():
    return establish_ssh_tunnel_once()

def stop_tunnel():
    with tunnel_lock:
        current_tunnel = app.config.get('ssh_tunnel')
        if current_tunnel:
            current_tunnel.stop()
            app.config['ssh_tunnel'] = None
            print("SSH 隧道已关闭。")

def tunnel_timer(duration):
    # 等待一小时后关闭隧道
    time.sleep(duration)
    print("定时器到期，关闭隧道。")
    stop_tunnel()

def maintain_tunnel(duration=app.config['ssh_keep_alive']):
    """
    建立隧道并启动后台线程定时关闭隧道，保持隧道一段时间（默认1小时）。
    """
    current_tunnel = establish_ssh_tunnel()
    with timer_lock:
        global global_timer_thread
        if global_timer_thread is None or not global_timer_thread.is_alive():
            global_timer_thread = threading.Thread(target=tunnel_timer, args=(duration,), daemon=True)
            global_timer_thread.start()
            print("定时器线程已启动，隧道将在 {} 秒后关闭".format(duration))
        else:
            print("已有定时器线程（隧道）在运行")
    return current_tunnel

def check_tunnel_working(tunnel):
    """
    使用 socket 方式检测隧道是否能建立 TCP 连接。
    尝试连接到 localhost:local_port，如果成功则认为隧道可用。
    """
    local_port = app.config.get('local_port')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)  # 设置超时
    try:
        s.connect(('localhost', local_port))
        s.close()
        print("隧道端口检测成功")
        return True
    except Exception as e:
        print("隧道端口检测失败:", e)
        return False

# def monitor_tunnel_lifetime(duration=3600):
#     """后台线程，每隔一段时间检查隧道是否超时"""
#     while True:
#         time.sleep(10)  # 每10秒检查一次
#         tunnel = app.config.get('ssh_tunnel')
#         start_time = app.config.get('tunnel_start_time')

