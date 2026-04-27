from typing import List
from unstructured.partition.html import partition_html
from unstructured.documents.elements import Element


def clean_webpage(soup):
    """Remove the header and footer elements"""
    for header in soup.find_all('header'):
        header.decompose()
    
    for footer in soup.find_all('footer'):
        footer.decompose()

    return soup


def crawl_website(base_url: str, max_pages: int = 50) -> List[Element]:
    """Recursively crawl and extract text from a website."""
    try:
        elements = partition_html(
            url=base_url,
            languages=["ita"]
        )
        print(f"✅ Successfully parsed {base_url}")
                
    except Exception as e:
        print(f"⚠️ Error fetching {base_url}: {e}")

    return elements
