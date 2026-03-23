from src.utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

# ----- library import -----
from fastapi import FastAPI, Request, Depends

# ----- local import -----
from src.utils.dependencies import check_rate_limit
from src.classes.Middleware import LoggingMiddleware

app = FastAPI()

# middleware for "/hello" route
app.add_middleware(LoggingMiddleware)


@app.get("/", dependencies=[Depends(check_rate_limit)])  # Base API route
def home(request: Request) -> dict[str, str]:
    client_ip = request.client.host
    return {"message": f"Hello, user {client_ip} !!"}


@app.get("/hello")  # Hello API route
def hello() -> dict[str, str]:
    return {"message": "Welcome to FastAPI tutorials!"}
