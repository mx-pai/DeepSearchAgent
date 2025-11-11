import re, json
from typing import Any
from json import JSONDecodeError

def clean_code_block_tags(text: str, language: str = "json") -> str:
    """移除形如```json...```的代码块标签 """
    text = re.sub(fr"```{language}\s*", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()

def remove_reasoning_from_output(text: str) -> str:
    """移除LLM输出的推理或者解释部分"""
    cleaned = re.sub(r'(?is)(?:reasoning|思考|分析|解释)[:：].*?(?=[{\[])', '', text)
    return cleaned.strip()

def extract_json_from_text(text: str) -> dict[str, Any]:
    text = clean_code_block_tags(remove_reasoning_from_output(text))
    try:
        return json.loads(text)
    except JSONDecodeError:
        pass

    match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if match:
        snippet = match.group()
        try:
            return json.load(snippet)
        except JSONDecodeError:
            return {"error": "JSON解析失败", "raw_text": snippet}
    return {"error": "未找到JSON结构", "raw_text": text}

