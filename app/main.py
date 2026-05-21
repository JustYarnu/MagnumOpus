from queue import Queue

from app.config import load_config
from app.pipeline.producer import CommitProducer
from app.pipeline.consumer import CommitConsumer
from app.pipeline.git_client import GitClient
from app.observability.metrics import Metrics
from app.observability.logger import EventLogger


def run():
    app_config = load_config()

    git_client = GitClient(app_config.repo.path)
    metrics = Metrics()
    logger = EventLogger()

    queue = Queue()

    producer = CommitProducer(app_config.file.input_path)
    consumer = CommitConsumer(git_client, metrics, app_config, logger)

    producer.produce(queue)
    consumer.consume(queue)

    print(metrics.summary())


if __name__ == "__main__":
    run()