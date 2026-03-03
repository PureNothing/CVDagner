from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from app.logger import logger
from pydantic import BaseModel
from app.agentsfuncs.agentexctractaddcam import exctract_new_camera_func
import aiohttp
from app.core.config import ADD_CAMERA_URL

router = APIRouter()

class BotMessage(BaseModel):
    message: str

@router.post("/ai_new_camera")
async def ai_new_camera_parse(message: BotMessage):
    logger.debug("Получено сообщение от пользователя на добавление новой камеры обрабатываю..")
    try:
        result = await exctract_new_camera_func(message=message.message)
        if result == "Не понял переформулируйте запрос.":
            return JSONResponse(status_code=400, content={"status": result})
        async with aiohttp.ClientSession() as session:
            async with session.post(url=ADD_CAMERA_URL, json={"camera_id": result.camera_id, 
                                                              "coordinates": result.coordinates, 
                                                              "place": result.place}) as response:
                logger.debug("Получен ответ от сервиса добавления правил по поводу добавления камеры, возвращаю..")
                response = await response.json()
                return JSONResponse(status_code=200, content={"status": response["status"]})
    except Exception as e:
        logger.error(f"Не удалось добавить камеру. {e}")
        raise HTTPException(status_code=500, detail=str(e))


