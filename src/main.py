from src.utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

# ----- library import -----
from fastapi import FastAPI, Request, Depends

# ----- local import -----
from src.utils.dependencies import check_rate_limit

app = FastAPI()


@app.get("/", dependencies=[Depends(check_rate_limit)])  # Base API route
def home(request: Request) -> dict[str, str]:
    client_ip = request.client.host
    return {"message": f"Hello, user {client_ip} !!"}


@app.get("/hello")  # Hello API route
def hello(request: Request) -> dict[str, str]:
    client_ip = request.client.host
    logger.info(f"Endpoint /hello triggered by IP: {client_ip}")
    return {"message": "Welcome to FastAPI tutorials!"}
