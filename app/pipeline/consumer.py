import time

class CommitConsumer:
    def __init__(self, git_client, metrics, config):
        self.git = git_client
        self.metrics = metrics
        self.config = config

        self.commits_since_push = 0

    def consume(self, queue):

        count = 0

        while not queue.empty() and count < self.config.commit.limit:

            msg = queue.get()

            try:
                self.git.commit_all(msg)
                self.metrics.inc_commit()

                count += 1
                self.commits_since_push += 1

                print(f"[COMMIT] {msg}")

                if self.commits_since_push >= self.config.commit.push_interval:
                    self.git.push(self.config.repo.branch)
                    self.metrics.inc_push()

                    print("[PUSH] batch pushed")

                    self.commits_since_push = 0
                    time.sleep(self.config.commit.delay_seconds)

            except Exception:
                self.metrics.inc_failed()

            queue.task_done()