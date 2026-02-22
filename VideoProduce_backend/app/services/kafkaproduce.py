from faststream import FastStream
from faststream.kafka import KafkaBroker
from config import KAFKA_URL

broker = FastStream(KAFKA_URL)

async def kafka_send(s3path: str):
    async with broker as broker:
        await broker.publish(s3path)