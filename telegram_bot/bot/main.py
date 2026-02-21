from handlers import commands
from handlers import callbacks
from handlers import messages
from config import BOT_TOKEN
from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramForbiddenError
from menus.buttonmenu import setup_menu
import asyncio
from logger import logger

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def check_and_alert():
    #Проверяем услвоие, если Да , сообщаем
    while True:
      try:
        await bot.send_message(
          chat_id=1111215202,
          text="Тревога! На камере 1 обнаружена опасность!",
          protect_content=True
        )
      except TelegramForbiddenError:
         logger.error("Пользователь заблокировал бота")
      except Exception as e:
         logger.error(f"Ошибка {e}")
      await asyncio.sleep(60)

dp.include_router(commands.router)
dp.include_router(callbacks.router)
dp.include_router(messages.router)

async def main():
    await setup_menu(bot=bot)
    await asyncio.gather(
      check_and_alert(),
      dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())