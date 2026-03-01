from faststream.kafka import KafkaBroker
from bot.core.config import KAFKA_URL

broker = KafkaBroker(KAFKA_URL)