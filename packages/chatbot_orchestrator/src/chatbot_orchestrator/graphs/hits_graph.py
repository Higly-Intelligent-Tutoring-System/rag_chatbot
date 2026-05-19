from __future__ import annotations
from typing import Literal

from chatbot_orchestrator.nodes.retrieval import build_retrieval_node
from langchain.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langgraph.graph import StateGraph, START, END

from chatbot_orchestrator.graphs.base import GraphBuilder
from chatbot_orchestrator.schemas.schemas import RoutingState
from chatbot_orchestrator.nodes.generation import build_single_rag_node
from chatbot_orchestrator.tools.retrival import search_vectordb
from chatbot_orchestrator.prompts.hits import *


# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["administrative", "learning", "services", "planning"] = Field(
        default="learning",
        description="The next step in the routing process"
    )

class HitsGraphBuilder(GraphBuilder):
    """
    Graph structured to meet the necessities of the HITS Chatbot.
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
        return "HITS"
    
    def build(self) -> StateGraph:
        retriever = self._retriever
        if retriever is None:
            from core.vectordb import get_vector_store
            retriever = get_vector_store()

        retrieve = build_retrieval_node(retriever=retriever)

        administrative = build_single_rag_node(
            llm=self._llm,
            prompt=get_administrative_prompt(),
        )
        learning = build_single_rag_node(
            llm=self._llm,
            prompt=get_learning_prompt(),
        )
        services = build_single_rag_node(
            llm=self._llm,
            prompt=get_services_prompt(),
        )
        planning = build_single_rag_node(
            llm=self._llm,
            prompt=get_planning_prompt(),
        )

        router = self._llm.with_structured_output(Route)
        def router_node(state: RoutingState):
            """Route the input to the appropriate node"""

            # Run the augmented LLM with structured output to serve as routing logic
            decision = router.invoke(
                [
                    SystemMessage(
                        content="""You are a routing assistant. Analyze the user's question and classify it into ONE of these categories:
                        - "administrative": Questions about rules, procedures, deadlines, enrollment, exam rules, credits, institutional policies or fees
                        - "learning": Questions about course concepts, study strategies, assignments, understanding topics
                        - "services": Requests for help connecting to tutoring, counseling, disability support, or other institutional services
                        - "planning": Requests for help organizing time, creating study plans, or managing tasks

                        Respond with ONLY the category name."""
                    ),
                    HumanMessage(content=state["messages"][-1].content),
                ]
            )

            return {"decision": decision.step}
        
        # Conditional edge function to route to the appropriate node
        def route_decision(state: RoutingState):
            # Return the node name you want to visit next
            return state["decision"]
        
        
        # ── Assemble graph ──────────────────────────────
        builder = StateGraph(RoutingState)

        builder.add_node("retrieve", retrieve)
        builder.add_node("administrative", administrative)
        builder.add_node("learning", learning)
        builder.add_node("services", services)
        builder.add_node("planning", planning)
        builder.add_node("router_node", router_node)


        builder.add_edge(START, "retrieve")
        builder.add_edge("retrieve", "router_node")
        builder.add_conditional_edges(
            "router_node",
            route_decision,
            {  # Name returned by route_decision : Name of next node to visit
                "administrative": "administrative",
                "learning": "learning",
                "services": "services",
                "planning": "planning",
            },
        )
        builder.add_edge("administrative", END)
        builder.add_edge("learning", END)
        builder.add_edge("services", END)
        builder.add_edge("planning", END)

        return builder