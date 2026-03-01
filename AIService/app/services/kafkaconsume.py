from app.core.kafkabroker import broker
from pydantic import BaseModel
from app.agentsfuncs.agentwithtools import tools_agent
from app.logger import logger

class Body(BaseModel):
    camera_id: int
    label: str
    count: int

@broker.subscriber("real_alerts")
async def alerts_ai_consumer(message: Body):
    try:
        logger.debug("Получено тревожное сообщение отправляю агенту для выбора инструмента..")
        mes_for_ai = f"На камере {message.camera_id}, замечено {message.count} {message.label}"
        await tools_agent(message=mes_for_ai)
        logger.debug("Успешно отправлено агенту.")
    except Exception as e:
        logger.error("Не удалось отправить тревожное сообщение агенту.")
        raise