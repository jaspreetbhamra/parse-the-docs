# pdf_server_shared.py
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from utils.docx_utils import extract_docx_metadata, extract_docx_text
from utils.embeddings import build_index, semantic_search
from utils.pdf_utils import extract_pdf_metadata, extract_pdf_text

# Keep an in-memory cache to avoid recomputing
doc_cache = {}

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
def parse_text(path: Path | str):
    """Extract raw text from a document."""
    path = get_document_path(path)
    path, ext = resolve_file(path)
    if ext == "pdf":
        return {"text": extract_pdf_text(path)}
    elif ext == "docx":
        return {"text": extract_docx_text(path)}
    else:
        raise ValueError("Unsupported format: " + str(path))


@server.tool()
def parse_metadata(path: Path | str):
    """Extract metadata from a document."""
    path = get_document_path(path)
    path, ext = resolve_file(path)
    if ext == "pdf":
        return {"metadata": extract_pdf_metadata(path)}
    elif ext == "docx":
        return {"metadata": extract_docx_metadata(path)}
    else:
        raise ValueError("Unsupported format: " + str(path))


@server.tool()
def search_in_doc(params: dict):
    """Simple keyword search in a document."""
    file_path = params["path"]
    query = params["query"].lower()

    path, ext = resolve_file(file_path)

    if ext == "pdf":
        text = extract_pdf_text(path)
    elif ext == "docx":
        text = extract_docx_text(path)
    else:
        raise ValueError("Unsupported format")

    # Find matching lines
    results = []
    for i, line in enumerate(text.splitlines()):
        if query in line.lower():
            results.append({"line": i + 1, "snippet": line.strip()})

    # TODO: Update so that the number of results returned is controlled by the user
    return {"matches": results[:10]}  # cap at 10 for readability


@server.tool()
def semantic_search_doc(params: dict):
    """Semantic search using embeddings + FAISS."""
    file_path = params["path"]
    query = params["query"]

    if file_path not in doc_cache:
        path, ext = resolve_file(file_path)

        if ext == "pdf":
            text = extract_pdf_text(path)
        elif ext == "docx":
            text = extract_docx_text(path)
        else:
            raise ValueError("Unsupported format")

        index, lines, embeddings = build_index(text)
        doc_cache[file_path] = (index, lines, embeddings)

    index, lines, embeddings = doc_cache[file_path]
    results = semantic_search(query, index, lines, embeddings, k=5)
    return {"results": results}


if __name__ == "__main__":
    # print("🚀 Starting MCP PDF/Doc Parser server (shared deps)...")
    server.run()
