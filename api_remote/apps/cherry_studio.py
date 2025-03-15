from flask import Response, stream_with_context, jsonify
from api_remote.process_output import stream_think
import json


def cherry_studio_chat(response):
    try:
        return Response(stream_think(response), mimetype='text/event-stream')
    except Exception as e:
        print('cherry_studio返回响应错误')
        raise

def cherry_studio_embed(response):
    try:
        return json.loads(response.text)
    except Exception as e:
        print('cherry_studio返回响应错误')
        raise

