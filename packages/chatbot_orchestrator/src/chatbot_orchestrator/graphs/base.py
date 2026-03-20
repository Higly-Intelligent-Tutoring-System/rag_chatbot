"""
Every graph builder follows this protocol so the service
can treat them uniformly.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from langgraph.graph import StateGraph


@runtime_checkable
class GraphBuilder(Protocol):
    """
    Protocol for graph builders.
    
    Implementations return an UNCOMPILED StateGraph.
    Compilation (with checkpointer + store) is the service's job.
    """

    @property
    def name(self) -> str:
        """Human-readable name for telemetry / logging."""
        ...

    def build(self) -> StateGraph:
        """
        Return an uncompiled StateGraph.
        
        Why uncompiled?
        → The service layer injects checkpointer & store at compile time.
        → This keeps graphs pure and testable without infrastructure.
        """
        ...