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
    step: Literal["a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "b4", "b5", "c1", "c2", "c3", "c4", "c5", "d1", "d2", "d3", "d4", "d5"] = Field(
        default="a1",
        description="Il prossimo passo nel processo di indirizzamento."
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

        a1 = build_generation_node(
            llm=self._llm,
            prompt=get_a1_prompt(),
        )
        a2 = build_generation_node(
            llm=self._llm,
            prompt=get_a2_prompt(),
        )
        a3 = build_generation_node(
            llm=self._llm,
            prompt=get_a3_prompt(),
        )
        a4 = build_generation_node(
            llm=self._llm,
            prompt=get_a4_prompt(),
        )
        a5 = build_generation_node(
            llm=self._llm,
            prompt=get_a5_prompt(),
        )
        b1 = build_generation_node(
            llm=self._llm,
            prompt=get_b1_prompt(),
        )
        b2 = build_generation_node(
            llm=self._llm,
            prompt=get_b2_prompt(),
        )
        b3 = build_generation_node(
            llm=self._llm,
            prompt=get_b3_prompt(),
        )
        b4 = build_generation_node(
            llm=self._llm,
            prompt=get_b4_prompt(),
        )
        b5 = build_generation_node(
            llm=self._llm,
            prompt=get_b5_prompt(),
        )
        c1 = build_generation_node(
            llm=self._llm,
            prompt=get_c1_prompt(),
        )
        c2 = build_generation_node(
            llm=self._llm,
            prompt=get_c2_prompt(),
        )
        c3 = build_generation_node(
            llm=self._llm,
            prompt=get_c3_prompt(),
        )
        c4 = build_generation_node(
            llm=self._llm,
            prompt=get_c4_prompt(),
        )
        c5 = build_generation_node(
            llm=self._llm,
            prompt=get_c5_prompt(),
        )
        d1 = build_generation_node(
            llm=self._llm,
            prompt=get_d1_prompt(),
        )
        d2 = build_generation_node(
            llm=self._llm,
            prompt=get_d2_prompt(),
        )
        d3 = build_generation_node(
            llm=self._llm,
            prompt=get_d3_prompt(),
        )
        d4 = build_generation_node(
            llm=self._llm,
            prompt=get_d4_prompt(),
        )
        d5 = build_generation_node(
            llm=self._llm,
            prompt=get_d5_prompt(),
        )
        
        router = self._llm.with_structured_output(Route)
        def router_node(state: RoutingState):
            """Route the input to the appropriate node"""

            # Run the augmented LLM with structured output to serve as routing logic
            decision = router.invoke(
                [
                    SystemMessage(
                        content="""Sei un assistente all'orientamento. Analizza la domanda dell'utente e classificala in UNA di queste categorie:
                        - “a1”: l'utente chiede “Come posso iscrivermi a un esame?” o qualcosa di simile.
                        - “a2”: l'utente chiede informazioni sulla scadenza per l'iscrizione, sull'iscrizione tardiva o sui tempi di iscrizione ai corsi.
                        - “a3”: l'utente chiede informazioni su crediti, crediti minimi, progressione, avviso accademico, ripetizione dell'anno.
                        - “a4”: l'utente utilizza termini quali ricorso, reclamo, contestazione di un voto, revisione del risultato.
                        - “a5”: l'utente chiede informazioni su tasse, scadenza di pagamento, rate, mora, mancato pagamento.
                        - “b1”: l'utente chiede “Che cos'è...?”, “Non capisco...”, “Qual è la differenza tra...”.
                        - “b2”: “Cosa dovrei studiare?”, “Da dove comincio?”, “Cosa è importante in questo argomento?” o altre domande simili.
                        - “b3”: la domanda riflette confusione tra due idee simili o una difficoltà concettuale nota.
                        - “b4”: “Aiutami a studiare...”, “Ho bisogno di un piano per questo argomento”, “Come posso ripassare...”.
                        - “b5”: “Sono indietro”, “Non so da dove cominciare”, “Non riesco a concentrarmi su questo argomento”.
                        - “c1”: menziona tutor, tutoraggio, aiuto nello studio, supporto con il corso.
                        - “c2”: chiede studio di gruppo, aiuto tra pari, compagni di classe, compagno di studio.
                        - “c3”: espressioni che denotano disagio entro i limiti consentiti, richiesta esplicita di sostegno per il benessere.
                        - “c4”: menziona accessibilità, agevolazioni, tempo aggiuntivo, disposizioni speciali, sostegno per la disabilità.
                        - “c5”: menziona CV, curriculum, tirocinio, carriera, colloquio, candidatura.
                        - “d1”: “Ho bisogno di un piano di studio”, “Aiutami a organizzare la mia settimana”, “Come dovrei prepararmi?”.
                        - “d2”: l'utente chiede aiuto per la preparazione in relazione a una scadenza ufficiale imminente.
                        - “d3”: chiede informazioni su gestione del tempo, procrastinazione, sovraccarico, equilibrio.
                        - “d4”: “Non riesco a iniziare”, “Sto procrastinando”, “Mi sento in ritardo”, “Dammi un piccolo passo da compiere”.
                        - “d5”: chiede come partecipare di più, prepararsi per la lezione, contribuire alla discussione.

                        Rispondi SOLO con il nome della categoria.
                        """
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
        builder.add_node("a1", a1)
        builder.add_node("a2", a2)
        builder.add_node("a3", a3)
        builder.add_node("a4", a4)
        builder.add_node("a5", a5)
        builder.add_node("b1", b1)
        builder.add_node("b2", b2)
        builder.add_node("b3", b3)
        builder.add_node("b4", b4)
        builder.add_node("b5", b5)
        builder.add_node("c1", c1)
        builder.add_node("c2", c2)
        builder.add_node("c3", c3)
        builder.add_node("c4", c4)
        builder.add_node("c5", c5)
        builder.add_node("d1", d1)
        builder.add_node("d2", d2)
        builder.add_node("d3", d3)
        builder.add_node("d4", d4)
        builder.add_node("d5", d5)
        
        builder.add_node("router_node", router_node)


        builder.add_edge(START, "retrieve")
        builder.add_edge("retrieve", "router_node")
        builder.add_conditional_edges(
            "router_node",
            route_decision,
            {  # Name returned by route_decision : Name of next node to visit
                "a1": "a1",
                "a2": "a2",
                "a3": "a3",
                "a4": "a4",
                "a5": "a5",
                "b1": "b1",
                "b2": "b2",
                "b3": "b3",
                "b4": "b4",
                "b5": "b5",
                "c1": "c1",
                "c2": "c2",
                "c3": "c3",
                "c4": "c4",
                "c5": "c5",
                "d1": "d1",
                "d2": "d2",
                "d3": "d3",
                "d4": "d4",
                "d5": "d5",
            },
        )
        builder.add_edge("a1", END)
        builder.add_edge("a2", END)
        builder.add_edge("a3", END)
        builder.add_edge("a4", END)
        builder.add_edge("a5", END)
        builder.add_edge("b1", END)
        builder.add_edge("b2", END)
        builder.add_edge("b3", END)
        builder.add_edge("b4", END)
        builder.add_edge("b5", END)
        builder.add_edge("c1", END)
        builder.add_edge("c2", END)
        builder.add_edge("c3", END)
        builder.add_edge("c4", END)
        builder.add_edge("c5", END)
        builder.add_edge("d1", END)
        builder.add_edge("d2", END)
        builder.add_edge("d3", END)
        builder.add_edge("d4", END)
        builder.add_edge("d5", END)

        return builder