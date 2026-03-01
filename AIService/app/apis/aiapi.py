from fastapi import APIRouter, HTTPException
from contextlib import asynccontextmanager
from app.orkestrs.orkestr import orkestr_func
from fastapi.responses import JSONResponse
from app.logger import logger
from pydantic import BaseModel
from app.core.kafkabroker import broker

@asynccontextmanager
async def lifespawn(router):
    logger.debug("="*20)
    logger.debug("Открываю ендипоинт и TCP с Kafka начинаю работу")
    await broker.start()
    yield
    await broker.stop()
    logger.debug("Закрываю соединени TCP с kafka и заканчиваю..")
    logger.debug("="*20)

router = APIRouter(lifespan=lifespawn)

class BotMessage(BaseModel):
    message: str

@router.post("/ai_rules_message")
async def ai_rules(message: BotMessage):
    logger.debug("Получено сообщени от пользователя об изменении правил отправляю в оркестратор.")
    try:
        result = await orkestr_func(message=message.message)
        logger.debug("Успешно отправлено в сервис изменения правил.")
        return JSONResponse(status_code=200, content={"status": result})
    except Exception as e:
        logger.error(f"Не удалось отправить в сервис извлечения правил. {e}")
        raise HTTPException(status_code=500, detail=str(e))
