from fastapi import APIRouter
from app.funcs.get_coordinates import get_coordinates_func
from app.logger import logger

router = APIRouter()

@router.get("/get_coordinates/{camera_id}")
async def get_coordinates(camera_id: int):
    try:
        logger.debug("Пришел запрос на получени координат, обрабатываю..")
        coordinates = await get_coordinates_func(camera_id=camera_id)
        logger.debug("Коордианты успешно получены и отправлены.")
        return coordinates
    except Exception as e:
        logger.error("Не удалос получить или вернуть коориданты.")
        raise