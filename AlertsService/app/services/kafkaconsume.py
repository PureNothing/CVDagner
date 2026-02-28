from app.core.kafkabroker import broker
from app.logger import logger
from app.orkestrs.orkestr_sender import orkestr_func
from pydantic import BaseModel


class DetetedObjects(BaseModel):
    success: bool
    boxes: list
    labels: list
    scores: list
    message: str


class DetectionMesage(BaseModel):
    detection_results: DetetedObjects
    camera_id: int

@broker.subscriber("alerts_topic")
async def detection_consume(message: DetectionMesage):
    try:
        logger.debug("Получение сообщение из Detection сервиса, номер камеры и разпознанные данные отправляю в оркестратор.")
        await orkestr_func(detection_results = message.detection_results, camera_id = message.camera_id)
    except Exception as e:
        logger.error(f"Не удалось отправить в оркесратор результаты детекции. {e}")