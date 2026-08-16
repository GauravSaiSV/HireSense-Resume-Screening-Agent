from pathlib import Path

import pymupdf
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from all pages of a PDF file.
    """
    document = pymupdf.open(file_path)

    try:
        text = []

        for page in document:
            page_text = page.get_text()

            if page_text.strip():
                text.append(page_text.strip())

        return "\n".join(text).strip()

    finally:
        document.close()


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from paragraphs in a DOCX file.
    """
    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        paragraph_text = paragraph.text.strip()

        if paragraph_text:
            text.append(paragraph_text)

    return "\n".join(text).strip()


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from a plain text file.
    """
    return Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    ).strip()


def extract_text(file_path: str) -> str:
    """
    Extract text from a supported document.

    Supported formats:
    - PDF
    - DOCX
    - TXT
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".pdf":
        text = extract_text_from_pdf(file_path)

    elif extension == ".docx":
        text = extract_text_from_docx(file_path)

    elif extension == ".txt":
        text = extract_text_from_txt(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            "Supported formats are PDF, DOCX, and TXT."
        )

    if not text:
        raise ValueError(
            f"No extractable text found in document: {file_path}"
        )

    return text