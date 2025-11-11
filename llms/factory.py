from typing import Any, Type
from .base import BaseLLM

class LLMFactory:

    _register: dict[str, Type[BaseLLM]] = {}

    @classmethod
    def register(cls, name: str, llm_class: Type[BaseLLM]) -> None:
        cls._register[name.lower()] = llm_class

    @classmethod
    def create(cls, provider: str, model_name: str, config: dict[str, Any]):
        provider = provider.lower()

        match provider:
            case "openai":
                from .openai_llm import OpenAILLM
                return OpenAILLM(model_name, config)
        #后续增加
            case _:
                raise ValueError(f"未知的 LLM 提供商：{provider}")

        llm_class = cls._regiter[provider]
        return llm_class(model_name, config)

