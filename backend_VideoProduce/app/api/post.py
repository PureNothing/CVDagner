from fastapi import UploadFile, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.logger import logger
from app.services.dbschema import DBCORE
from app.services.s3send import s3_client_videos, s3_client_frames
from app.orkestr.orkestr import orkestr_func
from contextlib import asynccontextmanager
from app.core.kafkabroker import broker
import app.services.kafkaconsume

@asynccontextmanager
async def lifepsawn(router):
    logger.debug("Проверяю БД и S3 перед запуском")
    try:
        await DBCORE.create_tables()
        await s3_client_videos.bucket_check()
        await s3_client_frames.bucket_check()
    except Exception as e:
        logger.error("Ошибка при инициализации БД или S3")
        raise
    try:
        logger.debug("Открываю соединие TCP c Kafka..")
        await broker.start()
    except Exception as e:
        logger.debug(f"Ошибка открытия соединия TCP с Kafka. {e}")
    yield
    logger.debug("Закрываю соединени S3, KAFKA, БД..")
    await broker.stop()
    logger.debug("="*20)


router = APIRouter(lifespan=lifepsawn)

@router.post("/video_upload/{camera_id}")
async def upload_video(videos: list[UploadFile], camera_id: int):
    logger.debug(f"Получено {len(videos)} видео.")
    for index, video in enumerate(videos):
        try:
            logger.debug(f"Пробую обработать {index+1}/{len(videos)}..")
            content = await video.read()
            name = video.filename
            await orkestr_func(file_name=name, content=content, camera_id=camera_id)
            logger.debug("Видео и все его фреймы успешно обработаны (S3, БД)!")
        except Exception as e:
            logger.error(f"Ошибка обработки видео! {e}")
            raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(status_code=200, content={"status": "ok"})

