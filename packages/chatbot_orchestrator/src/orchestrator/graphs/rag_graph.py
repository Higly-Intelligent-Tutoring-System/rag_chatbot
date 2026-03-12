from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langgraph.graph import StateGraph, START, END

from orchestrator.schemas.schemas import RAGState
from orchestrator.nodes import *

from orchestrator.prompts import get_rag_prompt


class RAGGraph:
    """
    Configurable RAG graph.

    Defaults are sensible, but every dependency can be overridden:

        # Default
        RAGGraph()

        # Everything custom
        RAGGraph(
            retriever=my_retriever,
            llm=my_llm,
        )
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
        return "BasicRagGraph"

    def build(self) -> StateGraph:
        # ── Resolve retriever (lazy so core isn't imported at class level) ──
        retriever = self._retriever
        if retriever is None:
            from core.vectordb import get_vector_store
            retriever = get_vector_store()

        # ── Create node functions via factories ─────────
        retrieve = build_retrieval_node(retriever=retriever)
        generate = build_generation_node(
            llm=self._llm,
            system_prompt=get_rag_prompt(),
        )

        # ── Assemble graph ──────────────────────────────
        builder = StateGraph(RAGState)

        builder.add_node("retrieve", retrieve)
        builder.add_node("generate", generate)

        builder.add_edge(START, "retrieve")
        builder.add_edge("retrieve", "generate")
        builder.add_edge("generate", END)

        return builder