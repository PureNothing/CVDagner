from app.core.reportprompt import REPORTPROMPT
from app.logger import logger
from app.core.config import client

async def agent_report_func(report: str) -> str:
    try:
        logger.debug("Пришел запрос на анализ и преобразование отчета через ллм, отправляю..")
        response = await client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": REPORTPROMPT},
                {"role": "user", "content": report}
            ]
        )
        text = response.choices[0].message.content
        logger.debug("Проанализированный отчет получен от агента, возвращаю..")
        return text
    except Exception as e:
        logger.error(f"Не удалось проанализировать отчет агенту и вернуть..")
        raise





