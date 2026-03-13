import time
import sqlite3
from config.constants import DB_NAME


class Counter:
    def __init__(self, limit: int, seconds: int) -> None:
        self.limit = limit
        self.seconds = seconds
        self._prepare_db()

    def _prepare_db(self):
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

    def get_ip(self, request):
        return request.client.host

    def allow_request(self, ip: str) -> bool:
        current_time = time.time()

        with sqlite3.connect(DB_NAME) as conn:
            # inserting record in the database table
            cursor = conn.cursor()
            cursor.execute("SELECT request_count, window_start_time FROM rate_limits WHERE client_ip = ?", (ip,))
            row = cursor.fetchone()

            if row is None:
                print(f"\nDEBUG: New IP {ip} at {window_start_time}. Initializing tracker.")
                cursor.execute(
                    "INSERT INTO rate_limits (client_ip, request_count, window_start_time) VALUES (?, ?, ?)",
                    (ip, 1, current_time),
                )
                conn.commit()
                return True

            request_count, window_start_time = row

            if current_time - window_start_time > self.seconds:
                # reset the window
                print(f"\nDEBUG: Window reset for {ip} at {current_time}.")
                cursor.execute(
                    "UPDATE rate_limits SET request_count = 1, window_start_time = ? WHERE client_ip = ?",
                    (current_time, ip),
                )
                conn.commit()
                return True
            elif request_count < self.limit:
                # increment request_count
                print(
                    f"\nDEBUG: IP {ip} has {request_count + 1}/{self.limit} requests at {current_time}."
                )
                cursor.execute(
                    "UPDATE rate_limits SET request_count = request_count + 1 WHERE client_ip = ?", (ip,)
                )
                conn.commit()
                return True
            else:
                print(f"\nDEBUG: RATE LIMIT EXCEEDED for {ip} at {current_time}!")
                return False