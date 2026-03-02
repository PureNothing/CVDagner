from app.core.kafkabroker import broker
from app.logger import logger

async def kafka_send(camera_id: int, label: str, count: int, mestnost: str, coordinates: list):
    try:
        logger.debug("Узнал о превышении порога, сообщаю в бота..")
        await broker.publish({"camera_id": camera_id, 
                              "label": label, 
                              "count": count, 
                              "place": mestnost, 
                              "coordinates": coordinates}, 
                              topic="real_alerts")
    except Exception as e:
        logger.error(f"Ошибка при отправке боту алерта. {e}")
