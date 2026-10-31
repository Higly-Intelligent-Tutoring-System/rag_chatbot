from typing import List
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Element

def load_pdf(filepath: str) -> List[Element]:
    """Extracts all pages from a given pdf file."""
    try:
        elements = partition_pdf(
            filename=filepath,
            languages=["ita"],
            strategy="hi_res",  # Vital for structure awareness
            infer_table_structure=True 
        )
        print(f"✅ Successfully parsed {filepath}")
        return elements
    except Exception as e:
        print(f"⚠️ Error fetching {filepath}: {e}")
        return []