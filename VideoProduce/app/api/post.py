from fastapi import FastAPI, UploadFile, File
import uvicorn
from main import orkestr
import uuid
from logger import logger

def lifepsawn():
    print("Будет что то с запуском БД и S3")
    yield
    print("Будет что то с закрытием БД и S3")


app = FastAPI(lifespan=lifepsawn)

@app.post("/video_ipload")
async def upload_video(videos: list[UploadFile], camera_id):
    for index, video in enumerate(videos):
        
        try:
            content = await video.read
            if "." in video.filename:
                end = video.filename.split('.')[-1]
                uniq_name = str(uuid.uuid4()) + "." + end
            else:
                uniq_name = str(uuid.uuid4())
            await orkestr(content, uniq_name)
        except:
            logger.error("Ошибка обработки видео!")


if __name__ == '__main__':
    uvicorn.run("fapi:app", reload=True)
