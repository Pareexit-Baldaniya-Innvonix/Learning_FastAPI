from fastapi import FastAPI, Request, HTTPException
from classes.FixedWindowCounter import FixedWindowCounter
import uvicorn
import time
from Settings import db_settings

app = FastAPI()

limiter = FixedWindowCounter(limit=db_settings.REQUEST_PER_SECOND, seconds=1)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI tutorials!"}


@app.get("/hello")
def greet(request: Request):
    client_ip = request.client.host

    # check actual clients IP
    if not limiter.allow_request(client_ip):
        raise HTTPException(status_code=429, details="Too many requests")

    return {"hello": "world", "ip": client_ip}


def main():
    user_ip = limiter.get_ip()
    print(f"Detected IP: {user_ip}")

    for i in range(25):
        allowed = limiter.allow_request(user_ip)
        status = "Allowed" if allowed else "Denied (Error! 429 Too Many Requests)"
        print(f"Request {i+1}: {status}")
        time.sleep(1)


if __name__ == "__main__":
    main()

    print("\n--- Starting FastAPI server ---")
    uvicorn.run(app, host="0.0.0.0", port=8001)
