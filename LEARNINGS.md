# What I Learnt from this Project

## 1. Purpose
Phase 1 of this project was to build a PDF/Docx Parser MCP Server.\\
The goal being to understand:
- What is MCP?
- How do MCP Servers Work?
- How can I make one?
- How do I test it?


## Testing after writing code for Phase 1

```bash
echo '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_documents",
    "arguments": {"path": "./data/documents"}
  }
}' | python src/pdf_server.py

```

- The above assumes that my documents are located in ./data/documents
- This is how a json request can be made to the server - `JSON-RPC 2.0`
- In order to make this more user friendly, Claude Desktop can be used (outlined below)
- There are multiple methods that can be used in the request (cheat sheet below)
- `name` in the above request maps to the `list_documents` function in the server script being called i.e. `pdf_server.py`
