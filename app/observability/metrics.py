import time

class Metrics:
    def __init__(self):
        self.commits = 0
        self.pushes = 0
        self.failed = 0
        self.start_time = time.time()

    def inc_commit(self):
        self.commits += 1

    def inc_push(self):
        self.pushes += 1

    def inc_failed(self):
        self.failed += 1

    def summary(self):
        runtime = time.time() - self.start_time
        return {
            "commits": self.commits,
            "pushes": self.pushes,
            "failed": self.failed,
            "runtime_sec": runtime,
            "commit_rate": self.commits / runtime if runtime else 0,
        }