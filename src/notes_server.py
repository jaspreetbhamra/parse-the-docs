from mcp.server.fastmcp import FastMCP

from utils.notes_utils import add_note, delete_note, list_notes, search_notes

server = FastMCP("pdf-doc-parser", "0.1.0")


@server.tool()
def save_note(params: dict):
    """Save a new note."""
    text = params["text"]
    return {"note": add_note(text)}


@server.tool()
def list_all_notes(params: dict = None):
    """List all saved notes."""
    return {"notes": list_notes()}


@server.tool()
def search_in_notes(params: dict):
    """Search for notes containing a keyword."""
    query = params["query"]
    return {"matches": search_notes(query)}


@server.tool()
def delete_note_by_id(params: dict):
    """Delete a note by its ID."""
    note_id = int(params["id"])
    success = delete_note(note_id)
    return {"deleted": success}


if __name__ == "__main__":
    print("🚀 Starting Notes MCP server...")
    server.run()
