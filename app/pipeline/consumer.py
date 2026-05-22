from os import path
import queue
import time
from queue import Empty


class CommitConsumer:
    def __init__(self, git_client, metrics, config, logger):
        self.git = git_client
        self.metrics = metrics
        self.config = config
        self.logger = logger

        self.commits_since_push = 0
        self.total_commits = 0
        self.batch_number = 0

    def _remove_first_line(self):
        path = self.config.file.input_path

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        lines = [l for l in lines if l.strip()]
        remaining = lines[1:] if lines else []

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(remaining)
    
    def consume(self, queue):
        while not queue.empty() and self.total_commits < self.config.commit.limit:

            msg = queue.get()

            try:
                self.git.commit_all(msg)

                self.total_commits += 1
                self.commits_since_push += 1

                self.metrics.inc_commit()

                self.logger.commit(
                    current=self.total_commits,
                    total=self.config.commit.limit,
                    msg=msg
                )

                self._remove_first_line()

                if self.commits_since_push >= self.config.commit.push_interval:
                    self.batch_number += 1

                    self.git.push(self.config.repo.branch)
                    self.metrics.inc_push()

                    self.logger.push(self.batch_number)

                    self.commits_since_push = 0

                    time.sleep(self.config.commit.delay_seconds)

            except Exception as e:
                self.metrics.inc_failed()
                self.logger.error("Commit failed", e)

        queue.task_done()