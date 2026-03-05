from bot.celery.celeryapp import app
import asyncio
from bot.logger import logger
from bot.parsers.full_report_parser import report_format_answer
from bot.utils.requests_func import get_full_and_info_final
from bot.core.config import AI_REPORT_PARSE
import aiohttp
from aiogram import Bot
from bot.core.config import BOT_TOKEN
from bot.core.config import BUDDY_ID, OWNER_ID
from aiogram.exceptions import TelegramForbiddenError
from telegramify_markdown import markdownify


@app.task(
    bind=True,
    max_retries=5,
    default_retry_delay=60,
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    autoretry_for=(ValueError,),
    acks_late=True,
    reject_on_worker_lost=True
    )
def full_10_report_task(self):
    task_bot = Bot(token=BOT_TOKEN)
    async def async_logic():
        try:
            logger.debug("Пришло время получать каждй 10 минут отчет..")
            full_report, cor_res = await get_full_and_info_final()
            parsed_report = report_format_answer(response=full_report, cor_plc=cor_res)
            async with aiohttp.ClientSession() as session:
                async with session.post(url=AI_REPORT_PARSE, json={"report": parsed_report}) as response:
                    result = await response.json()
            logger.debug("Отчет получен от агента, отправляю пользователю..")
            converted_text = markdownify(result['report'])
            await task_bot.send_message(
                chat_id=OWNER_ID,
                text=converted_text,
                parse_mode="MarkdownV2",
                protect_content=False
            )
            logger.debug("Полный отчет отпрален в чат телеграм.")
        except TelegramForbiddenError:
            logger.error("Пользователь заблокировал бота не удалось отпавить отчет")
        except Exception as e:
            logger.error(f"Не удалось отпавить 10 минутный отчет. {e}")
        finally:
            await task_bot.close()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop=loop)
    try:
        loop.run_until_complete(async_logic())
    finally:
        loop.close()



