import uuid
from app.services.s3send import s3_client_videos
from app.logger import logger
from app.framer.framer import exctract_and_load_frames
from app.services.dbschema import DBCORE


async def orkestr_func(file_name, content, camera_id):
    logger.debug("Назначаю имена файлам..")
    base_uniq_name = f"camera_id={camera_id}/"+ str(uuid.uuid4())
    if "." in file_name:
        end = file_name.split('.')[-1]
        video_iniq_name = f"{base_uniq_name}" + "." + end
    else:
        video_iniq_name = f"{base_uniq_name}"
    try:
        logger.debug("Отправляю видео в S3")
        await s3_client_videos.upload_file(file_name=video_iniq_name, file_data=content)
        logger.debug("Видео успешно отправлено в S3")
    except Exception as e:
        logger.debug("Не удалось отправить видео в S3")
        raise
    try:
        logger.debug("Отпарвляю информацию о видео в БД")
        video_id = await DBCORE.insert_videos(camera_id=camera_id, minio_path=video_iniq_name)
        logger.debug("Видео успешно загружено в БД")
    except Exception as e:
        logger.error(f"Не удалось загрузить данные о видео в БД. {e}")
        raise
    try:
        logger.debug("Отправляю фреймы видео в S3 и БД..")
        await exctract_and_load_frames(base_name=base_uniq_name, content=content, camera_id=camera_id, video_id=video_id)
        logger.debug("Фреймы нарезаны и успешно загружены в S3 и инфа о всех в БД")
    except Exception as e:
        logger.error("Не удалось нарезать или загрузить фреймы в S3")
        raise
    