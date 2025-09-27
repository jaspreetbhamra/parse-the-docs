from pathlib import Path

from PyPDF2 import PdfReader


def extract_pdf_text(file_path: Path | str) -> str:
    path = Path(file_path)
    reader = PdfReader(str(path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_pdf_metadata(file_path: Path | str) -> dict:
    path = Path(file_path)
    reader = PdfReader(str(path))
    meta = reader.metadata
    return {
        "title": meta.title if meta else None,
        "author": meta.author if meta else None,
        "pages": len(reader.pages),
    }
