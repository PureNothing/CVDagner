import aiohttp
from app.core.config import GET_RESTRICTIONS_URL
from app.logger import logger

async def get_restrict(camera_id):
    try:
        logger.debug(f"Получен запрос на информацию о местности камеры {camera_id}.")
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{GET_RESTRICTIONS_URL}/{camera_id}") as response:
                response = await response.json()
                logger.debug("Информация местности успешно получена.")
                return f"Описание местности камеры: {response}"
    except Exception as e:
        logger.error(f"Не удалось запросить информацию о местности камеры {camera_id}. {e}")
        raise


