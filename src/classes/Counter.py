# ----- library import -----
import time
import sqlite3
from fastapi import Request

# ----- local import -----
from src.config.constants import DB_NAME
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Counter:
    def __init__(self, limit: int, seconds: int) -> None:
        self.limit = limit
        self.seconds = seconds
        self._prepare_db()

    def _prepare_db(self) -> None:
        logger.info("Initializing a rate-limiter database table")
        # create a table
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                """ 
                    CREATE TABLE IF NOT EXISTS rate_limits(
                        client_ip TEXT PRIMARY KEY,
                        request_count INTEGER,
                        window_start_time REAL
                    )
                """
            )
            conn.commit()
        logger.info("Rate-limiter Database ready.")

    def get_ip(self, request: Request) -> str:
        return request.client.host

    def allow_request(self, ip: str) -> bool:
        current_time = time.time()

        with sqlite3.connect(DB_NAME) as conn:
            # inserting record in the database table
            cursor = conn.cursor()
            cursor.execute(
                "SELECT request_count, window_start_time FROM rate_limits WHERE client_ip = ?",
                (ip,),
            )
            row = cursor.fetchone()

            # new IP
            if row is None:
                logger.info(f"New IP {ip} at {current_time}.")
                cursor.execute(
                    "INSERT INTO rate_limits (client_ip, request_count, window_start_time) VALUES (?, 1, ?)",
                    (ip, current_time),
                )
                conn.commit()
                logger.info("Request 1 Allowed: 200 Ok")
                return True

            request_count, window_start_time = row

            # reset the window
            if current_time - window_start_time > self.seconds:
                logger.info(f"Window reset for {ip} at {current_time}.")
                cursor.execute(
                    "UPDATE rate_limits SET request_count = 1, window_start_time = ? WHERE client_ip = ?",
                    (current_time, ip),
                )
                conn.commit()
                logger.info("Request 1 Allowed: 200 Ok")
                return True

            # increment request_count
            request_count = row[0]
            new_count = request_count + 1
            cursor.execute(
                "UPDATE rate_limits SET request_count = ? WHERE client_ip = ?",
                (new_count, ip),
            )
            conn.commit()

            # decide allow/deny based on the NEW count
            if new_count <= self.limit:
                logger.info(f"Request {new_count} Allowed: 200 Ok")
                return True
            else:
                # request denied
                logger.warning(f"Request {new_count} Denied: 429 Too Many Requests")
                return False
