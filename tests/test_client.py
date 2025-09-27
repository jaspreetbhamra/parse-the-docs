import json
import subprocess
import sys

# Start the MCP server
proc = subprocess.Popen(
    ["python", "src/pdf_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    bufsize=1,
)


def read_message():
    """Read one JSON message from server stdout."""
    while True:
        line = proc.stdout.readline()
        if not line:
            return None
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            # Ignore anything that's not JSON
            print(f"[STDOUT] {line.strip()}", file=sys.stderr)


def send_message(msg):
    """Send one JSON message to the server."""
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()


# --- Step 1: Initialize ---
init_req = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test-client", "version": "0.1.0"},
    },
}
print("\n➡️ Sending initialize...")
send_message(init_req)

while True:
    msg = read_message()
    if msg is None:
        sys.exit("⚠️ Server closed connection")

    print(f"\n⬅️ SERVER → CLIENT:\n{json.dumps(msg, indent=2)}")

    # If this is the init response, break out
    if msg.get("id") == 1 and "result" in msg:
        break

    # If it's a server request, auto-ack
    if "method" in msg and "id" in msg:
        ack = {"jsonrpc": "2.0", "id": msg["id"], "result": None}
        send_message(ack)


post_init_msg = {"jsonrpc": "2.0", "method": "notifications/initialized"}
print("\n➡️ Sending initialized notification...")
send_message(post_init_msg)


# --- Step 2: List tools ---
list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
print("\n➡️ Sending tools/list...")
send_message(list_req)

msg = read_message()
print(f"\n⬅️ TOOLS LIST:\n{json.dumps(msg, indent=2)}")

# --- Step 3: Call list_documents ---
call_req = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "list_documents",
        "arguments": {"path": "./data/documents"},
    },
}
print("\n➡️ Calling list_documents...")
send_message(call_req)

msg = read_message()
print(f"\n⬅️ TOOL CALL RESPONSE:\n{json.dumps(msg, indent=2)}")
