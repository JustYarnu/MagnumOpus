from queue import Queue
import os

class CommitProducer:
    def __init__(self, file_path):
        self.file_path = file_path

    def produce(self, queue: Queue):

        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = [l for l in f.readlines() if l.strip()]

        for line in lines:
            queue.put(line.strip())