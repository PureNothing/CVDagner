import aiohttp
from app.agentsfuncs.agentextract import exctract_rule
from app.core.config import UPDATE_ALERTS_URL
from app.core.so import SO
from app.logger import logger

async def orkestr_func(message: str):
    try:
        logger.debug("Отправляю сообщение на извлечение фактов..")
        so = await exctract_rule(message=message)
        if isinstance (so, SO):
            async with aiohttp.ClientSession() as session:
                so = so.model_dump()
                async with session.post(url=UPDATE_ALERTS_URL, json={"camera_id": so["camera_id"], "label": so["label"], "threshold": so["count"]}) as response:
                    result = await response.json()
                    if response.status == 400:
                        return result['status']
                    logger.debug("Факты успешно извлечены и отправлены на сервер изменения алертов.")
                    return "Отправлено на сервер алертов и правил."
        else:
            return so
    except Exception as e:
        logger.error(f"Факты не удалось извлечь. {e}")
        raise