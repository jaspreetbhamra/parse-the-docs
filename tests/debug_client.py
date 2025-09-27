import json
import subprocess
import sys

# Start your MCP server subprocess
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
            msg = json.loads(line)
            return msg
        except json.JSONDecodeError:
            # Ignore non-JSON output (or log it separately)
            print(f"[STDOUT] {line.strip()}", file=sys.stderr)


def send_message(msg: dict):
    """Send one JSON message to the server."""
    line = json.dumps(msg)
    print(f"\n➡️ CLIENT → SERVER:\n{json.dumps(msg, indent=2)}")
    proc.stdin.write(line + "\n")
    proc.stdin.flush()


def respond_to_server(req: dict):
    """Auto-respond to server-initiated requests with dummy result."""
    ack = {"jsonrpc": "2.0", "id": req["id"], "result": None}
    print(f"\n↩️ AUTO-ACK to SERVER request:\n{json.dumps(ack, indent=2)}")
    proc.stdin.write(json.dumps(ack) + "\n")
    proc.stdin.flush()


# --- Bootstrap sequence ---
# 1. Send initialize
init_req = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "debug-client", "version": "0.1.0"},
    },
}
send_message(init_req)

# 2. Enter read loop
while True:
    msg = read_message()
    if msg is None:
        print("⚠️ Server closed connection")
        break

    print(f"\n⬅️ SERVER → CLIENT:\n{json.dumps(msg, indent=2)}")

    # If it's a server request, send back a dummy result
    if "method" in msg and "id" in msg:
        respond_to_server(msg)

    # If it's a response, pretty print only
    if "id" in msg and "result" in msg:
        print(f"[Result for id={msg['id']}]")
