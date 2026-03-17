# FastAPI Rate Limiter
A FastAPI rate limiter is a mechanism used to control the number of requests a client (i.e user or IP address) can make to a FastAPI application within a specific time period.

When the limit exceeded, algorithm automatically returns '429 Too Many Requests' error and after certain amount of time it will refresh.

---

## Project Structure

```text
.
├── example.env
├── pyproject.toml
├── README.md
└── src
    ├── main.py
    ├── classes
    │   ├── Counter.py
    │   ├── Settings.py
    │   └── Status.py
    ├── config
    │   └── constants.py
    ├── tests
    │   └── test_api.py
    └── utils
        ├── db_connection.py
        └── dependencies.py
```

---

## Setup and Installation

Prerequisites
 - Python 3.8+
 - FastAPI
 - SQLite3

Installation

```bash
# clone the repository

git clone <your_repository-url>
cd <your-repo>
```

Running the server

```bash
uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

The server starts at `http://127.0.0.1:8000`

---

## API endpoints

`get/` - rate limited (protected route) endpoint which returns a greeting with client-ip

Response (200 OK)
```text
{"message":"Hello, user 127.0.0.1 !!"}
```

Response (429 Too many requests)
```text
{"detail":"429 Too many requests"}
```

`get/hello` - no rate limiting (public route) applied and it returns a message

Response (200 OK)
```text
{"message": "Welcome to FastAPI tutorials!"}
```

---

## How It Works

1. **Detection**: When a request hits a protected route, the check_rate_limit dependency extracts the client.host IP.

2. **Verification**: The Counter class queries the rate_limits table in rate_limiter.db.

3. **Logic**:

    ```text
    Client Request
        │
        v
    check_rate_limit (src/utils/dependency)
        │
        ├─> New IP?         -> Insert record, allow
        ├─> Window expired? -> Reset counter, allow 
        ├─> Under limit?    -> Increment counter, allow 
        └─> Over limit?     -> Raise HTTP 429 
    ```

4. **Error Handling**: The Status class manages the HTTPException with a standardized detail message.

---

## Testing

We can use the `test_api.py` script to verify the rate limiting functionality.

```bash
# in another terminal

python src/tests/test_api.py
```

This script will send 25 consecutive requests to the server and report which were allowed and which were denied once the limit is reached.