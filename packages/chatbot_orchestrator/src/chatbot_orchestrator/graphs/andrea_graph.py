from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langgraph.graph import StateGraph, START, END

from chatbot_orchestrator.graphs.base import GraphBuilder
from chatbot_orchestrator.schemas.schemas import AndreaState
from chatbot_orchestrator.nodes.generation import build_andrea_generation_node
from chatbot_orchestrator.prompts.gpt import get_refined_prompt



class AndreaGraphBuilder(GraphBuilder):
    """
    GPT-A Graph: A simple graph that uses GPT-A for direct question answering without retrieval. This graph is designed to test the capabilities of GPT-A in generating accurate and concise answers based solely on the user's question, without any additional context from retrieved documents.

    It does not rely on on-prem retrievers or vector stores, due to responses' API built-in file search.
    """

    def __init__(
        self,
        retriever: BaseRetriever | None = None,
        llm: BaseChatModel | None = None,
    ):
        super().__init__(retriever, llm)


    @property
    def name(self) -> str:
        return "AndreaGraph"

    def build(self) -> StateGraph:
        # ── Create node functions via factories ─────────
        generate = build_andrea_generation_node(
            llm=self._llm,
            prompt=get_refined_prompt(),
        )

        # ── Assemble graph ──────────────────────────────
        builder = StateGraph(AndreaState)

        builder.add_node("generate", generate)

        builder.add_edge(START, "generate")
        builder.add_edge("generate", END)

        return builder