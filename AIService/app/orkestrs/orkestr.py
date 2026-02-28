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
                async with session.post(url=UPDATE_ALERTS_URL, json={"message": so}) as response:
                    response.raise_for_status()
                    logger.debug("Факты успешно извлечены и отправлены на сервер изменения алертов.")
                    return "Отправлено на сервер алертов и правил."
        else:
            return so
    except Exception as e:
        logger.error(f"Факты не удалось извлечь. {e}")
        raise