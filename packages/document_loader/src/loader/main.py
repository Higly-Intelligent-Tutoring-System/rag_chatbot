import sys
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from sources.web import crawl_website
from core import get_vector_store

load_dotenv()

def process_and_store(documents):
    if not documents:
        print("No documents to process.")
        return

    print(f"📚 Processing {len(documents)} raw documents...")

    # 1. Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=int(os.getenv("CHUNK_SIZE")), chunk_overlap=int(os.getenv("CHUNK_OVERLAP")))
    chunks = text_splitter.split_documents(documents) 
    print(f"🧩 Created {len(chunks)} chunks.") 

    # 2. Get DB (Abstracted by core) 
    vector_store = get_vector_store(collection_name="chatbot_knowledge") 
   
    #3. Store 
    print("💾 Uploading to Vector Database...")
    vector_store.add_documents(chunks)
    print("✅ Done!")


def main():
    # Simple CLI arguments to choose mode 
    if len(sys.argv) < 2:
        print("Usage: python main.py [web] [target]")
        return 

    mode = sys.argv[1]
    target = sys.argv[2]
    docs = []

    match mode:
        case "web":
            docs = crawl_website(base_url=target, max_pages=5)
        case _:
            print("Unknown mode. Use 'web'.")


    return process_and_store(docs)


if __name__ == "__main__":
    main()