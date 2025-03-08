import re


def remove_think_tags(text):
    """
    移除文本中所有 <think> ... </think> 标签及其内部内容。
    """
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)


def process_response_json(response_json):
    """
    处理 OpenAI API 格式的 JSON 响应，过滤掉每个 choice 的 message.content 中的 <think> 标签内容。

    示例输入格式：
    {
      "choices": [
         {
           "message": {
             "role": "assistant",
             "content": "原始内容，可能包含 <think>推理过程</think>"
           },
           "finish_reason": "stop"
         }
      ]
    }

    返回处理后的 JSON 对象。
    """
    if "choices" in response_json:
        for choice in response_json["choices"]:
            if "message" in choice and "content" in choice["message"]:
                original_content = choice["message"]["content"]
                filtered_content = remove_think_tags(original_content)
                choice["message"]["content"] = filtered_content
    return response_json