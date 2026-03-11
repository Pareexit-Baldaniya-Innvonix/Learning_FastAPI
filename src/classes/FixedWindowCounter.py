import time
import sqlite3
import socket

DB_NAME = "rate_limiter.db"  # database


class FixedWindowCounter:
    def __init__(self, limit, seconds):
        self.limit = limit
        self.seconds = seconds
        self._prepare_db()

    def _prepare_db(self):
        # create a table
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                """ 
                    CREATE TABLE IF NOT EXISTS limits(
                        ip TEXT PRIMARY KEY,
                        count INTEGER,
                        start_time REAL
                    )
                """
            )

    def get_ip(self):
        # getting user ip address
        # AF_INET: use IPv4
        # SOCK_DGRAM: specifies UDP to establish connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 1))  # send data to public DNS on port 1
            ip = s.getsockname()[
                0
            ]  # returns a tuple containing the local add and the port
        except:
            return "127.0.0.1"
        finally:
            s.close()
        return ip

    def allow_request(self, ip):
        current_time = time.time()

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # inserting record in the database table
            cursor.execute("SELECT count, start_time FROM limits WHERE ip = ?", (ip,))
            row = cursor.fetchone()

            if row is None:
                cursor.execute(
                    "INSERT INTO limits VALUES (?, ?, ?)", (ip, 1, current_time)
                )
                return True

            count, start_time = row

            if current_time - start_time > self.seconds:
                # reset the seconds
                cursor.execute(
                    "UPDATE LIMITS SET count = 1, start_time = ? WHERE ip = ?",
                    (current_time, ip),
                )
                conn.commit()
                return True
            elif count < self.limit:
                # increment count
                cursor.execute(
                    "UPDATE limits SET count = count + 1 WHERE ip = ?", (ip,)
                )
                conn.commit()
                return True
            else:
                return False
