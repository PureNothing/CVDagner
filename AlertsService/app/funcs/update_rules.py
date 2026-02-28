import aiofiles
import json

async def update_rules_func(camera_id, label: str, threshold: int):
    async with aiofiles.open("app/rules/rules.json", "r") as f:
        data = await f.read()
        rules = json.loads(data)
        rules["cameras"][str(camera_id)]["rules"][str(label)]["threshold"] = threshold
    async with aiofiles.open("app/rules/rules.json", "w") as f:
        await f.write(json.dumps(rules))