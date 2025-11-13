from dotenv import load_dotenv
load_dotenv()

import json
from config import Config
from llms.factory import LLMFactory
from nodes.search_node import FirstSearchNode


def test_first_search_node():
    print("\n====== 测试 FirstSearchNode ======")

    # 1. 加载配置（记得确保 .env 已经生效）
    config = Config()
    llm_config = config.get_llm_config()

    # 2. 创建 LLM 实例
    llm = LLMFactory.create(
        provider=config.llm_provider,
        model_name=config.openai_model,
        config=llm_config
    )

    # 3. 创建 Node
    node = FirstSearchNode(llm)

    # 4. 构造输入
    input_data = {
        "title": "2025年A股走势分析",
        "content": "请根据基本面、资金面、宏观经济等因素预测A股未来走势。"
    }

    # 5. 执行 Node
    result = node.run(input_data)

    print("\n--- Node 输出 ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    assert "search_query" in result and result["search_query"]
    print("\n测试通过！")


if __name__ == "__main__":
    test_first_search_node()