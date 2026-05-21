class CommitConsumer:
    def __init__(self, git_client, metrics):
        self.git = git_client
        self.metrics = metrics

    def consume(self, queue):

        while not queue.empty():

            msg = queue.get()

            try:
                self.git.commit_all(msg)
                self.metrics.inc_commit()

                print(f"[COMMIT] {msg}")

            except Exception:
                self.metrics.inc_failed()

            queue.task_done()