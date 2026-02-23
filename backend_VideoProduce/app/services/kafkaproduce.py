from faststream import FastStream
from faststream.kafka import KafkaBroker
from app.core.config import KAFKA_URL

broker = KafkaBroker(KAFKA_URL)

async def kafka_send(s3path: str):
    await broker.publish(s3path, topic="ready_to_detect")