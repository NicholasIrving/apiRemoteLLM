import api_remote as api
from main import app
def load_params(model):
    user_payload = {
        "model": model,
        "stream": False
    }

    load = api.api_ollama_generate(local_bind_port=app.config['local_port'], payload=user_payload)
    return load