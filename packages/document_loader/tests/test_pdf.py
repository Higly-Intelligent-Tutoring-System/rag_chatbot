import pytest
from langchain_core.documents import Document
from loader.sources.pdf import load_pdf

def test_load_pdf_success(mocker):
    """
    Test that the loader correctly iterates over pages
    and returns a list of Documents.
    """
    # 1. Mock the PyPDFLoader class
    # We patch where it is IMPORTED (loader.sources.pdf), not where it is defined
    mock_loader_class = mocker.patch("loader.sources.pdf.PyPDFLoader")
    
    # 2. Setup the mock instance
    mock_loader_instance = mock_loader_class.return_value
    
    # 3. Setup the lazy_load method to return a dummy list of Documents
    expected_docs = [
        Document(page_content="Page 1 Content", metadata={"page": 1}),
        Document(page_content="Page 2 Content", metadata={"page": 2})
    ]
    mock_loader_instance.lazy_load.return_value = expected_docs

    # 4. Run the function
    result = load_pdf("dummy_path.pdf")

    # 5. Assertions
    assert len(result) == 2
    assert result[0].page_content == "Page 1 Content"
    
    # Verify we initialized the loader with the correct path
    mock_loader_class.assert_called_once_with("dummy_path.pdf")


def test_load_pdf_file_not_found(mocker, capsys):
    """
    Test that the function handles exceptions gracefully
    (returns empty list and prints error).
    """
    # 1. Mock the loader to raise an exception immediately on initialization
    mock_loader_class = mocker.patch("loader.sources.pdf.PyPDFLoader")
    mock_loader_class.side_effect = FileNotFoundError("No such file")

    # 2. Run the function
    result = load_pdf("non_existent.pdf")

    # 3. Assertions
    # It should return an empty list, not crash
    assert result == []

    # Check that it printed the error (using pytest's capsys fixture)
    captured = capsys.readouterr()
    assert "Error laodring" in captured.out # Note: keeping your typo from source code
    assert "No such file" in captured.out


def test_load_pdf_empty_file(mocker):
    """Test behavior when the PDF has no readable pages."""
    mock_loader_class = mocker.patch("loader.sources.pdf.PyPDFLoader")
    mock_loader_instance = mock_loader_class.return_value
    
    # lazy_load returns empty iterator
    mock_loader_instance.lazy_load.return_value = []

    result = load_pdf("empty.pdf")

    assert result == []