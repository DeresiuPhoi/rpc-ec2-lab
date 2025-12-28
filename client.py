import socket
import json
import uuid
import time

SERVER_IP = "98.92.168.14"  
PORT = 5000

def make_request():
    return {
        "requestid": str(uuid.uuid4()),
        "method": "add",
        "params": {"a": 5, "b": 7},
    }

max_retries = 3
timeout_sec = 2

for attempt in range(1, max_retries + 1):
    req = make_request()
    print(f"\nAttempt {attempt}, requestid={req['requestid']}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_sec)

    try:
        start = time.time()
        sock.connect((SERVER_IP, PORT))
        sock.send(json.dumps(req).encode())
        resp_raw = sock.recv(1024).decode()
        elapsed = time.time() - start

        resp = json.loads(resp_raw)
        print("Response from server:", resp)
        print(f"Round-trip time: {elapsed:.2f} sec")
        break  # success

    except socket.timeout:
        print(f"Timeout after {timeout_sec} sec, will retry...")
    except Exception as e:
        print("Error:", e)
        break
    finally:
        sock.close()
else:
    print("\nAll retries failed. Giving up.")
