import aiofiles
import json

async def update_coordinates_func(camera_id: int, coordinates: list):
    async with aiofiles.open("app/rules/rules.json", "r", encoding="utf-8-sig") as f:
        data = await f.read()
        rules = json.loads(data)
        rules["cameras"][str(camera_id)]["coordinates"] = coordinates
    async with aiofiles.open("app/rules/rules.json", "w", encoding="utf-8-sig") as f:
        await f.write(json.dumps(rules, ensure_ascii=False, indent=2))



