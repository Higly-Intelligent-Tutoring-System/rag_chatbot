from typing import List
from urllib.parse import urldefrag, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from unstructured.documents.elements import Element
from unstructured.partition.html import partition_html


def crawl_website(base_url: str, max_pages: int = 50) -> List[Element]:
    """Recursively crawl the base URL's site and extract Unstructured elements."""
    base_parts = urlsplit(base_url)
    base_site = (base_parts.scheme, base_parts.netloc)

    visited = set()
    to_visit = [base_url]
    elements_found: List[Element] = []

    print(f"🕷️ Starting crawl on {base_url}")

    while to_visit and len(visited) < max_pages:
        url = urldefrag(to_visit.pop(0))[0]

        if url in visited:
            continue

        page_parts = urlsplit(url)
        if (page_parts.scheme, page_parts.netloc) != base_site:
            continue

        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type.lower():
                continue

            page_elements = partition_html(
                text=response.text,
                languages=["ita"],
            )

            for element in page_elements:
                element.metadata.url = url
                elements_found.append(element)

            print(f"✅ Successfully parsed {url}")

            soup = BeautifulSoup(response.text, "html.parser")
            for link_tag in soup.find_all("a", href=True):
                link = urldefrag(urljoin(url, link_tag["href"]))[0]
                link_parts = urlsplit(link)

                if (
                    (link_parts.scheme, link_parts.netloc) == base_site
                    and link not in visited
                ):
                    to_visit.append(link)

        except Exception as e:
            print(f"⚠️ Error fetching {url}: {e}")

    return elements_found



def clean_webpage(soup):
    """Remove the header and footer elements"""
    for header in soup.find_all('header'):
        header.decompose()
    
    for footer in soup.find_all('footer'):
        footer.decompose()

    return soup