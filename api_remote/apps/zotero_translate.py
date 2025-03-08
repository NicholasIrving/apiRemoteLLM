from flask import Response
from flask import jsonify
from api_remote.process_output import stream_non_think

def zotero_translate(response, ssh_tunnel):
    try:
        return Response(stream_non_think(response), mimetype='text/event-stream')
    except Exception as e:
        print('zotero_translate返回响应错误')
        raise

