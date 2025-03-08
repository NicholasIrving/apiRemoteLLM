from sshtunnel import SSHTunnelForwarder
import time
import threading
from flask import Flask, request, jsonify

global_tunnel = None
def start_tunnel():
    global global_tunnel
    if global_tunnel is None:
        global_tunnel = SSHTunnelForwarder(
            ('115.126.76.162', 45629),
            ssh_username='nick',
            ssh_pkey='~/.ssh/id_rsa',  # 或使用 ssh_password='你的密码'
            remote_bind_address=('localhost', 11434),
            local_bind_address=('0.0.0.0', 10001)
        )
        global_tunnel.start()
        # 设置 keepalive，每30秒发送一次保持包
        # transport = global_tunnel.ssh_transport
        # transport.set_keepalive(30)
        print("隧道已建立，并设置了 keepalive。")

def stop_tunnel():
    global global_tunnel
    if global_tunnel:
        global_tunnel.stop()
        global_tunnel = None
        print("隧道已关闭。")

def tunnel_timer(duration):
    # 等待一小时后关闭隧道
    time.sleep(duration)
    stop_tunnel()

def maintain_tunnel(duration=3600):
    """
    建立隧道并启动后台线程定时关闭隧道，保持隧道一段时间（默认1小时）。
    """
    start_tunnel()
    # 启动后台线程，在duration秒后关闭隧道
    timer_thread = threading.Thread(target=tunnel_timer, args=(duration,), daemon=True)
    timer_thread.start()