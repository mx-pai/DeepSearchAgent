from abc import ABC, abstractmethod
from typing import Any,  Literal, TypedDict, Generator, AsyncGenerator

class LLMMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str

class BaseLLM(ABC):
    """LLM 抽象基类"""
    def __init__(self, model_name: str, config: dict[str, Any]):
        self.model_name = model_name
        self.config = config

        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url")

    @abstractmethod
    def invoke(self, messages: list[LLMMessage], **kwargs) -> str:
        pass

    @abstractmethod
    async def ainvoke(self, messages: list[LLMMessage], **kwargs) -> str:
        pass

    def stream(self, messages: list[LLMMessage], **kwargs) -> Generator[str, Any, Any]:
        raise NotImplementedError(f"{self.__class__.__name__} does not support streaming")

    async def astream(self, messages: list[LLMMessage], **kwargs) -> AsyncGenerator[str, Any]:
        raise NotImplementedError(f"{self.__class__.__name__} does not  async support streaming")



    def validate_response(self, response: str) -> str:
        if response is None:
            return ""
        return response.strip()

    def get_model_info(self) -> dict[str, Any]:
        return {
            "model_name": self.model_name,
            "config": self.config,
            "api_key_set": bool(self.api_key),
            "base_url": self.base_url,
            "class": self.__class__.__name__
        }

