import os
from pathlib import Path
from langchain_core.documents import Document
from unstructured.documents.elements import Element

from .main import process_and_store
from .sources.web import crawl_website
from .sources.pdf import load_pdf
from .config import document_loader_settings

def run_web_batch(list_file_path) -> list[list[Element]]:
    """Reads a text file of URLs and processes them one by one."""
    if not os.path.exists(list_file_path):
        print(f"❌ File not found: {list_file_path}")
        return

    print(f"📋 Reading URLs from: {list_file_path}")
    
    with open(list_file_path, "r") as f:
        # Read non-empty lines
        urls = [line.strip() for line in f if line.strip()]

    print(f"🚀 Found {len(urls)} URLs. Starting batch job...")
    all_website_element_sets = []

    for i, url in enumerate(urls, 1):
        print(f"\n--- [Web {i}/{len(urls)}] Processing: {url} ---")
        try:
            elements = crawl_website(
                base_url=url, 
                max_pages=document_loader_settings.MAX_PAGES_RECURSION
                )
            all_website_element_sets.append(elements)
        except Exception as e:
            print(f"⚠️ Failed to process URL {url}: {e}")
            # We continue to the next one, don't crash the whole batch

    return all_website_element_sets


def run_pdf_batch(folder_path) -> list[list[Element]]:
    """Scans a folder for .pdf files and processes them one by one."""
    path_obj = Path(folder_path)
    
    if not path_obj.exists() or not path_obj.is_dir():
        print(f"❌ Folder not found or is not a directory: {folder_path}")
        return

    # Find all PDFs
    pdf_files = list(path_obj.glob("*.pdf"))
    
    if not pdf_files:
        print("⚠️ No .pdf files found in this folder.")
        return

    print(f"🚀 Found {len(pdf_files)} PDF files. Starting batch job...")
    all_document_element_sets = []

    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n--- [PDF {i}/{len(pdf_files)}] Processing: {pdf_file.name} ---")
        try:
            elements = load_pdf(filepath=str(pdf_file))
            all_document_element_sets.append(elements)
        except Exception as e:
            print(f"⚠️ Failed to process PDF {pdf_file.name}: {e}")

    return all_document_element_sets


def main():
    process_and_store(
        run_web_batch(document_loader_settings.URL_PATH) +
        run_pdf_batch(document_loader_settings.PDF_PATH)
    )


if __name__ == "__main__":
    main()