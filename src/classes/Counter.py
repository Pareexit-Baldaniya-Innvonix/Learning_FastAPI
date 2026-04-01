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

        try:
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
                    new_count = 1
                    logger.info(f"First time request from IP: {ip}")
                    cursor.execute(
                        "INSERT INTO rate_limits (client_ip, request_count, window_start_time) VALUES (?, ?, ?)",
                        (ip, new_count, current_time),
                    )
                else:

                    request_count, window_start_time = row

                    # reset the window
                    if current_time - window_start_time > self.seconds:
                        new_count = 1
                        logger.debug(f"Window reset for {ip} at {current_time}.")
                        cursor.execute(
                            "UPDATE rate_limits SET request_count = ?, window_start_time = ? WHERE client_ip = ?",
                            (new_count, current_time, ip),
                        )
                    else:
                        # increment request_count
                        new_count = request_count + 1
                        cursor.execute(
                            "UPDATE rate_limits SET request_count = ? WHERE client_ip = ?",
                            (new_count, ip),
                        )
                conn.commit()

                # decide allow/deny based on the NEW count
                if new_count > self.limit:
                    # request denied
                    logger.warning(
                        f"Request {new_count} Denied",
                        extra={"client_ip": ip, "status": 429},
                    )
                    return False

                logger.info(
                    f"Request {new_count} Allowed",
                    extra={"client_ip": ip, "status": 200},
                )
                return True

        except sqlite3.Error as e:
            logger.error(f"SQLite error: {e}", exc_info=True)
            return True
