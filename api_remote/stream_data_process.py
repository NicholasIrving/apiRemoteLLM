import json
import re


def remove_think_tags(text, in_think):
    """
    过滤掉文本中位于 <think> ... </think> 标签之间的内容。
    返回过滤后的文本和更新后的 in_think 状态（True 表示当前处于 <think> 区间内）。
    """
    output = ""
    i = 0
    while i < len(text):
        # 如果不在 <think> 区间，且遇到标签起始
        if not in_think and text[i:].startswith("<think>"):
            in_think = True
            i += len("<think>")
        # 如果在 <think> 区间，且遇到标签结束
        elif in_think and text[i:].startswith("</think>"):
            in_think = False
            i += len("</think>")
        elif not in_think:
            output += text[i]
            i += 1
        else:
            # 在 <think> 内的字符直接跳过
            i += 1
    return output, in_think


def generate_stream(upstream_response, server):
    """
    处理上游响应流，过滤掉所有 <think> 标签及其内的内容。
    upstream_response: 从上游（ollama）返回的 requests.Response 对象（流式）。
    server: SSH 隧道对象，生成器结束后需要停止隧道。

    返回一个生成器，生成的每一项符合 text/event-stream 格式的数据行。
    """
    in_think = False  # 用于跟踪是否处于 <think> 标签内
    try:
        for line in upstream_response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8').strip()
                # 遇到结束标识直接返回
                if decoded_line == "data: [DONE]":
                    yield decoded_line + "\n"
                    break
                # 对以 "data: " 开头的行进行处理
                if decoded_line.startswith("data: "):
                    json_str = decoded_line[len("data: "):].strip()
                    try:
                        chunk = json.loads(json_str)
                        # 如果存在 choices 中 delta 的内容，则进行过滤
                        if "choices" in chunk and isinstance(chunk["choices"], list) and len(chunk["choices"]) > 0:
                            delta = chunk["choices"][0].get("delta", {})
                            if "content" in delta:
                                original_content = delta["content"]
                                filtered_content, in_think = remove_think_tags(original_content, in_think)
                                chunk["choices"][0]["delta"]["content"] = filtered_content
                        new_json_str = json.dumps(chunk, ensure_ascii=False)
                        yield "data: " + new_json_str + "\n"
                    except Exception as e:
                        print("JSON解析错误:", e)
                        yield decoded_line + "\n"
                else:
                    yield decoded_line + "\n"
    finally:
        # server.stop()
        pass