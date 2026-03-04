from app.core.addcameraprompt import ADDCAMERAPROMPT
from app.core.so import SONEWCAMERA
from app.logger import logger
from app.core.config import client

async def exctract_new_camera_func(message: str):
    try:
        logger.debug("Пришло сообщение от пользователя на добавление камеры пробые извлечь данные..")
        response = await client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": ADDCAMERAPROMPT},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"}
        )
        text = response.choices[0].message.content
        so = SONEWCAMERA.model_validate_json(text)
        logger.debug(f"Извлечённые факты: camera_id={so.camera_id}, coordinates={so.coordinates}, place={so.place}")
        logger.debug("Факты для добавления камеры успешно извлечены, отпраляю в сервис правил..")
        return so
    except Exception as e:
        logger.error("Не удалось извлечь факты для добавления камеры.")
        return "Не понял переформулируйте запрос."





