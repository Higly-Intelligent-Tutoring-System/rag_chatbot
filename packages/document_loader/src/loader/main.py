import sys
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader.config import *
from loader.sources.web import crawl_website
from loader.sources.pdf import load_pdf
from core import get_vector_store


def process_and_store(documents):
    if not documents:
        print("No documents to process.")
        return

    print(f"📚 Processing {len(documents)} raw documents...")

    # 1. Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents) 
    print(f"🧩 Created {len(chunks)} chunks.") 

    # 2. Get DB (Abstracted by core) 
    vector_store = get_vector_store(collection_name="chatbot_knowledge")
    print(f"✅ Vector Database loaded succesfully!")
   
    #3. Store 
    print(f"💾 Uploading to Vector Database...")
    vector_store.add_documents(chunks)
    print(f"✅ Done!")


def main():
    # Simple CLI arguments to choose mode 
    if len(sys.argv) < 2:
        print("Usage: python main.py [ web | pdf ] [target]")
        return 

    mode = sys.argv[1]
    target = sys.argv[2]
    docs = []

    match mode:
        case "web":
            docs = crawl_website(base_url=target, max_pages=MAX_PAGES_RECURSION)
        case "pdf":
            docs = load_pdf(filepath=target)
        case _:
            print("Unknown mode. Use 'web'.")


    return process_and_store(docs)


if __name__ == "__main__":
    main()