# FastAPI
Learning and completing all FastAPI tasks in this repository.

## How to run the code
For running the code need to add `uvicorn` and then need to follow this steps:
1. open terminal
2. set the file url to that place where main file located
3. run this code through the `debugger` or try
    
    Terminal-1:
    - `uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload`
    - --reload used for auto reload the file
    - once the server is started do next step...

    Terminal-2:
    - `python src/tests/test_api.py`
    - this runs a loop which checks how many requests are allowed and what happens after rate-limit hits.
    - whenever we changed it, need to restart the server from Terminal-1 and it's working.

## API endpoints:

`get/`
- rate limited endpoint which returns a greeting with client-ip

Response (200 OK):
```
{"message":"Hello, user 127.0.0.1 !!"}
```

Response (429 Too many requests):
```
{"detail":"429 Too many requests"}
```

`get/hello`
- no rate limiting applied and it returns a message

Response (200 OK):
```
{"message": "Welcome to FastAPI tutorials!"}
```

## How It Works:

1. Every request to a rate-limited route triggers the check_rate_limit FastAPI dependency.
2. The dependency extracts the client IP and calls Counter.allow_request(ip).
3. Counter looks up the IP in the SQLite rate_limits table:

    - New IP --> insert a row with request_count = 1 and the current timestamp. Allow.
    - Within window, under limit --> increment request_count. Allow.
    - Within window, at/over limit --> do nothing. Deny with HTTP 429.
    - Window expired --> reset request_count = 1 and update window_start_time. Allow.
