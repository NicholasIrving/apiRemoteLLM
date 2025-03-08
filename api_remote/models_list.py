
def choose_model(key):
    model = {
        'ds:32b_q4': 'deepseek-r1:32b',
        'ds:32b': 'deepseek-r1:32b',
        'ds:70b_q4': 'deepseek-r1:70b',
        'ds:70b': 'deepseek-r1:70b',
        'ds:70b_q8': 'deepseek-r1:70b-llama-distill-q8_0',

        'deepseek-r1:32b_q4': 'deepseek-r1:32b',
        'deepseek-r1:32b': 'deepseek-r1:32b',
        'deepseek-r1:70b_q4': 'deepseek-r1:70b',
        'deepseek-r1:70b': 'deepseek-r1:70b',
        'deepseek-r1:70b_q8': 'deepseek-r1:70b-llama-distill-q8_0',

        'qwen:7b': 'qwen2.5:7b',
        'qwen:7b_q4': 'qwen2.5:7b',
        'qwen:14b': 'qwen2.5:7b',
        'qwen:14b_q4': 'qwen2.5:7b',

        'qwen2.5:7b': 'qwen2.5:7b',
        'qwen2.5:7b_q4': 'qwen2.5:7b',
        'qwen2.5:14b': 'qwen2.5:14b',
        'qwen2.5:14b_q4': 'qwen2.5:14b',

        'qwen:32b_q4': 'qwen2.5:32b',
        'qwen:32b': 'qwen2.5:32b',
        'qwen:70b_q4': 'qwen2.5:72b',
        'qwen:72b_q4': 'qwen2.5:72b',
        'qwen:70b': 'qwen2.5:72b',
        'qwen:72b': 'qwen2.5:72b',
        'qwen:70b_q6': 'qwen2.5:72b-instruct-q6_K',
        'qwen:72b_q6': 'qwen2.5:72b-instruct-q6_K',

        'qwen2.5:32b_q4': 'qwen2.5:32b',
        'qwen2.5:32b': 'qwen2.5:32b',
        'qwen2.5:70b_q4': 'qwen2.5:72b',
        'qwen2.5:72b_q4': 'qwen2.5:72b',
        'qwen2.5:70b': 'qwen2.5:72b',
        'qwen2.5:72b': 'qwen2.5:72b',
        'qwen2.5:70b_q6': 'qwen2.5:72b-instruct-q6_K',
        'qwen2.5:72b_q6': 'qwen2.5:72b-instruct-q6_K'
    }
    if key in model:
        return model[key]
    else:
        return key

