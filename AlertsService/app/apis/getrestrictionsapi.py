from fastapi import APIRouter
from app.logger import logger
from app.funcs.get_restrictions import get_restrict_func

router = APIRouter()

@router.get("/get_restrictions/{camera_id}")
async def get_restrict_api(camera_id: int):
    try:
        logger.debug("Получен запрос на получение информации о местности камеры.")
        restrict = await get_restrict_func(camera_id=camera_id)
        logger.debug("Данные о местности успешно получены, отпраляю обратно..")
        return restrict
    except Exception as e:
        logger.error("Не удалось получить данные о местности камеры.")
        raise

