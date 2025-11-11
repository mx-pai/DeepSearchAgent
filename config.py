import os
from attrs import define

@define(auto_attribs=True, slots=True)
class Config:
    llm_provider: str = "openai"
    openai_model: str = "gpt-5-mini"
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL")

    def get_llm_config(self) -> dict[str, str]:
        match self.llm_provider:
            case "openai":
                return {
                    "api_key": self.openai_api_key,
                    "base_url": self.openai_base_url,
                    "temperature": 0.7,
                    "max_tokens": 4096
                }
            case _:
                raise ValueError(f"未知的LLM提供商： {self.llm_provider}")
