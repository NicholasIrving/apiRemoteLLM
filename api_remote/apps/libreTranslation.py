from flask import Response, jsonify, abort
from ..stream_data_process import generate_stream
from translate_web.main import main as libre_t
import requests
import api_remote as api
from main import app
from translate_web.app import InfoError

def libretranslate_translate():
    try:
        libre_t(port=6001)
        # return Response(generate_stream(response, ssh_tunnel), mimetype='text/event-stream')
    except Exception as e:
        print('libretranslate_translate启动错误')
        raise

def translate(q, source_language, target_language, prompt, model, temperature):
    print("----- 收到来自libreTranslate_translate的请求 -----")
    # print("请求方法：", request.method)
    # print("请求 URL：", request.url)
    # print("请求 Headers：", dict(request.headers))
    # print("请求体：", request.get_data(as_text=True))
    print("----------------------------------")

    if prompt == "" or not "${source_language}" in prompt \
        or not "${target_language}" in prompt \
        or not "${text}" in prompt or model == "" or temperature == "":
        raise InfoError("这里是自定义的错误信息")

    prompt_text = process_prompt(q, source_language, target_language, prompt)

    # 从请求中获取参数（可选）
    user_payload = {
        "model": model,
        'prompt': prompt_text,
        'options': {
            "temperature": float(temperature)
        },
        "stream": False
    }

    alian_model = api.choose_model(user_payload['model'])
    user_payload['model'] = alian_model

    # ssh_tunnel = api.establish_ssh_tunnel_once()
    ssh_tunnel = api.maintain_tunnel()
    load = api.load_params(model)
    response = api.api_ollama_generate(local_bind_port=app.config['local_port'], payload=user_payload)
    return response

def process_prompt(text, source_language, target_language, prompt):
    prompt_text = prompt.replace('${source_language}', source_language) \
                        .replace('${target_language}', target_language) \
                        .replace('${text}', text)
    return prompt_text
