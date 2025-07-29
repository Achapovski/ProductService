from faststream.kafka import KafkaBroker

from src.core.settings.settings import settings

# kafka_broker = KafkaBroker(bootstrap_servers=settings.KAFKA.BOOSTRAP_SERVERS)
kafka_broker = KafkaBroker(bootstrap_servers=["45.89.188.224:9092"])
