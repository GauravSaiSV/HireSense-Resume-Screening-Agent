from pathlib import Path

import pytest

from src.parser import extract_text


RESUME_DIR = Path("data/resumes")


def test_extract_text_from_txt():
    text = extract_text(str(RESUME_DIR / "test_resume.txt"))

    assert "Gaurav Sharma" in text
    assert "Python" in text
    assert "Machine Learning" in text


def test_extract_text_from_docx():
    text = extract_text(str(RESUME_DIR / "test_resume.docx"))

    assert "Gaurav Sharma" in text
    assert "Python" in text
    assert "Machine Learning" in text


def test_extract_text_from_pdf():
    text = extract_text(str(RESUME_DIR / "test_resume.pdf"))

    assert "Gaurav Sharma" in text
    assert "Python" in text
    assert "Machine Learning" in text


def test_empty_document_raises_error(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="No extractable text"):
        extract_text(str(empty_file))


def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        extract_text(str(RESUME_DIR / "does_not_exist.txt"))


def test_unsupported_file_format_raises_error(tmp_path):
    unsupported_file = tmp_path / "resume.csv"

    unsupported_file.write_text(
        "name,skills\nGaurav,Python",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Unsupported file format"):
        extract_text(str(unsupported_file))