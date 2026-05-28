from pathlib import Path

import fitz
from docx import Document


class UnsupportedDocumentTypeError(ValueError):
    pass


def load_document_text(file_path: str | Path) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _load_pdf_text(path)
    if suffix == ".docx":
        return _load_docx_text(path)
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")

    raise UnsupportedDocumentTypeError(f"Unsupported document type: {suffix}")


def _load_pdf_text(path: Path) -> str:
    with fitz.open(path) as document:
        return "\n".join(page.get_text() for page in document)


def _load_docx_text(path: Path) -> str:
    document = Document(path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs)
