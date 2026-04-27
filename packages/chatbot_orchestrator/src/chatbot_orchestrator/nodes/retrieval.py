from langchain_core.vectorstores import VectorStore

# async def retrive_docs(query: str, retriver: VectorStore) -> list[Document]:
#     """Inject context from the given user query."""
    
#     vector_store = retriver
#     retrieved_docs = vector_store.similarity_search(query, k=3)

#     docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    
#     return docs_content


# IMPORTANT: It has to be sync because if not it will return a coroutine, not a callable.
def build_retrieval_node(retriever: VectorStore):

    async def retrieve(state):
        question = state["messages"][-1].content
        docs = retriever.similarity_search(question)
        return {
            "documents": docs
        }

    return retrieve