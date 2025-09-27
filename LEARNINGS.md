# What I Learnt from this Project

## 1. Purpose
Phase 1 of this project was to build a PDF/Docx Parser MCP Server.\\
The goal being to understand:
- What is MCP?
- How do MCP Servers Work?
- How can I make one?
- How do I test it?


## Testing after writing code for Phase 1

### Testing with CLI

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
- IMP: Check `tests/test_client.py`. The server didn't run till the client sent back an auth after initialization (i.e. it was htrowing an error saying Invalid Message Parameters). Hence the workflow is - send the init request, read the ack, send the `notifications/initialized` message saying that init ack received, and then after that send the rest of the workflow requests.


### Testing with Claude Desktop

- Download Claude Desktop
- Edit the `claude_desktop_config.json` file - Launch Claude -> Settings -> Developer -> Add MCP Server -> It'll open file explorer in the location where the json file is located
    - Contents:
    - ```json
      {
        "mcpServers": {
            "pdf-doc-parser": {
            "command": "/opt/miniconda3/envs/parse_the_docs/bin/python3.12",
            "args": ["/absolute_path_to_project/parse-the-docs/src/pdf_server.py"],
            "cwd": "/absolute_path_to_project/parse-the-docs"
            }
        }
      }
        ```
    - Note that the command was needed since otherwise Claude tries to find the associated packages like `mcp` in the global environment. I wanted it to use the specific conda environment for the project, hence I've explicitly given it the location