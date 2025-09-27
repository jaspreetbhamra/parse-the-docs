# pdf_server_shared.py
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from utils.pdf_utils import extract_pdf_text, extract_pdf_metadata
from utils.docx_utils import extract_docx_text, extract_docx_metadata

server = FastMCP("pdf-doc-parser", "0.1.0")


# ✅ Shared dependency
def get_document_path(path: Path | str = Path(".")) -> Path:
    """Resolve and validate a document path."""
    path_obj = Path(path)
    if not path_obj.exists():
        raise ValueError(f"Path does not exist: {path_obj}")
    return path_obj


@server.tool()
def list_documents(path: Path | str = Path(".")):
    """List all supported PDF/DOCX files in a folder."""
    folder = get_document_path(path)
    files = [
        entry.name
        for entry in folder.iterdir()
        if entry.is_file() and entry.suffix.lower() in {".pdf", ".docx"}
    ]
    return {"documents": files}


def resolve_file(path: Path | str | os.PathLike[str]) -> tuple[Path, str]:
    path_obj = get_document_path(path)
    ext = path_obj.suffix.lower()
    if ext == ".pdf":
        return path_obj, "pdf"
    elif ext == ".docx":
        return path_obj, "docx"
    else:
        raise ValueError("Unsupported format: " + str(path_obj))


@server.tool()
def parse_text(path: Path | str = get_document_path()):
    """Extract raw text from a document."""
    path, ext = resolve_file(path)
    if ext == "pdf":
        return {"text": extract_pdf_text(path)}
    elif ext == "docx":
        return {"text": extract_docx_text(path)}
    else:
        raise ValueError("Unsupported format: " + str(path))


@server.tool()
def parse_metadata(path: Path | str = get_document_path()):
    """Extract metadata from a document."""
    path, ext = resolve_file(path)
    if ext == "pdf":
        return {"metadata": extract_pdf_metadata(path)}
    elif ext == "docx":
        return {"metadata": extract_docx_metadata(path)}
    else:
        raise ValueError("Unsupported format: " + str(path))


if __name__ == "__main__":
    # print("🚀 Starting MCP PDF/Doc Parser server (shared deps)...")
    server.run()
