import logging
import sys

class EventLogger:
    def __init__(self):
        self.logger = logging.getLogger("commit-bot")
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def commit(self, current: int, total: int, msg: str):
        self.logger.info(f"COMMIT | {current}/{total} | {msg}")

    def push(self, batch: int):
        self.logger.info(f"PUSH   | batch={batch}")

    def timeout(self, seconds: int):
        self.logger.info(f"TIMEOUT | {seconds}s")