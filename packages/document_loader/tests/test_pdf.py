from unstructured.documents.elements import NarrativeText, Title

from loader.sources.pdf import load_pdf


def test_load_pdf_success(mocker):
    partition_mock = mocker.patch("loader.sources.pdf.partition_pdf")
    expected_elements = [
        Title(text="Page title"),
        NarrativeText(text="Page content"),
    ]
    partition_mock.return_value = expected_elements

    result = load_pdf("dummy_path.pdf")

    assert result is expected_elements
    assert result[0].text == "Page title"
    assert result[1].text == "Page content"
    partition_mock.assert_called_once_with(
        filename="dummy_path.pdf",
        languages=["ita"],
        strategy="hi_res",
        infer_table_structure=True,
    )


def test_load_pdf_file_not_found(mocker, capsys):
    partition_mock = mocker.patch("loader.sources.pdf.partition_pdf")
    partition_mock.side_effect = FileNotFoundError("No such file")

    result = load_pdf("non_existent.pdf")
    
    assert result == []

    output = capsys.readouterr().out
    assert "Error fetching non_existent.pdf" in output
    assert "No such file" in output


def test_load_pdf_empty_file(mocker):
    partition_mock = mocker.patch("loader.sources.pdf.partition_pdf")
    partition_mock.return_value = []

    result = load_pdf("empty.pdf")

    assert result == []
    partition_mock.assert_called_once()
