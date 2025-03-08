from flask import Flask, request, jsonify, Response
import config, sys, subprocess, os
import api_remote as api
from translate_web.main import main as libre_t
from threading import Thread
import rumps
from waitress import serve


class LLMAPI(rumps.App):
    def __init__(self):
        super(LLMAPI, self).__init__("App", icon="icon.png")

app = Flask(__name__)
app.config['public_ip'] = config.PUBLIC_IP
app.config['private_port'] = config.PRIVATE_PORT
app.config['user_name'] = config.USER_NAME
app.config['remote_port'] = config.REMOTE_PORT
app.config['host'] = config.HOST
app.config['local_port'] = config.LOCAL_PORT
app.config['ssh_keep_alive'] = config.SSH_KEEP_ALIVE
# 用于存储 SSH 隧道和建立时间
app.config['ssh_tunnel'] = None
app.config['tunnel_start_time'] = None



@app.route('/zotero_translate', methods=['POST'])
def zotero_translate():
    # 打印来自 X 程序的所有请求信息
    # print("----- 收到来自zotero translate的请求 -----")
    # print("请求方法：", request.method)
    # print("请求 URL：", request.url)
    # print("请求 Headers：", dict(request.headers))
    # print("请求体：", request.get_data(as_text=True))
    # print("----------------------------------")


    # 从请求中获取参数（可选）
    user_payload = request.get_json() or {}

    model = api.choose_model(user_payload['model'])
    user_payload['model'] = model

    ssh_tunnel = api.maintain_tunnel()
    response = api.api_openai(local_bind_port= app.config['local_port'], payload=user_payload)
    result = api.zotero_translate(response, ssh_tunnel)
    return result

@app.route('/immersive_translate', methods=['POST'])
def immersive_translate():
    user_payload = request.get_json() or {}
    model = api.choose_model(user_payload['model'])
    user_payload['model'] = model

    ssh_tunnel = api.maintain_tunnel()
    response = api.api_openai(local_bind_port=app.config['local_port'], payload=user_payload)
    result = api.immersive_translate(response, ssh_tunnel)
    return result

def libretranslate_translate():
    libre_t(**{
                'port': config.LIBRE_TRANSLATION_PORT,
                'disable-files-translation': True
              }
    )

@app.route('/cherry_studio', methods=['POST'])
def cherry_studio():
    user_payload = request.get_json() or {}
    model = api.choose_model(user_payload['model'])
    user_payload['model'] = model

    ssh_tunnel = api.maintain_tunnel()
    response = api.api_openai(local_bind_port=app.config['local_port'], payload=user_payload)
    result = api.cherry_studio_chat(response)
    return result


def main():

    t = Thread(target=libretranslate_translate, daemon=True)
    t.start()

    # 将 web 服务器放入后台线程运行
    server_thread = Thread(target=lambda: serve(app, host='127.0.0.1', port=config.MAIN_PORT), daemon=True)
    server_thread.start()
    print("Start")
    LLMAPI().run()

if __name__ == '__main__':
    # 如果环境变量 "DETACHED" 没有设为 "1"，说明当前是父进程
    # if os.environ.get("DETACHED") != "1":
    #     # 设置环境变量，让子进程知道已经脱离终端了
    #     env = os.environ.copy()
    #     env["DETACHED"] = "1"
    #     # 不改变 sys.argv，这样服务器可以正常解析通过 -- 传入的参数
    #     subprocess.Popen([sys.executable] + sys.argv,
    #                      env=env,
    #                      start_new_session=True,
    #                      stdout=subprocess.DEVNULL,
    #                      stderr=subprocess.DEVNULL)
    #     # 父进程退出，Terminal 会关闭
    #     sys.exit(0)
    main()

