from fastapi import Request
from classes.Counter import Counter
from classes.RateLimit import rate_limit
from classes.Status import Status

limiter = Counter(limit=rate_limit.REQUEST_PER_SECOND, seconds=1)


async def check_rate_limit(request: Request):
    client_ip = request.client.host

    if not limiter.allow_request(client_ip):
        raise Status.raise_rate_limit_error()  # Trigger 429 error
