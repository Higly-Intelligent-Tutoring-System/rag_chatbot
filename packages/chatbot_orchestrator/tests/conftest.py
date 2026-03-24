from __future__ import annotations

import pytest

from langchain_core.documents import Document
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.prompts import ChatPromptTemplate


# ════════════════════════════════════════════════════════
#  Fake retriever — returns canned documents
# ════════════════════════════════════════════════════════

class FakeVectorStore:
    """Vector store that always returns the same documents."""

    def __init__(self, docs: list[Document]):
        self.docs = docs

    def similarity_search(self, query: str, k: int = 4) -> list[Document]:
        return self.docs[:k]


@pytest.fixture
def fake_docs() -> list[Document]:
    return [
        Document(
            page_content="Python is a programming language created by Guido van Rossum.",
            metadata={"source": "wiki"},
        ),
        Document(
            page_content="Python supports multiple programming paradigms.",
            metadata={"source": "docs"},
        ),
        Document(
            page_content="The moon is very beautiful tonight.",
            metadata={"source": "anime"},
        ),
        Document(
            page_content="I have seen things that you humans would not be able to imagine.",
            metadata={"source": "movie"},
        ),
        Document(
            page_content="At the end, the winner is still the last man standing.",
            metadata={"source": "manga"},
        ),
        Document(
            page_content="It will be embarassig the next time we'll meet.",
            metadata={"source": "anime"},
        ),
    ]


@pytest.fixture
def fake_vectorstore(fake_docs):
    return FakeVectorStore(fake_docs)


@pytest.fixture
def empty_vectorstore():
    return FakeVectorStore([])

# ════════════════════════════════════════════════════════
#  Fake LLM — returns pre-defined responses in order
# ════════════════════════════════════════════════════════

@pytest.fixture
def fake_generation_llm() -> FakeListChatModel:
    """LLM for the generate node — returns a canned answer."""
    return FakeListChatModel(
        responses=[
            "Python is a programming language created by Guido van Rossum. "
            "It supports multiple paradigms."
        ]
    )

# ════════════════════════════════════════════════════════
#  Prompts for testing
# ════════════════════════════════════════════════════════

@pytest.fixture
def fake_system_prompt() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "Context:\n{context}\n\nQuestion:\n{question}")
        ])
    return prompt