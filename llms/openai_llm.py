from openai import OpenAI, AsyncOpenAI
from typing import Any, Generator, AsyncGenerator
from .base import BaseLLM, LLMMessage

class OpenAILLM(BaseLLM):

    def __init__(self, model_name: str, config: dict[str, Any]):
        super().__init__(model_name, config)

        if not self.api_key:
            raise ValueError("OpenAI API Key 未设置，请在config或环境变量提供")
        if not self.base_url:
            raise ValueError("OpenAI Base Url 未设置，请在config提供")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
            )

        self.async_client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url)

    def _build_params(self, messages, stream=False, **kwargs) -> dict[str, Any]:
        return {
            "model": self.model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.config.get("temperature", 0.7)),
            "max_tokens": kwargs.get("max_tokens", self.config.get("max_tokens", 4096)),
        }


    def invoke(self, messages: list[LLMMessage], **kwargs) ->  str:

        try:
            response = self.client.chat.completions.create(**self._build_params(messages, **kwargs))

            content = response.choices[0].message.content if response.choices else ""

            return self.validate_response(content)

        except Exception as e:
            print(f"[OpenAILLM] 同步调用错误: {str(e)}")
            raise

    async def ainvoke(self, messages: list[LLMMessage], **kwargs) ->  str:
        try:
            response = await self.async_client.chat.completions.create(**self._build_params(messages, **kwargs))

            content = response.choices[0].message.content if response.choices else ""

            return self.validate_response(content)

        except Exception as e:
            print(f"[OpenAILLM] 异步调用错误: {str(e)}")
            raise

    def stream(self, messages: list[LLMMessage], **kwargs) -> Generator[str, Any, Any]:
        try:
            with self.client.chat.completions.stream(**self._build_params(messages, **kwargs)) as stream:
                for event in stream:
                    if getattr(event, "type", None) == "content.delta":
                        chunk = event.delta
                        if chunk:
                            yield chunk
        except Exception as e:
            print(f"[OpenAILLM] 同步流式调用错误：{e}")
            raise

    async def astream(self, messages: list[LLMMessage], **kwargs) -> AsyncGenerator[str, Any]:
        try:
            async with self.async_client.chat.completions.stream(**self._build_params(messages, **kwargs)) as stream:
                async for event in stream:
                    if getattr(event, "type", None) == "content.delta":
                        chunk = event.delta
                        if chunk:
                            yield chunk
        except Exception as e:
            print(f"[OpenAILLM] 异步流式调用错误：{e}")
            raise

