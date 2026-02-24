from app.core.kafkabroker import broker
from app.logger import logger

async def publish_video_produce_service(minio_path):
    try:
        logger.debug("Получено сообщение что фрейм был обработан отправял в топик Kafka = (frame_detected).")
        await broker.publish(minio_path, "frame_detected")
        logger.debug("Успешно отправлено в топик Kafka = (frame_detected).")
    except Exception as e:
        logger.error(f"Не удалось отправить в топик Kafka = (frame_detected). {e}")
        raise