from fastapi import HTTPException


class StatusCode:

    @staticmethod
    def error_code():
        return HTTPException(
            status_code=429,
            detail="Too many requests",
        )
