from dotenv import load_dotenv
load_dotenv()

from config import Config
from llms.factory import LLMFactory

if __name__ == "__main__":
    config = Config()
    llm_config = config.get_llm_config()

    llm = LLMFactory.create(config.llm_provider, config.openai_model, llm_config)

    messages = [
        {"role": "system", "content": "你是一个简洁回答助手。"},
        {"role": "user", "content": "请简短回答：现在的A股行情如何？"}
    ]

    print("\n--- 开始流式输出 ---\n")

    for chunk in llm.astream(messages):
        print(chunk, end="", flush=True)

    print("\n--- 流式输出结束 ---")
