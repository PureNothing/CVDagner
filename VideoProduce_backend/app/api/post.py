from fastapi import FastAPI, UploadFile, APIRouter
import uvicorn
from main import orkestr
import uuid
from app.logger import logger

def lifepsawn():
    print("Будет что то с запуском БД и S3")
    yield
    print("Будет что то с закрытием БД и S3")


router = APIRouter(lifespan=lifepsawn)

@router.post("/video_ipload/{camera_id}")
async def upload_video(videos: list[UploadFile], camera_id):
    for index, video in enumerate(videos):
        logger.debug(f"Получено {len(videos)} видео.")
        try:
            logger.debug(f"Пробую обработать {index+1}/{len(videos)}")
            content = await video.read
            if "." in video.filename:
                end = video.filename.split('.')[-1]
                uniq_name = f"camera_id={camera_id}"+ str(uuid.uuid4()) + "." + end
            else:
                uniq_name = str(uuid.uuid4())
                await orkestr(content, uniq_name)
        except Exception as e:
            logger.error(f"Ошибка обработки видео! {e}")

