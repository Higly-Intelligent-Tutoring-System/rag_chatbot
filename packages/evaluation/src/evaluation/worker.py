import asyncio
import json
import os
from langchain.chat_models import init_chat_model
from core import get_embeddings_model, get_vector_store
from chatbot_orchestrator import ChatService
from chatbot_orchestrator.graphs.registry import get_graph_builder
from evaluation.dataset_builder import build_evaluation_dataset
from evaluation.service import EvalService
from evaluation.metrics import FULL_METRICS  # or REFERENCE_FREE_METRICS
from evaluation.config  import eval_settings, core_settings, datasets_dir


chatbot_llm = init_chat_model(
    model=eval_settings.MODEL_NAME,
    model_provider=eval_settings.PROVIDER_NAME,
    temperature=eval_settings.MODEL_TEMPERATURE,
    )
evaluator_llm = init_chat_model(
    model=eval_settings.MODEL_NAME,
    model_provider=eval_settings.PROVIDER_NAME,
    temperature=eval_settings.MODEL_TEMPERATURE,
    )
embeddings = get_embeddings_model(core_settings)
vectordb  = get_vector_store(core_settings)
retriever = vectordb.as_retriever(search_kwargs={"k": 4})


async def main():
    # 1. Load test queries ---------------------------------------------------
    test_queries = []
    for dataset in sorted(datasets_dir.glob("*.json")):
        try:
            with open(dataset) as f:
                test_queries += json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON in {dataset}: {e}") from e
        

    # 2. Build & compile ChatService ----------------------------------------
    chat_service = ChatService(
        graph_builder=get_graph_builder(eval_settings.GRAPH_NAME),
        llm=chatbot_llm,
        retriever=vectordb,
    )
    await chat_service.compile()
    print("✅ ChatService compiled.")

    # 3. Build the ragas EvaluationDataset ---------------------------------
    print(f"\n⏳ Running {len(test_queries)} queries through the chatbot…")
    dataset = await build_evaluation_dataset(
        chat_service=chat_service,
        test_queries=test_queries,
        retriever=retriever,
    )
    print(f"✅ Dataset built: {len(dataset.samples)} samples.\n")

    # 4. Run ragas evaluation -----------------------------------------------
    eval_service = EvalService(
        llm=evaluator_llm,
        embeddings=embeddings,
        metrics=FULL_METRICS,
    )

    print("⏳ Running ragas evaluation… (this may take a few minutes)\n")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, eval_service.run, dataset)

    # 5. Print results -------------------------------------------------------
    df = result.to_pandas()

    # Identify metric columns — exclude ragas bookkeeping columns
    non_metric_cols = {
        "user_input", "retrieved_contexts", "response",
        "reference", "reference_contexts", "rubrics",
    }
    metric_cols = [c for c in df.columns if c not in non_metric_cols]

    print("═" * 50)
    print("  RAGAS EVALUATION RESULTS")
    print("═" * 50)
    for metric_name in metric_cols:
        score = df[metric_name].mean()         # mean across all samples
        bar = "█" * int(score * 20)
        print(f"  {metric_name:<35} {score:.4f}  {bar}")
    print("═" * 50)

    # 6. Export to CSV -------------------------------------------------------
    df.to_csv("eval_results.csv", index=False)
    print("\n📄 Detailed results saved to eval_results.csv")


if __name__ == "__main__":
    asyncio.run(main())