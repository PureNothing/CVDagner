from app.core.kafkabroker import broker
from app.orkestr.orkestr import orkerstr_func
from app.logger import logger
from pydantic import BaseModel

class FrameModel(BaseModel):
    minio_path: str
    camera_id: int

@broker.subscriber("ready_to_detect", max_workers=2)
async def ready_to_detect(message: FrameModel):
    try:
        logger.debug("Получение адрес Minio из топика Kafka = (ready_to_detect) отправляю на обработку..")
        await orkerstr_func(minio_path=message.minio_path, camera_id=message.camera_id)
        logger.debug("Файл успешно прошел весь цикл обработки.")
    except Exception as e:
        logger.error(f"Файл не смог пройти пайплайн детекции. {e}")
        raise
    
