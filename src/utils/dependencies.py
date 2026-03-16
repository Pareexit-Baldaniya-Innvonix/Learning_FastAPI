from fastapi import Request
from src.classes.Counter import Counter
from src.classes.Status import Status
from src.classes.Settings import settings


limiter = Counter(limit=settings.REQUEST_PER_SECOND, seconds=1)


async def check_rate_limit(request: Request):
    client_ip = request.client.host

    if not limiter.allow_request(client_ip):
        Status.raise_rate_limit_error()  # Trigger 429 error
