from bot.handlers import commands
from bot.handlers import callbacks
from bot.handlers import messages
from aiogram import Dispatcher
from bot.core.config import bot
from bot.menus.buttonmenu import setup_menu
import asyncio
from bot.logger import logger
from bot.core.kafkabroker import broker
from bot.services import kafkaconume
from bot.services import kafkaconsumeactions


dp = Dispatcher()

@dp.startup()
async def on_strartup():
   logger.debug("Открываю TCP с kafka.")
   logger.debug("="*20)
   await setup_menu(bot=bot)
   await broker.start()

@dp.shutdown()
async def on_shutdown():
   await broker.stop()
   logger.debug("Закрываю TCP с кафка.")
   logger.debug("="*20)

dp.include_router(commands.router)
dp.include_router(callbacks.router)
dp.include_router(messages.router)

async def main():
   await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())