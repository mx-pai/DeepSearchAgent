import os
from typing import Any
from attrs import define, asdict
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()


@define(auto_attribs=True, slots=True)
class SearchResult:
    title: str
    url: str
    content: str
    score: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SearchResult":
        return cls(
            title=data.get("title", ""),
            url=data.get("url", ""),
            content=data.get("content", ""),
            score=data.get("score")
        )


class TavilySearch:
    def __init__(self, api_key: str | None = None):
        if api_key is None:
            api_key = os.getenv("TAVILY_API_KEY")
            if not api_key:
                raise ValueError("Tavily API Key未找到， 请设置TAVILY_API_KEY环境变量或在初始化时提供")
        self.client = TavilyClient(api_key=api_key)

    def search(self,
               query: str,
               max_results: int = 5,
               include_raw_content: bool = True,
               timeout: int = 240) -> list[SearchResult]:
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                include_raw_content=include_raw_content,
                timeout=timeout
            )
            results = [SearchResult.from_dict(item) for item in response.get("results", [])]
            return [r.to_dict() for r in results]

        except Exception as e:
            print(f"搜索错误: {str(e)}")
            return []

_tavily_client: TavilyClient | None = None

def get_tavily_client() -> TavilySearch:
    global _tavily_client
    if _tavily_client is None:
        _tavily_client = TavilySearch()
    return _tavily_client

def tavily_search(query: str, **kwargs) -> list[SearchResult]:
    return get_tavily_client().search(query, **kwargs)


def test_search(query: str = "武大诬陷案", max_results: int = 3):
    print(f"\n=== 测试Tavily搜索功能 ===")
    print(f"搜索查询: {query}")
    print(f"最大结果数: {max_results}")

    try:
        results = tavily_search(query, max_results=max_results)

        if results:
            print(f"\n找到 {len(results)} 个结果:")
            for i, result in enumerate(results, 1):
                print(f"\n结果 {i}:")
                print(f"标题: {result['title']}")
                print(f"链接: {result['url']}")
                print(f"内容摘要: {result['content'][:200]}...")
                if result.get('score'):
                    print(f"相关度评分: {result['score']}")
        else:
            print("未找到搜索结果")

    except Exception as e:
        print(f"搜索测试失败: {str(e)}")

if __name__ == "__main__":
    test_search()























