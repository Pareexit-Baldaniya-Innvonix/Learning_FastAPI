import time
import uvicorn
from Settings import db_settings
from fastapi import FastAPI, Request
from classes.StatusCode import StatusCode
from classes.FixedWindowCounter import FixedWindowCounter

app = FastAPI()

limiter = FixedWindowCounter(limit=db_settings.REQUEST_PER_SECOND, seconds=1)


@app.get("/")  # Base API route
def read_root():
    return {"message": "Welcome to FastAPI tutorials!"}


def run_test():
    user_ip = limiter.get_ip()
    print(f"Detected IP: {user_ip}")

    for i in range(25):
        allowed = limiter.allow_request(user_ip)
        if allowed:
            print(f"Request {i+1}: Allowed")
        else:
            print(f"Request {i+1}: Denied", StatusCode.error_code())
        time.sleep(1)


@app.get("/hello")  # API route
def greet(request: Request):
    client_ip = request.client.host

    return {"hello": "world", "ip": client_ip}


if __name__ == "__main__":
    run_test()

    print("\n--- Starting FastAPI server ---")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
