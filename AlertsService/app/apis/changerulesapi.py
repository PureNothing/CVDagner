from fastapi import APIRouter, HTTPException
from app.logger import logger
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.kafkabroker import broker
from pydantic import BaseModel
from app.funcs.update_rules import update_rules_func

@asynccontextmanager
async def lifespawn(router):
    try:
        logger.debug("="*20)
        logger.debug("Открываю TCP соединение с Kafka перед запуском..")
        await broker.start()
    except Exception as e:
        logger.error(f"Не удалось открыть соединение с Kafka. {e}")
    yield
    logger.debug("Закрываю соединение с Kafka перед выключением.")
    await broker.stop()
    logger.debug("Соединение с Kafka успешно закрыто.")
    logger.debug("="*20)

router = APIRouter(lifespan=lifespawn)

class Body(BaseModel):
    camera_id: int
    label: str
    threshold: int

@router.post("/change_rules")
async def change_rules(message: Body):
    logger.debug("Получено сообщение со стороны бота на обновление правил, обрабатываю..")
    try:
        result = await update_rules_func(camera_id=message.camera_id, label=message.label, threshold=message.threshold)
        if isinstance(result, str):
            return JSONResponse(status_code=400, content={"status": result})
        logger.debug("Правила успешно изменены.")
        return JSONResponse(status_code=200, content={"status": "rules_changed"})
    except Exception as e:
        logger.error(f"Не удалось изменить правила. {e}")
        raise HTTPException(status_code=500, detail=str(e))






