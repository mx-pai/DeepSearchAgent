import json
from typing import Any
from json.decoder import JSONDecodeError
from nodes.base_node import BaseNode

from prompts import SYSTEM_PROMPT_FIRST_SEARCH, SYSTEM_PROMPT_REFLECTION
from utils.text_processing import (
    remove_reasoning_from_output,
    clean_code_block_tags,
    extract_json_from_text
)

class FirstSearchNode(BaseNode):
    def __init__(self, llm_client, node_name = ""):
        super().__init__(llm_client, "FirstSearchNode")

    def validate_input(self, input_data: Any) -> bool:
        if isinstance(input_data, str):
            try:
                data = json.loads(input_data)
                return "title" in data and "content" in data
            except JSONDecodeError:
                return False
        elif isinstance(input_data, dict):
            return "title" in input_data and "content" in input_data
        return False

    def before_run(self, input_data: Any):
        self.log_info("开始进行首次查询")

    def run(self, input_data: Any, **kwargs) -> dict[str, Any]:
        self.before_run(input_data)
        try:
            if not self.validate_input(input_data):
                raise ValueError("输入格式错误，需要包含title和content字段")

            if isinstance(input_data, dict):
                message = json.dumps(input_data, ensure_ascii=False)
            else:
                message = input_data

            response =self.llm_client.invoke(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_FIRST_SEARCH},
                    {"role": "user", "content": message}
                    ])
            result = self.process_output(response)
            self.after_run(result)
            return result

        except Exception as e:
            self.log_error(f"生成首次搜索查询失败: {str(e)}")
            raise e

    def after_run(self, result: Any):
        self.log_info(f"生成搜索查询：{result.get('search_query', 'N/A')}")


    def process_output(self, output: str) -> dict[str, Any]:
        try:
            cleaned_output = remove_reasoning_from_output(output)
            cleaned_output = clean_code_block_tags(cleaned_output)

            try:
                result = json.loads(cleaned_output)
            except JSONDecodeError:
                result = extract_json_from_text(cleaned_output)
                if "error" in result:
                    raise ValueError("JSON解析失败")

            search_query = result.get("search_query", "")
            reasoning = result.get("reasoning", "")

            if not search_query:
                raise ValueError("未找到搜索查询")

            return {
                "search_query": search_query,
                "reasoning": reasoning
            }


        except Exception as e:
            self.log_error(f"处理输出失败：{str(e)}")
            return {
                "search_query": "相关主题研究",
                "reasoning": "解析失败，使用默认搜索查询"
            }

class ReflectionNode(BaseNode):
    def __init__(self, llm_client, node_name = ""):
        super().__init__(llm_client, "ReflectionNode")

    def validate_input(self, input_data: Any) -> bool:

        return super().validate_input(input_data)


























