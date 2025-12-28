# rpc-ec2-lab
# Simple RPC over TCP on AWS EC2

This project implements a minimal RPC system using two Amazon EC2 instances (server and client). The server exposes a remote `add(a, b)` function over TCP port 5000, and the client calls it using a simple JSON-based protocol.

## Architecture

- **Server instance** (Amazon Linux / Python 3)
  - Listens on `0.0.0.0:5000`
  - Accepts JSON requests:
    ```
    {
      "requestid": "<uuid>",
      "method": "add",
      "params": {"a": 5, "b": 7}
    }
    ```
  - Returns JSON responses:
    ```
    {
      "requestid": "<same uuid>",
      "result": 12,
      "status": "OK"
    }
    ```
  - Handles invalid / non-UTF8 data without crashing.

- **Client instance**
  - Sends requests with unique `requestid` values.
  - Uses a 2 second timeout and up to 3 retries.
  - Prints the server response or a failure message.

## How to run
Install Python (Amazon Linux)
sudo dnf update -y
sudo dnf install python3 python3-pip -y

Copy server.py to the instance, then:
python3 server.py

Output: "RPC server listening on port 5000..."

Make sure the EC2 security group for the server allows:

- SSH: TCP 22 from your IP
- Custom TCP: port 5000 from 0.0.0.0/0
- (Optional) ICMP for ping
### Client (on client EC2)
Install Python
sudo dnf update -y
sudo dnf install python3 python3-pip -y

Edit client.py and set SERVER_IP to the server's public IPv4
python3 client.py

Example output:

Attempt 1, requestid=...
Response from server: {'requestid': '...', 'result': 12, 'status': 'OK'}

With the artificial delay enabled on the server you can see:

Attempt 1, requestid=...
Timeout after 2 sec, will retry...
Attempt 2, requestid=...
...

## RPC semantics

Because the client retries on timeout, the same logical operation (`add(a, b)`) may be executed more than once if responses are lost or delayed. This implementation therefore provides **at-least-once** semantics. For idempotent operations like `add(5, 7)` this is safe; for non-idempotent operations (e.g., charging a credit card) you would need extra logic (such as a server-side request log) to implement **at-most-once** semantics.



### Server (on server EC2)

