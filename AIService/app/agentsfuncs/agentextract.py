from app.core.sgrpompt import SGR
from app.core.so import SO
from app.logger import logger
from app.core.config import client

async def exctract_rule(message: str):
    try:
        logger.debug("Пришло сообщение от пользователя пробую извлечь данные для обновления правил..")
        response = await client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SGR},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"}
        )
        text = response.choices[0].message.content
        so = SO.model_validate_json(text)
        logger.debug("Факты успешно извлечены из сообщения пользователя, отправляю в сервис справилами..")
        return so
    except Exception as e:
        logger.error("Ошибка при извлечении данных, отправляю пользователю просьбу переформулировать..")
        return "Не понял, переформулируйте запрос."