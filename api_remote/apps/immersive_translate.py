from flask import Response
from flask import jsonify
from ..stream_data_process import generate_stream


def immersive_translate(response, ssh_tunnel):
    try:
        return Response(generate_stream(response, ssh_tunnel), mimetype='text/event-stream')
    except Exception as e:
        print('immersive_translate返回响应错误')
        raise

