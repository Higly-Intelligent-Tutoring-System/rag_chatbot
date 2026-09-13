# packages/evaluation/evaluation/dataset_builder.py

import uuid
import asyncio
from typing import TypedDict, List, Optional

from ragas import EvaluationDataset
from ragas.dataset_schema import SingleTurnSample

from chatbot_orchestrator import ChatService


class TestQuery(TypedDict):
    """One entry in your golden test set."""
    question: str
    reference: Optional[str]  # the expected / ground-truth answer


async def build_evaluation_dataset(
    chat_service: ChatService,
    test_queries: List[TestQuery],
    retriever,                      # LangChain VectorStoreRetriever
    thread_id_prefix: str = "eval",
) -> EvaluationDataset:
    """
    For every test query:
      1. Ask ChatService for an answer (fresh thread per query).
      2. Ask the retriever for the context chunks.
      3. Pack into a SingleTurnSample.

    Returns a ragas EvaluationDataset.
    """
    samples: List[SingleTurnSample] = []

    for idx, entry in enumerate(test_queries):
        question = entry["question"]

        # ── 1. Generate answer via the compiled LangGraph ─────────────────────
        thread_id = f"{thread_id_prefix}-{idx}-{uuid.uuid4().hex[:8]}"
        response = await chat_service.ainvoke(question, thread_id)

        # ── 2. Retrieve context chunks ─────────────────────────────────────────
        # retriever.ainvoke returns List[Document]; we extract .page_content
        contexts = []
        if retriever:
            docs = await retriever.ainvoke(question)
            contexts: List[str] = [doc.page_content for doc in docs]

        # ── 3. Build ragas sample ──────────────────────────────────────────────
        sample = SingleTurnSample(
            user_input=question,
            response=response,
            retrieved_contexts=contexts,
            # 'reference' is optional; include if you have ground-truth answers
            reference=entry.get("reference"),
        )
        samples.append(sample)

        #print(f"  [{idx+1}/{len(test_queries)}] ✓  {question[:60]}")

    return EvaluationDataset(samples=samples)