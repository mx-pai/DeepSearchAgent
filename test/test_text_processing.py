import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils.text_processing import (
    clean_code_block_tags,
    remove_reasoning_from_output,
    extract_json_from_text,
    truncate_content,
    format_search_results_for_prompt,
    validate_json_schema
)


def test_clean_code_block_tags():
    text = """```json
    {"key": "value"}
    ```"""
    cleaned = clean_code_block_tags(text, "json")
    assert "```" not in cleaned
    assert cleaned.strip().startswith("{")
    assert cleaned.strip().endswith("}")


def test_remove_reasoning_from_output():
    text = """Reasoning: 我认为这是一个测试。
    {"result": "ok"}"""
    cleaned = remove_reasoning_from_output(text)
    assert "Reasoning" not in cleaned
    assert cleaned.strip().startswith("{")

    # 中文测试
    text_cn = """思考：我们需要输出一个JSON。
    [1, 2, 3]"""
    cleaned_cn = remove_reasoning_from_output(text_cn)
    assert "思考" not in cleaned_cn
    assert cleaned_cn.startswith("[")


def test_extract_json_from_text_object():
    text = """```json
    {"name": "Alice", "age": 25}
    ```"""
    result = extract_json_from_text(text)
    assert isinstance(result, dict)
    assert result["name"] == "Alice"
    assert result["age"] == 25


def test_extract_json_from_text_array():
    text = """Reasoning: Some explanation
    [1, 2, 3]"""
    result = extract_json_from_text(text)
    assert isinstance(result, list)
    assert result == [1, 2, 3]


def test_extract_json_from_text_invalid():
    text = """Reasoning: 这是错误格式"""
    result = extract_json_from_text(text)
    assert "error" in result
    assert "raw_text" in result


def test_truncate_content_short_text():
    text = "short text"
    result = truncate_content(text, max_length=20)
    assert result == text


def test_truncate_content_long_text():
    text = "word " * 1000
    result = truncate_content(text, max_length=50)
    assert len(result) <= 53  # 包含 ...
    assert result.endswith("...")


def test_format_search_results_for_prompt():
    results = [
        {"content": "第一条结果"},
        {"content": "第二条结果"},
        {"content": ""}
    ]
    formatted = format_search_results_for_prompt(results)
    assert "第一条结果" in formatted
    assert "第二条结果" in formatted
    assert "\n\n" in formatted  # 多段拼接


def test_validate_json_schema():
    data = {"a": 1, "b": 2}
    required = ["a", "b"]
    assert validate_json_schema(data, required)

    required_missing = ["a", "c"]
    assert not validate_json_schema(data, required_missing)
