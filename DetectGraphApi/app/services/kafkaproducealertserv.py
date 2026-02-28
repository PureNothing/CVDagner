from app.core.kafkabroker import broker
from app.logger import logger

async def publish_alert_service(detection_results: dict, camera_id: int):
    try:
        logger.debug("Получены результаты детекции публикую в топик Kafka = (alerts_topic).")
        await broker.publish({"detection_results": detection_results, "camera_id": camera_id}, topic = "alerts_topic")
        logger.debug("Реузльтаты детекции успешно опубликованы в топик Kafka = (alerts_topic).")
    except Exception as e:
        logger.error(f"Не удалось опубликовать в топик Kafka = (alerts_topic) результаты детекции. {e}")
        raise