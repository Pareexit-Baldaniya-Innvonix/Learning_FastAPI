from fastapi import HTTPException


class Status:

    @staticmethod
    def raise_rate_limit_error():
        raise HTTPException(
            status_code=429,
            detail="429 Too many requests",
        )
