import api_remote as api

def load_params(model):
    payload = {
        "model": model
    }

    load = api.api_ollama_generate(local_bind_port=app.config['local_port'], payload=user_payload)
    return load