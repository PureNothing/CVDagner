import io
import av
from app.services.s3send import s3_client_frames
from app.logger import logger
from app.services.dbschema import DBCORE
from app.services.kafkaproduce import kafka_send

async def exctract_and_load_frames(content: bytes, base_name: str, video_id: str, camera_id: int):
    buffer = io.BytesIO(content)
    container = av.open(buffer, format=None)

    fps = container.streams.video[0].average_rate
    
    logger.debug("Пробую нарезать фреймы и загрузить в S3..")

    for index, frame in enumerate(container.decode(video=0)):
        try:
            if index % int(fps) == 0:
                
                img = frame.to_image()
                buf = io.BytesIO()
                img.save(buf, format="JPEG")
                frame_value = buf.getvalue()
                frame_name = f"{base_name}/frame{index:05d}.jpg"
                await s3_client_frames.upload_file(file_data=frame_value,
                                            file_name=frame_name)
                await DBCORE.insert_frames(minio_path=frame_name,
                                           video_id=video_id,
                                           camera_id=camera_id,
                                           )
                try:
                    logger.debug("Отправляю путь фрейма в топик..")
                    await kafka_send(minio_path = frame_name, camera_id=camera_id)
                    logger.debug("Успшео отправлено в топик!")
                except Exception as e:
                    logger.error(f"Ошибка отправки в топик. {e}")
            else:
                continue
        except Exception as e:
            logger.error(f"Ошибка загрузки фреймов в S3 И БД или нарезке. {e}")

