import asyncio
from typing import List
import warnings
from ragas import evaluate, EvaluationDataset, experiment
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig
from ragas.metrics.base import MetricWithLLM, MetricWithEmbeddings


class EvalService:
    def __init__(
        self,
        llm,           # LangChain chat model (e.g. ChatOpenAI)
        embeddings,    # LangChain embeddings (e.g. OpenAIEmbeddings)
        metrics: List,
        run_config: RunConfig = None,
    ):
        self.evaluator_llm = LangchainLLMWrapper(llm)
        self.evaluator_emb = LangchainEmbeddingsWrapper(embeddings)
        self.metrics = metrics
        self.run_config = run_config or RunConfig(max_workers=4, timeout=120)

        # inject LLM / embeddings into every metric that needs them
        self._init_metrics()

    def _init_metrics(self):
        for metric in self.metrics:
            if isinstance(metric, MetricWithLLM):
                metric.llm = self.evaluator_llm
            if isinstance(metric, MetricWithEmbeddings):
                metric.embeddings = self.evaluator_emb
            metric.init(self.run_config)

    def _run_coroutine_in_thread(self, coro):
        """
        Run an async coroutine safely from a non-async context (e.g. a thread
        spawned by run_in_executor). Creates a fresh event loop for this thread
        so there is no conflict with the outer asyncio.run() loop.
        """
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    async def _run_with_experiment(self, dataset: EvaluationDataset):
        """Use the new @experiment decorator API (async)."""
        from ragas.experiment import experiment  # noqa: PLC0415

        metrics = self.metrics
        llm = self.evaluator_llm
        embeddings = self.evaluator_emb
        run_config = self.run_config

        @experiment(name=self.experiment_name)
        def scoring_fn(sample):
            scores = {}
            for metric in metrics:
                try:
                    scores[metric.name] = metric.score(sample)
                except Exception as e:
                    scores[metric.name] = float("nan")
                    print(f"⚠️  Metric '{metric.name}' failed: {e}")
            return scores

        # The decorated function is async — await it properly
        result = await scoring_fn(
            dataset=dataset,
            llm=llm,
            embeddings=embeddings,
            run_config=run_config,
        )
        return result

    def _run_with_evaluate_fallback(self, dataset: EvaluationDataset):
        """Fall back to ragas.evaluate() with deprecation warning suppressed."""
        from ragas import evaluate  # noqa: PLC0415

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            return evaluate(
                dataset=dataset,
                metrics=self.metrics,
                llm=self.evaluator_llm,
                embeddings=self.evaluator_emb,
                run_config=self.run_config,
            )

    def run(self, dataset: EvaluationDataset):
        """
        Synchronous entry point — safe to call from run_in_executor.

        Tries the new @experiment API first; falls back to evaluate() if the
        API is not yet available or incompatible. In both cases a fresh event
        loop is created inside this thread so there is no conflict with the
        outer asyncio loop.
        """
        try:
            return self._run_coroutine_in_thread(
                self._run_with_experiment(dataset)
            )
        except (ImportError, AttributeError, TypeError) as e:
            warnings.warn(
                f"ragas @experiment decorator unavailable ({e}); "
                "falling back to ragas.evaluate(). "
                "Upgrade ragas when the new API is stable.",
                UserWarning,
                stacklevel=2,
            )
            return self._run_with_evaluate_fallback(dataset)