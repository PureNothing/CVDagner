from app.core.kafkabroker import broker
from app.services.dbschema import DBCORE
from app.logger import logger

@broker.subscriber("frame_detected")
async def video_detected(minio_path):
    try:
        logger.debug(f"Получено сообщение из Kafka = (frame_detected) о обработанном фрейме, меняю статус..")
        await DBCORE.update_status_frames(minio_path=minio_path)
        logger.debug(f"Статус успешно изменен.")
    except Exception as e:
        logger.error(f"Не удалось изменить статус в БД. {e}")