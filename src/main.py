from fastapi import FastAPI, Request, Depends
from utils.dependencies import check_rate_limit

app = FastAPI()


@app.get("/hello")  # Base API route
def read_root():
    return {"message": "Welcome to FastAPI tutorials!"}


@app.get("/", dependencies=[Depends(check_rate_limit)])  # API route
def greet(request: Request):
    return {"hello": "world", "ip": request.client.host}
