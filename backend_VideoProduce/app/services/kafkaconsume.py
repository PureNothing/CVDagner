from faststream import FastStream
from faststream.kafka import KafkaBroker
from app.core.config import KAFKA_URL
from app.services.dbschema import DBCORE

broker = KafkaBroker(KAFKA_URL)

@broker.subscriber("frame_detected")
async def video_detected(minio_path):
    await DBCORE.update_status_frames(minio_path=minio_path)