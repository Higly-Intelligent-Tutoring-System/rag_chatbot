import sys
import os
from itertools import batched
from typing import List
from unstructured.chunking.title import chunk_by_title
from langchain_core.documents import Document
from loader.config import *
from loader.sources.web import crawl_website
from loader.sources.pdf import load_pdf
from core import get_vector_store
from .config import core_settings, document_loader_settings


def clean_metadata(chunk):
    """Cleans metadata from unstructured chunks (chromaDB specific)"""
    raw_metadata = chunk.metadata.to_dict()
    cleaned_metadata = {
        k: v for k, v in raw_metadata.items() 
        if isinstance(v, (str, int, float, bool)) or v is None
    }
    return cleaned_metadata


def process_and_store(elements_list):
    """
    Takes structural elements, chunks them smartly, 
    converts to LangChain format, and stores in Chroma.
    """
    if not elements_list:
        print("No documents to process.")
        return
    
    docs = []

    for elements in elements_list:
        print(f"📚 Processing {len(elements)} raw documents...")

        # 1. Split
        chunks = chunk_by_title(
            elements=elements,
            max_characters=1000,          # Optimized for your Italian BERT (512 tokens)
            new_after_n_chars=800,
            combine_text_under_n_chars=250,
            overlap=100,
            multipage_sections=True
        )
        print(f"🧩 Created {len(chunks)} chunks.")

        # 2 Convert to langchain Documents
        for chunk in chunks:
            metadata = clean_metadata(chunk) 

            # Context Enrichment (Optional but recommended)
            source = metadata.get("filename", "WebPage")
            content = f"[Fonte: {source}] {chunk.text}"

            docs.append(Document(
                page_content=content,
                metadata=metadata
                ))

    # 3. Get DB (Abstracted by core) 
    vector_store = get_vector_store(core_settings)
    print(f"✅ Vector Database loaded succesfully!")
   
    # 4. Store 
    print(f"💾 Uploading to Vector Database...")
    list(map(vector_store.add_documents, batched(docs, document_loader_settings.BATCH_SIZE)))
    print(f"✅ Done!")


def main():
    # Simple CLI arguments to choose mode 
    if len(sys.argv) < 2:
        print("Usage: python main.py [ web | pdf ] [target]")
        return 

    mode = sys.argv[1]
    target = sys.argv[2]
    elements = []

    match mode:
        case "web":
            elements = crawl_website(
                base_url=target, 
                max_pages=document_loader_settings.MAX_PAGES_RECURSION
                )
        case "pdf":
            elements = load_pdf(filepath=target)
        case _:
            print("Unknown mode. Use 'web' or 'pdf'.")


    return process_and_store(List(elements))


if __name__ == "__main__":
    main()