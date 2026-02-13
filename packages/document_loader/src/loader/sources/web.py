import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain_core.documents import Document


def clean_webpage(soup):
    """Remove the header and footer elements"""
    for header in soup.find_all('header'):
        header.decompose()
    
    for footer in soup.find_all('footer'):
        footer.decompose()

    return soup


def crawl_website(base_url: str, max_pages: int = 50) -> list[Document]:
    """Recursively crawl and extract text from a website."""
    visited = set()
    to_visit = [base_url]
    docs = []

    print(f"🕷️ Starting crawl on {base_url}")

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited or not url.startswith(base_url):
            continue
        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            if "text/html" not in response.headers.get("content-type", ""):
                continue
            
            soup = clean_webpage(BeautifulSoup(response.text, "html.parser"))
            
            # Simple extraction strategy
            text = ' '.join(p.get_text() for p in soup.find_all(['p', 'li', 'h1', 'h2', 'h3']))
            
            if text.strip():
                docs.append(Document(
                    page_content=text, 
                    metadata={"source": url, "type": "web"}
                ))

            # Find links
            for link_tag in soup.find_all("a", href=True):
                link = urljoin(url, link_tag['href'])
                if link.startswith(base_url) and link not in visited:
                    to_visit.append(link)

            print(f"✅ Successfully parsed {url}")
                    
        except Exception as e:
            print(f"⚠️ Error fetching {url}: {e}")

    return docs
