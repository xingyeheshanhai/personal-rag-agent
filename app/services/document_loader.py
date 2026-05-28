from dataclasses import dataclass
from pathlib import Path

import fitz
from docx import Document


class UnsupportedDocumentTypeError(ValueError):
    pass


@dataclass(frozen=True)
class DocumentPage:
    page_number: int
    text: str


def load_document_pages(file_path: str | Path) -> list[DocumentPage]:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _load_pdf_pages(path)
    if suffix == ".docx":
        return [DocumentPage(page_number=1, text=_load_docx_text(path))]
    if suffix in {".txt", ".md", ".markdown"}:
        return [DocumentPage(page_number=1, text=path.read_text(encoding="utf-8"))]

    raise UnsupportedDocumentTypeError(f"Unsupported document type: {suffix}")


def load_document_text(file_path: str | Path) -> str:
    return "\n".join(page.text for page in load_document_pages(file_path))


def _load_pdf_pages(path: Path) -> list[DocumentPage]:
    with fitz.open(path) as document:
        return [
            DocumentPage(page_number=index + 1, text=page.get_text())
            for index, page in enumerate(document)
        ]


def _load_docx_text(path: Path) -> str:
    document = Document(path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs)
