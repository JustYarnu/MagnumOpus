from queue import Queue

import git
from git import config
from joblib import Logger

from app.config import load_config
from app.observability import metrics
from app.pipeline.producer import CommitProducer
from app.pipeline.consumer import CommitConsumer
from app.pipeline.git_client import GitClient
from app.observability.metrics import Metrics
from app.observability.logger import EventLogger


def run():

    config = load_config()

    git = GitClient(config.repo.path)
    metrics = Metrics()
    logger = EventLogger()

    queue = Queue()

    producer = CommitProducer(config.file.input_path)
    consumer = CommitConsumer(git, metrics, config, logger)
    producer.produce(queue)
    consumer.consume(queue)

    print(metrics.summary())


if __name__ == "__main__":
    run()