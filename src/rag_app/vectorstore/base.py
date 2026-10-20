from __future__ import annotations

from abc import ABC, abstractmethod


class VectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: list[dict]) -> None:
        raise NotImplementedError

    @abstractmethod
    def similarity_search(self, query: str, k: int = 4) -> list[dict]:
        raise NotImplementedError
