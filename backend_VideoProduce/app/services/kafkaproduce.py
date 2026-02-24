from app.core.kafkabroker import broker
from app.logger import logger

async def kafka_send(s3path: str, camera_id: int):
    try:
        logger.debug("Получено сообщение отправляю в топик Kafka = (ready_to_detect)..")
        await broker.publish({"minio_path": s3path, "camera_id": camera_id}, topic="ready_to_detect")
        logger.debug("Сообщение успешно отправлено в топик Kafka = (ready_to_detect)")
    except Exception as e:
        logger.error(f"Не удалось отправить в топик Kafka = (ready_to_detect). {e}")
        raise