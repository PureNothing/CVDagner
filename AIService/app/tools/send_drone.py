import aiohttp
from app.core.config import GET_COORDINATES_URL, GET_RESTRICTIONS_URL
from app.logger import logger

async def send_drone_tool(camera_id: int):
    try:
        logger.debug(f"Запрашиваю отправу дрона к камере {camera_id}.")
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{GET_COORDINATES_URL}/{camera_id}") as response:
                coordinates = await response.json()
                logger.debug(f"Получены координаты камеры {camera_id} = {coordinates}.")
            async with session.get(url=f"{GET_RESTRICTIONS_URL}/{camera_id}") as response:
                place = await response.json()
                logger.debug(f"Местонсть камеры {camera_id} на коориданатах {coordinates} получена.")
            logger.debug("Дрон отправлен.")
            return f"Дрон отправлен к камере {camera_id} = {coordinates}\nНа местность:\n {place}."
    except Exception as e:
        logger.error(f"Не удалось запросить координаты для отправки дрона. {e}")
        raise