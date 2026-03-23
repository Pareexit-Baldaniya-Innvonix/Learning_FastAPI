# ----- library import -----
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# ----- local import -----
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"

        response = await call_next(request)

        # check for route
        if request.url.path:
            logger.info(
                f"client_ip: {client_ip} visits {request.method} {request.url.path} status {response.status_code}"
            )
        return response
