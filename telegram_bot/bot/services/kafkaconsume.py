from bot.core.kafkabroker import broker
from bot.core.config import bot
from aiogram.exceptions import TelegramForbiddenError
from bot.logger import logger
from pydantic import BaseModel
from bot.core.config import BUDDY_ID, OWNER_ID

class AlertMessage(BaseModel):
    camera_id: int
    label: str
    count: int
    place: str
    coordinates: list

@broker.subscriber("real_alerts")
async def alert_messages(message: AlertMessage):
    text = (
        f"🚨 Тревога, порог превышен!\n\n"
        f"📹 Камера: {message.camera_id}\n\n"
         f"📍 Коордианаты:\n"
        f"{message.coordinates}\n\n"
        f"🏔️ Местность:\n"
        f"{message.place}\n\n"
        f"🎯 Обнаружено:\n\n"
        f"• {message.label}: {message.count} шт."
    )
    try:
        logger.debug("Получен алерт из сервиса алертов, отправляю пользователю.")
        await bot.send_message(
        chat_id=OWNER_ID,
        text=text,
        protect_content=True
        )
        await bot.send_message(
            chat_id=OWNER_ID,
            text=text,
            protect_content=True
        )
    except TelegramForbiddenError:
        logger.error("Пользователь заблокировал бота")
        raise
    except Exception as e:
        logger.error(f"Ошибка отправи алерта. {e}")
        raise
