from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore

# async def retrive_docs(query: str, retriver: VectorStore) -> list[Document]:
#     """Inject context from the given user query."""
    
#     vector_store = retriver
#     retrieved_docs = vector_store.similarity_search(query, k=3)

#     docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    
#     return docs_content

async def build_retrieval_node(retriever):

    async def retrieve(state):
        question = state["messages"][-1].content

        docs = await retriever.ainvoke(question)

        return {
            "documents": [doc.page_content for doc in docs]
        }

    return retrieve