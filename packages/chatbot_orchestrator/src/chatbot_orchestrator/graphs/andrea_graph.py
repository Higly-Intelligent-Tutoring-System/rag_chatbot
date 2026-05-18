from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState

from chatbot_orchestrator.nodes import *
from chatbot_orchestrator.prompts.gpt import get_gpt_a_prompt
from supabase_auth import model


class AndreaGraphBuilder:
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
        return "AndreaGraph"

    def build(self) -> StateGraph:
        # ── Attaching openai's LLM with server tools ────
        model = ChatOpenAI(
                    model="gpt-5.4-mini", 
                    use_responses_api=True, 
                    reasoning={"effort": "low"},
                    output_version="v1",
                )
        tools = [{
            "type": "file_search",
            "vector_store_ids": ["vs_6a072cf47c8481918470de3b01dcca74"]
        }]
        self._llm = model.bind_tools(tools)
        
        # ── Create node functions via factories ─────────
        generate = build_generation_node(
            llm=self._llm,
            prompt=get_gpt_a_prompt(),
        )

        # ── Assemble graph ──────────────────────────────
        builder = StateGraph(MessagesState)

        builder.add_node("generate", generate)

        builder.add_edge(START, "generate")
        builder.add_edge("generate", END)

        return builder