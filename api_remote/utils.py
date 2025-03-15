import re

def is_embed(payload):
    return re.search(r"embed", payload['model'], re.IGNORECASE) \
        or re.search(r"embedding", payload['model'], re.IGNORECASE) \
        or 'input' in payload
