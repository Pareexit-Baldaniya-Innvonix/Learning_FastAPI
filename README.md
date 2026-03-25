# FastAPI Rate Limiter
A FastAPI rate limiter is a mechanism used to control the number of requests a client (i.e user or IP address) can make to a FastAPI application within a specific time period.

When the limit exceeded, algorithm automatically returns '429 Too Many Requests' error and after certain amount of time it will refresh.

---

## Tech Stack

Runtime: Python 3.12 (Slim Bookworm)

Framework: FastAPI

Package Manager: uv

Database: SQLite3

Containerization: Docker & Docker Compose

---

## Project Structure

```text
.
├── example.env                 # Template for environment variables
├── README.md                   # Project documentation
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Multi-container orchestration
├── pyproject.toml              # Project metadata & dependencies
├── uv.lock                     # Deterministic lockfile (managed by uv)
└── src/                        # Source code
    ├── main.py                 # FastAPI entry point
    ├── rate_limiter.db         # SQLite database file
    ├── app.log                 # Rotating log file
    ├── classes/                # Logic handlers
    │   ├── Counter.py
    │   ├── Middleware.py
    │   ├── Settings.py
    │   └── Status.py
    ├── config/                 # Global constants & configurations
    │   └── constants.py
    ├── tests/                  # API functional tests
    │   └── test_api.py
    └── utils/                  # Database & dependencies
        ├── db_connection.py
        ├── dependencies.py
        └── logger.py
```

---

## Configuration

The application is highly configurable via environment variables.

| Variable | Default | Description |
| --- | :---: | --- |
| REQUEST_PER_SECOND | 20 | Maximum requests allowed per 1-second window |
| LOG_LEVEL | INFO | Logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| ENV | development | Checking that environment is production or development |

---

## Setup and Installation

The fastest way to get the project running is using Docker Compose. This handles the environment setup and database persistence automatically.

Prerequisites
 - Python 3.8+
 - FastAPI
 - SQLite3

**Installation**

```bash
# clone the repository

git clone <your_repository-url>
cd <your-repo>
```

**Run the application**

```bash
# for docker

docker compose up --build  # for starting the docker container

docker compose down # for removing the docker container 
```

----- OR -----

**Running the server**

```bash
# for directly run the server

uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

The server starts at `http://127.0.0.1:8000`

**Testing**

While the container or server is running, trigger the test script from host machine to verify the rate limiting:

```bash
# in another terminal

python src/tests/test_api.py
```

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

1. **Detection**: When a request hits a protected route, the `check_rate_limit` dependency extracts the client.host IP.

2. **Verification**: The Counter class queries the rate_limits table in `rate_limiter.db`.

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

5. **Logging**: All activity is logged to both the console and src/app.log with automatic rotation.

---
