from fastapi import FastAPI, Request, Depends
from src.utils.dependencies import check_rate_limit

app = FastAPI()


@app.get("/hello")  # Base API route
def read_root():
    return {"message": "Welcome to FastAPI tutorials!"}


@app.get("/", dependencies=[Depends(check_rate_limit)])  # API route
def home(request: Request):
    client_id = request.client.host
    return {"message": f"Hello, user {client_id} !!"}
