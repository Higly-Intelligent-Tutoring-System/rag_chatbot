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
from chatbot_orchestrator.nodes.generation import build_generation_node
from chatbot_orchestrator.prompts.italian import *


# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["amministrativo", "apprendimento", "servizi", "pianificazione"] = Field(
        default="amministrativo",
        description="Il prossimo passo nel processo di routing"
    )

class NudgingItalianGraphBuilder(GraphBuilder):
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
        return "NudgingItalian"
    
    def build(self) -> StateGraph:
        retriever = self._retriever
        if retriever is None:
            from core.vectordb import get_vector_store
            retriever = get_vector_store()

        retrieve = build_retrieval_node(retriever=retriever)

        administrative = build_generation_node(
            llm=self._llm,
            prompt=get_administrative_prompt(),
        )
        learning = build_generation_node(
            llm=self._llm,
            prompt=get_learning_prompt(),
        )
        services = build_generation_node(
            llm=self._llm,
            prompt=get_services_prompt(),
        )
        planning = build_generation_node(
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
                        content="""Sei un assistente di smistamento. Analizza la domanda dell'utente e classificala in UNA delle seguenti categorie:
                        - “amministrativo”: domande su regolamenti, procedure, scadenze, iscrizioni, norme d'esame, crediti, politiche istituzionali o tasse
                        - “apprendimento”: domande su concetti dei corsi, strategie di studio, compiti, comprensione degli argomenti
                        - “servizi”: richieste di assistenza per accedere a tutoraggio, consulenza, supporto per disabilità o altri servizi istituzionali
                        - “pianificazione”: richieste di assistenza per organizzare il tempo, creare piani di studio o gestire i compiti

                        Rispondi indicando SOLO il nome della categoria."""
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
        builder.add_node("amministrativo", administrative)
        builder.add_node("apprendimento", learning)
        builder.add_node("servizi", services)
        builder.add_node("pianificazione", planning)
        builder.add_node("router_node", router_node)


        builder.add_edge(START, "retrieve")
        builder.add_edge("retrieve", "router_node")
        builder.add_conditional_edges(
            "router_node",
            route_decision,
            {  # Name returned by route_decision : Name of next node to visit
                "amministrativo": "amministrativo",
                "apprendimento": "apprendimento",
                "servizi": "servizi",
                "pianificazione": "pianificazione",
            },
        )
        builder.add_edge("amministrativo", END)
        builder.add_edge("apprendimento", END)
        builder.add_edge("servizi", END)
        builder.add_edge("pianificazione", END)

        return builder