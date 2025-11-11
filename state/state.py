from attrs import field, define, asdict
from typing import Any
import json
import os
from datetime import datetime

@define(auto_attribs=True, slots=True)
class Serializable:
    version: int = 1
    created_at: str = field(factory=lambda: datetime.now().isoformat())
    updated_at: str = field(factory=lambda: datetime.now().isoformat())

    # 自动更新
    def _touch(self):
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


@define(auto_attribs=True, slots=True)
class Search(Serializable):
    query: str = ""
    url: str = ""
    title: str = ""
    content: str = ""
    score: float | None = None
    timestamp: str = field(factory=lambda: datetime.now().isoformat())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Search":
        return cls(
            query=data.get("query", ""),
            url=data.get("url", ""),
            title=data.get("title", ""),
            content=data.get("content", ""),
            score=data.get("score"),
            timestamp=data.get("timestamp", datetime.now().isoformat())
        )

@define(auto_attribs=True, slots=True)
class Research(Serializable):
    search_history: list[Search] = field(factory=list)
    latest_summary: str = ""
    reflection_iteration: int = 0
    is_completed: bool = False

    def add_search(self, search: Search):
        self.search_history.append(search)
        self._touch()

    def add_search_results(self, query: str, results: list[dict[str, Any]]):
        for result in results:
            search = Search(
                query=query,
                url=result.get("url", ""),
                title=result.get("title", ""),
                content=result.get("content", ""),
                score=result.get("score")
            )
            self.add_search(search)
        self._touch()

    def get_search_count(self) -> int:
        return len(self.search_history)

    def increment_reflection(self):
        self.reflection_iteration += 1
        self._touch()

    def mark_completed(self):
        self.is_completed = True
        self._touch()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Research":
        search_history = [Search.from_dict(search_data) for search_data in data.get("search_history", [])]
        return cls(
            search_history=search_history,
            latest_summary=data.get("latest_summary", ""),
            reflection_iteration=data.get("reflection_iteration", 0),
            is_completed=data.get("is_completed", False)
        )

@define(auto_attribs=True, slots=True)
class Paragraph(Serializable):
    title: str = ""
    content: str = ""
    research: Research = field(factory=Research)
    order: int = 0

    @property
    def is_completed(self) -> bool:
        return self.research.is_completed and bool(self.research.latest_summary)

    def get_final_content(self) -> str:
        return self.research.latest_summary or self.content

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Paragraph":
        research_data = data.get("research", {})
        research = Research.from_dict(research_data) if research_data else Research()

        return cls(
            title=data.get("title", ""),
            content=data.get("content", ""),
            research=research,
            order=data.get("order", 0)
        )

@define(auto_attribs=True, slots=True)
class State(Serializable):
    query: str = ""
    report_title: str = ""
    paragraphs: list[Paragraph] = field(factory=list)
    final_report: str = ""
    is_completed: bool = False

    def update_completion(self):
        """自动同步整体完成状态"""
        if self.paragraphs and all(p.is_completed for p in self.paragraphs):
            if not self.is_completed:
                self.is_completed = True
                self._touch()
        else:
            if self.is_completed:
                self.is_completed = False
                self._touch()

    def add_paragraph(self, title: str, content: str) -> int:
        order = len(self.paragraphs)
        paragraph = Paragraph(title=title, content=content, order=order)
        self.paragraphs.append(paragraph)
        self._touch()
        return order

    def get_paragraph(self, index: int) -> Paragraph | None:
        if 0 <= index < len(self.paragraphs):
            return self.paragraphs[index]
        return None

    def get_progress_summary(self) -> dict[str, Any]:
        self.update_completion()
        completed = sum(1 for p in self.paragraphs if p.is_completed)
        total = len(self.paragraphs)
        return {
            "total_paragraphs": total,
            "completed_paragraphs": completed,
            "progress_percentage": (completed / total * 100) if total > 0 else 0,
            "is_completed": self.is_completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "State":
        paragraphs = [Paragraph.from_dict(p_data) for p_data in data.get("paragraphs", [])]

        return cls(
            query=data.get("query", ""),
            report_title=data.get("report_title", ""),
            paragraphs=paragraphs,
            final_report=data.get("final_report", ""),
            is_completed=data.get("is_completed", ""),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat())
        )

    @classmethod
    def from_json(cls, json_str: str) -> "State":
        data = json.loads(json_str)
        return cls.from_dict(data)

    def save_to_file(self, filepath: str):
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(self.to_json())

    @classmethod
    def load_from_file(cls, filepath: str) -> "State":
        with open(filepath, "r", encoding='utf-8') as f:
            json_str = f.read()
        return cls.from_json(json_str)