from flask import jsonify, request
import requests, json
from .ssh_tunnel import stop_tunnel

def api_openai(local_bind_port, payload):
    url = "http://localhost:{}/v1/chat/completions".format(local_bind_port)
    headers = {"Content-Type": "application/json"}
    stream = payload["stream"]

    try:
        response = requests.post(url, json=payload, headers=headers, stream=stream)
        response.raise_for_status()
        return response
    except Exception as e:
        stop_tunnel()
        print('openai接口请求错误：', e)
        raise
        # return jsonify({"error": str(e)}), 500

def api_ollama_generate(local_bind_port, payload):
    url = "http://localhost:{}/api/generate".format(local_bind_port)
    headers = {"Content-Type": "application/json"}
    stream = payload["stream"]

    try:
        response = requests.post(url, json=payload, headers=headers, stream=stream)
        response.raise_for_status()
        return response
    except Exception as e:
        stop_tunnel()
        print('generate接口请求错误：', e)
        raise