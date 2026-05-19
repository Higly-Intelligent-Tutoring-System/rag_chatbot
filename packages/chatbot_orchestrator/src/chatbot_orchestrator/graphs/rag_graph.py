from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langgraph.graph import StateGraph, START, END

from chatbot_orchestrator.schemas.schemas import RagState
from chatbot_orchestrator.nodes import *

from chatbot_orchestrator.prompts.rag import get_rag_prompt


class RAGGraphBuilder:
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
        generate = build_single_rag_node(
            llm=self._llm,
            prompt=get_rag_prompt(),
        )

        # ── Assemble graph ──────────────────────────────
        builder = StateGraph(RagState)

        builder.add_node("retrieve", retrieve)
        builder.add_node("generate", generate)

        builder.add_edge(START, "retrieve")
        builder.add_edge("retrieve", "generate")
        builder.add_edge("generate", END)

        return builder