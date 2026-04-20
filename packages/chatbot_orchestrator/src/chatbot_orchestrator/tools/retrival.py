# TODO: Add tool to wire to the HITS graph to retrive documents.
from langchain_core.vectorstores import VectorStore
from langchain.tools import tool

@tool
def search_vectordb(retriever: VectorStore, query: str) -> str:
    """Search the vecotr database for information about a the user's query."""
    docs = retriever.similarity_search(query)
    return {
        "documents": docs
    }