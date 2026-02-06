import pytest
import requests_mock
from loader.sources.web import crawl_website

# Fake HTML content
HTML_PAGE_1 = """
<html>
    <body>
        <main>
            <h1>Welcome to Page 1</h1>
            <p>This is the main content.</p>
            <a href="/page2">Go to Page 2</a>
            <a href="https://google.com">External Link</a>
        </main>
    </body>
</html>
"""

HTML_PAGE_2 = """
<html>
    <body>
        <main>
            <h2>Page 2 Subtitle</h2>
            <p>This is the content of page 2.</p>
            <a href="/..">Back to Root</a>
        </main>
    </body>
</html>
"""

def test_crawl_single_page(requests_mock):
    """Test basic extraction of a single page"""
    base_url = "https://example.com/page1"
    
    # Mock the network call
    requests_mock.get(base_url, text=HTML_PAGE_1, headers={"content-type": "text/html"})

    # Run crawler
    docs = crawl_website(base_url, max_pages=1)

    assert len(docs) == 1
    assert "Welcome to Page 1" in docs[0].page_content
    assert docs[0].metadata["source"] == base_url
    assert docs[0].metadata["type"] == "web"

def test_crawl_recursion_and_filtering(requests_mock):
    """
    Test that the crawler:
    1. Follows internal links (Root -> Page 2)
    2. Ignores external links (Google)
    3. Handles loops (Page 2 -> Root) without crashing
    """
    base_url = "https://example.com"
    
    # Register multiple URLs
    requests_mock.get("https://example.com/", text=HTML_PAGE_1, headers={"content-type": "text/html"})
    requests_mock.get("https://example.com/page2", text=HTML_PAGE_2, headers={"content-type": "text/html"})
    requests_mock.get("https://google.com", text="Ignore me", headers={"content-type": "text/html"})

    # Run crawler starting at Page 1
    docs = crawl_website("https://example.com/", max_pages=10)

    # Should find Page 1 AND Page 2
    assert len(docs) == 2
    
    # Verify content
    sources = [d.metadata["source"] for d in docs]
    assert "https://example.com/" in sources
    assert "https://example.com/page2" in sources
    
    # Verify it did NOT add google.com
    assert "https://google.com" not in sources

def test_crawl_max_pages(requests_mock):
    """Test that max_pages stops the recursion"""
    requests_mock.get("https://example.com/page1", text=HTML_PAGE_1, headers={"content-type": "text/html"})
    requests_mock.get("https://example.com/page2", text=HTML_PAGE_2, headers={"content-type": "text/html"})

    # Limit to 1 page
    docs = crawl_website("https://example.com/page1", max_pages=1)

    assert len(docs) == 1
    assert docs[0].metadata["source"] == "https://example.com/page1"