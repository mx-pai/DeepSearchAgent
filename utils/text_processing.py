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

def validate_json_schema(data: dict[str, Any], required_field: list[str]) -> bool:
    return all(field in data for field in required_field)

def truncate_content(content: str, max_length: int = 20000) -> str:
    if len(content) <= max_length:
        return content
    truncated = content[:max_length]
    last_space = truncated.rfind(" ")
    if last_space > max_length * 0.8:
        truncated = truncated[:last_space]
    return truncated + "..."

def format_search_results_for_prompt(search_results: list[dict[str, Any]], max_length: int = 20000) -> str:
    formatted = []
    for item in search_results:
        content = item.get("content", "").strip()
        if content:
            formatted.append(truncate_content(content, max_length))
    return "\n\n".join(formatted)


