from bot.handlers import commands
from bot.handlers import callbacks
from bot.handlers import messages
from aiogram import Dispatcher
from bot.core.config import bot
from bot.menus.buttonmenu import setup_menu
import asyncio
from bot.celery.celeryapp import app
from bot.logger import logger
from bot.core.kafkabroker import broker
from bot.services import kafkaconsume
from bot.services import kafkaconsumeactions
from bot.celery import tasks
import threading

def start_worker():
   app.worker_main(argv=['worker', '--loglevel=info', '--pool=solo'])

def start_beat():
   app.Beat(loglevel="info").run()


dp = Dispatcher()

@dp.startup()
async def on_strartup():
   threading.Thread(target=start_worker, daemon=True).start()
   threading.Thread(target=start_beat, daemon=True).start()
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