# 🧠 RAG Core Library

The **core** package is the shared foundation of the RAG Monorepo. It acts as the "Single Source of Truth" for:
1.  **Configuration** (Connection parameters & Environment Variables).
2.  **Infrastructure** (Vector Database Factory).
3.  **AI Models** (Embedding Model definitions).

## 🚨 Important note

If you wish to change the embedding model to experiment new vectorization functions, remember to clean out the current VectorDB as the new embeddings wouldn'd be compatible with the new ones.

Moreover, since this package is shared between the **document_loader** and the **rag_api**, changing the embedding model implies that even if the old embeddings are present, they are very unlikely to be returned with a similarity serach in inference.

The embedding model can be swapped out by editing `config.py` with another one from [HuggingFace](https://huggingface.co/models?other=embedding).


## 🔌 Current connection options

At this moment, the available VecotrDB connections are:

 - ChromaDB locally (chroma_local)
 - ChromaDB as a removte service (chroma_server)
 - Supabase

To use one or another it is sufficient to change the relative parameter inside of `config.py`.

Remember to copy a version of `.env.dist` in `.env` and populate the variables of the desired connection method with the corresponding values to ensure the system's correct working.