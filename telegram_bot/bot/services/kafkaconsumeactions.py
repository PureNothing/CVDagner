from bot.core.kafkabroker import broker
from pydantic import BaseModel
from bot.core.config import bot
from bot.logger import logger
from bot.core.config import OWNER_ID, BUDDY_ID
from aiogram.exceptions import TelegramForbiddenError

class MSG(BaseModel):
    action: str

@broker.subscriber("agent_actions")
async def agent_action(message: MSG):
    text = f"🤖 Агент выполнил действие:\n⚡️ {message.action}"
    try:
        logger.debug("Получено действие агента, отправляю пользователю.")
        await bot.send_message(
        chat_id=OWNER_ID,
        text=text,
        protect_content=False
        )
        await bot.send_message(
            chat_id=OWNER_ID,
            text=text,
            protect_content=False
        )
        logger.debug("Действие агента отправлено пользователю.")
    except TelegramForbiddenError:
        logger.error("Пользователь заблокировал бота")
        raise
    except Exception as e:
        logger.error(f"Ошибка отправи действия агента алерта. {e}")
        raise