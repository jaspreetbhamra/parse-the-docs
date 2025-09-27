import json
import subprocess
import sys
from pprint import pprint

proc = subprocess.Popen(
    ["python", "src/pdf_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    bufsize=1,
)


def send(req, expect_id=None):
    """Send one JSON-RPC request and wait for the matching response.
    If server sends its own requests, respond minimally so init completes.
    """
    line = json.dumps(req)
    proc.stdin.write(line + "\n")
    proc.stdin.flush()

    while True:
        resp_line = proc.stdout.readline()
        if not resp_line:
            print("⚠️ No response received", file=sys.stderr)
            return None
        try:
            msg = json.loads(resp_line)
        except json.JSONDecodeError:
            continue  # ignore junk lines

        # Case 1: It's the response we wanted
        if expect_id is None or msg.get("id") == expect_id:
            return msg

        # Case 2: It's a request from the server → send minimal result
        if "method" in msg and "id" in msg:
            ack = {"jsonrpc": "2.0", "id": msg["id"], "result": None}
            proc.stdin.write(json.dumps(ack) + "\n")
            proc.stdin.flush()


# 1. Initialize
init_req = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "cli", "version": "0.1.0"},
    },
}
print("\n➡️ Sending initialize...")
init_resp = send(init_req, expect_id=1)
print("⬅️ INIT response:")
pprint(init_resp)

# 2. List tools
list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
print("\n➡️ Sending tools/list...")
tools_list = send(list_req, expect_id=2)
print("⬅️ TOOLS LIST response:")
pprint(tools_list)

# 3. Call the tool
call_req = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "list_documents",
        "arguments": {"path": "./data/documents"},
    },
}
print("\n➡️ Sending tools/call (list_documents)...")
call_resp = send(call_req, expect_id=3)
print("⬅️ TOOL CALL response:")
pprint(call_resp)
