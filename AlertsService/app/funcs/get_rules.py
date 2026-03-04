import json
import aiofiles

async def get_rules_func(camera_id: int):
    async with aiofiles.open("app/rules/rules.json", "r", encoding="utf-8-sig") as f:
        data = await f.read()
        rules = json.loads(data)
        camera_rules = rules["cameras"][str(camera_id)]["rules"]
        return camera_rules