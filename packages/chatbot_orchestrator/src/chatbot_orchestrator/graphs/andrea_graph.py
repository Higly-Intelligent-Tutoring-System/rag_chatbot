from __future__ import annotations


from api.config import ApiSettings
from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState

from chatbot_orchestrator.nodes.generation import build_multiple_generation_node
from chatbot_orchestrator.prompts.gpt import get_gpt_a_prompt



class AndreaGraphBuilder:
    """
    GPT-A Graph: A simple graph that uses GPT-A for direct question answering without retrieval. This graph is designed to test the capabilities of GPT-A in generating accurate and concise answers based solely on the user's question, without any additional context from retrieved documents.

    It does not rely on on-prem retrievers or vector stores, due to responses' API built-in file search.
    """

    def __init__(
        self,
        vs_id: str | None = None,
    ):
        self._vs_id = vs_id


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
            "vector_store_ids": [self._vs_id] if self._vs_id else []
        }]
        self._llm = model.bind_tools(tools)
        
        # ── Create node functions via factories ─────────
        generate = build_multiple_generation_node(
            llm=self._llm,
            prompt=get_gpt_a_prompt(),
        )

        # ── Assemble graph ──────────────────────────────
        builder = StateGraph(MessagesState)

        builder.add_node("generate", generate)

        builder.add_edge(START, "generate")
        builder.add_edge("generate", END)

        return builder