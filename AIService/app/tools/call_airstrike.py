import aiohttp
from app.core.config import GET_COORDINATES_URL
from app.logger import logger


async def send_airstrike_tool(camera_id: int):
    try:
        logger.debug(f"Запрашиваю коордианаты для авиадура к камере {camera_id}.")
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{GET_COORDINATES_URL}/{camera_id}") as response:
                coordinates = await response.json()
                logger.debug(f"Получены коордианаты камеры {camera_id} = {coordinates}.")
                logger.debug("Авиаудар выполнен.")
                return "Авиаудар Выполнен"
    except Exception as e:
        logger.error(f"Не удалось запросить координаты для авиаудара. {e}")
        raise

