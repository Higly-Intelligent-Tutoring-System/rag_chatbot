from __future__ import annotations

from langchain.messages import HumanMessage
import pytest

from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from chatbot_orchestrator.graphs.rag_graph import RAGGraphBuilder


@pytest.fixture
def compiled_graph(fake_retriever, fake_generation_llm):
    """Build and compile the RAG graph with all fakes."""
    graph_builder = RAGGraphBuilder(
        retriever=fake_retriever,
        llm=fake_generation_llm,
    )

    builder = graph_builder.build()
    return builder.compile(
        checkpointer=MemorySaver(),
        store=InMemoryStore(),
    )


class TestRAGGraph:

    def test_graph_has_correct_name(self):
        graph = RAGGraphBuilder()
        assert graph.name == "BasicRagGraph"

    def test_graph_builds_without_error(
        self, fake_retriever, fake_generation_llm
    ):
        graph = RAGGraphBuilder(
            retriever=fake_retriever,
            llm=fake_generation_llm,
        )
        builder = graph.build()

        # Should compile without errors
        compiled = builder.compile(checkpointer=MemorySaver())
        assert compiled is not None

    @pytest.mark.asyncio
    async def test_single_turn(self, compiled_graph):
        """A single message should produce a response."""
        config = {"configurable": {"thread_id": "test-1", "user_id": "u1"}}

        result = await compiled_graph.ainvoke(
            {"messages": [HumanMessage(content="What is Python?")]},
            config=config,
        )

        assert len(result["messages"]) == 2  # Human + AI
        assert result["messages"][0].content == "What is Python?"
        assert len(result["messages"][1].content) > 0