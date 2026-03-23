"""
Central place to register and look up available graphs.
Keeps rag-api from importing concrete graph classes directly.
"""
from __future__ import annotations

from .base import GraphBuilder
from .rag_graph import RAGGraphBuilder

# ── Registry ────────────────────────────────────────────
_REGISTRY: dict[str, GraphBuilder] = {}


def _register(builder: GraphBuilder) -> None:
    _REGISTRY[builder.name] = builder


# Register all graphs at import time
_register(RAGGraphBuilder())


def get_graph_builder(name: str) -> GraphBuilder:
    if name not in _REGISTRY:
        available = ", ".join(_REGISTRY.keys())
        raise ValueError(f"Unknown graph '{name}'. Available: {available}")
    return _REGISTRY[name]


def available_graphs() -> list[str]:
    return list(_REGISTRY.keys())