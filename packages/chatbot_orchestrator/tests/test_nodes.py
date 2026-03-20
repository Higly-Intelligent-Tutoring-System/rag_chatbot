from __future__ import annotations

import pytest
from langchain_core.messages import HumanMessage

from chatbot_orchestrator.nodes.retrieval import build_retrieval_node
from chatbot_orchestrator.nodes.generation import build_generation_node


# ════════════════════════════════════════════════════════
#  RETRIEVE NODE
# ════════════════════════════════════════════════════════

class TestRetrieveNode:
    """Test the retrieve node factory."""

    @pytest.mark.asyncio
    async def test_first_turn(
        self, fake_retriever, fake_docs
    ):
        """First message → no history → query used as-is, no LLM call."""
        retrieve = build_retrieval_node(
            retriever=fake_retriever,
        )

        state = {
            "messages": [HumanMessage(content="What is Python?")],
        }

        result = await retrieve(state)

        # Should return the fake docs
        assert len(result["documents"]) == len(fake_docs)
        assert result["documents"][0] == fake_docs[0]

    @pytest.mark.asyncio
    async def test_empty_retrieval(
        self, empty_retriever
    ):
        """Retriever returns no docs → documents list is empty."""
        retrieve = build_retrieval_node(
            retriever=empty_retriever,
        )

        state = {
            "messages": [HumanMessage(content="What is Zylox?")],
        }

        result = await retrieve(state)

        assert result["documents"] == []


# ════════════════════════════════════════════════════════
#  GENERATE NODE
# ════════════════════════════════════════════════════════

class TestGenerateNode:
    """Test the generate node factory."""

    @pytest.mark.asyncio
    async def test_generates_response_with_context(
        self, fake_generation_llm, fake_docs, fake_system_prompt
    ):
        """Generate node should produce a response and wrap it in messages."""
        generate = build_generation_node(
            llm=fake_generation_llm,
            prompt=fake_system_prompt,
        )

        state = {
            "messages": [HumanMessage(content="What is Python?")],
            "documents": fake_docs,
        }

        result = await generate(state)

        assert "messages" in result
        assert len(result["messages"]) == 1

        ai_message = result["messages"][0]
        assert "Python" in ai_message.content
        assert "Guido" in ai_message.content

    @pytest.mark.asyncio
    async def test_generates_with_no_documents(
        self, fake_generation_llm, fake_system_prompt
    ):
        """When no docs retrieved, should still produce a response."""
        generate = build_generation_node(
            llm=fake_generation_llm,
            prompt=fake_system_prompt,
        )

        state = {
            "messages": [HumanMessage(content="What is Zylox?")],
            "documents": [],
        }

        result = await generate(state)

        assert "messages" in result
        assert len(result["messages"]) == 1