from flask import Response
from flask import jsonify
from api_remote.process_output import stream_non_think

def immersive_translate(response):
    try:
        return Response(stream_non_think(response), mimetype='text/event-stream')
    except Exception as e:
        print('immersive_translate返回响应错误')
        raise

