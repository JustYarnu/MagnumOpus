import os


class CommitProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def next_commit_message(self):
        if not os.path.exists(self.file_path):
            return None, None

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]

        if not lines:
            return None, None

        return lines[0], lines[1:]