from faststream import FastStream
from faststream.kafka import KafkaBroker
from config import KAFKA_URL

broker = KafkaBroker(KAFKA_URL)

@broker.subscriber("frame_detected")
async def video_detected(frame_name):
    