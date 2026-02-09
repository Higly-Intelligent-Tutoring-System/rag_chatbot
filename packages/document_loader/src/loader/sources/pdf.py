from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(filepath: str) -> list[Document]:
    """Extracts all pages from a given pdf file."""
    pages = []

    try:
        loader = PyPDFLoader(filepath)
        for page in loader.lazy_load():
            page.metadata["type"] = "pdf"
            pages.append(page)
        print(f"✅ Loaded {len(pages)} pages from {filepath}")

    except Exception as e:
            print(f"⚠️ Error laodring {filepath}: {e}")

    return pages