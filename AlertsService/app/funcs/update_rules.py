import aiofiles
import json
from app.core.config import LABELS
from app.logger import logger

async def update_rules_func(camera_id, label: str, threshold: int):
    try:
        if label in LABELS:
            async with aiofiles.open("app/rules/rules.json", "r") as f:
                data = await f.read()
                rules = json.loads(data)
                rules["cameras"][str(camera_id)]["rules"][str(label)]["threshold"] = threshold
            async with aiofiles.open("app/rules/rules.json", "w") as f:
                await f.write(json.dumps(rules))
        else:
            logger.error("Пришел неизестный лейбл, невозможно обновить.")
            raise ValueError(f"Неизвестный Лейбл {label}")
    except Exception as e:
        raise