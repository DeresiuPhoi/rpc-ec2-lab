import socket
import json
import time

HOST = "0.0.0.0"
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print("RPC server listening on port 5000...")

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")
    try:
        raw = conn.recv(1024)
        if not raw:
            conn.close()
            continue

        # Handle garbage / non-UTF8 traffic gracefully
        try:
            data = raw.decode("utf-8")
        except UnicodeDecodeError:
            print("Received non-UTF8 data, ignoring.")
            conn.close()
            continue

        req = json.loads(data)
        print(f"Request ID: {req['requestid']}, method: {req['method']}")

        # Simulate slow server for failure demo (uncomment during video)
        # time.sleep(4)

        if req["method"] == "add":
            a = req["params"]["a"]
            b = req["params"]["b"]
            result = a + b
            status = "OK"
        else:
            result = "Unknown method"
            status = "ERROR"

        resp = {
            "requestid": req["requestid"],
            "result": result,
            "status": status,
        }
        conn.send(json.dumps(resp).encode())

    except Exception as e:
        print("Error while handling connection:", e)
    finally:
        conn.close()
