"""
Every graph builder follows this protocol so the service
can treat them uniformly.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from langchain.chat_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langgraph.graph import StateGraph


class GraphBuilder(ABC):
    """
    Graph builders base class.
    
    Implementations return an UNCOMPILED StateGraph.
    Compilation (with checkpointer + store) is the service's job.
    """
    def __init__(
        self,
        retriever: BaseRetriever | None = None,
        llm: BaseChatModel | None = None,
    ):
        self._retriever = retriever
        self._llm = llm

    @property
    def name(self) -> str:
        """Human-readable name for telemetry / logging."""
        pass

    @abstractmethod
    def build(self) -> StateGraph:
        """
        Return an uncompiled StateGraph.
        
        Why uncompiled?
        → The service layer injects checkpointer & store at compile time.
        → This keeps graphs pure and testable without infrastructure.
        """
        pass