import requests_mock
from loader.sources.web import crawl_website


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
            <a href="/">Back to Root</a>
        </main>
    </body>
</html>
"""


def extracted_text(elements):
    return " ".join(element.text for element in elements if element.text)


def test_crawl_single_page(requests_mock):
    base_url = "https://example.com/page1"
    requests_mock.get(
        base_url,
        text=HTML_PAGE_1,
        headers={"content-type": "text/html"},
    )

    elements = crawl_website(base_url, max_pages=1)

    assert elements
    assert "Welcome to Page 1" in extracted_text(elements)
    assert {element.metadata.url for element in elements} == {base_url}


def test_crawl_recursion_and_filtering(requests_mock):
    root_url = "https://example.com/"
    page2_url = "https://example.com/page2"

    requests_mock.get(
        root_url,
        text=HTML_PAGE_1,
        headers={"content-type": "text/html"},
    )
    requests_mock.get(
        page2_url,
        text=HTML_PAGE_2,
        headers={"content-type": "text/html"},
    )
    requests_mock.get(
        "https://google.com",
        text="Ignore me",
        headers={"content-type": "text/html"},
    )

    elements = crawl_website(root_url, max_pages=10)

    sources = {element.metadata.url for element in elements}
    content = extracted_text(elements)

    assert root_url in sources
    assert page2_url in sources
    assert "Welcome to Page 1" in content
    assert "Page 2 Subtitle" in content
    assert "https://google.com" not in sources
    assert all(
        request.url != "https://google.com"
        for request in requests_mock.request_history
    )


def test_crawl_max_pages(requests_mock):
    page1_url = "https://example.com/page1"
    page2_url = "https://example.com/page2"

    requests_mock.get(
        page1_url,
        text=HTML_PAGE_1,
        headers={"content-type": "text/html"},
    )
    requests_mock.get(
        page2_url,
        text=HTML_PAGE_2,
        headers={"content-type": "text/html"},
    )

    elements = crawl_website(page1_url, max_pages=1)

    assert elements
    assert {element.metadata.url for element in elements} == {page1_url}
    assert all(
        request.url != page2_url
        for request in requests_mock.request_history
    )
