import aiofiles
import json

async def get_restrict_func(camera_id: int):
    async with aiofiles.open("app/rules/rules.json", "r") as f:
        data = await f.read()
        rules = json.loads(data)
        restriction = rules["cameras"][str(camera_id)]["restrictions"]
        return restriction






