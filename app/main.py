from queue import Queue

from app.config import load_config
from app.pipeline.producer import CommitProducer
from app.pipeline.consumer import CommitConsumer
from app.pipeline.git_client import GitClient
from app.observability.metrics import Metrics


def run():

    config = load_config()

    git = GitClient(config.repo.path)
    metrics = Metrics()

    queue = Queue()

    producer = CommitProducer(config.file.input_path)
    consumer = CommitConsumer(git, metrics)

    producer.produce(queue)
    consumer.consume(queue)

    print(metrics.summary())


if __name__ == "__main__":
    run()