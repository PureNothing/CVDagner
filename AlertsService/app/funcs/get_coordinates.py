import json
import aiofiles

async def get_coordinates_func(camera_id: int):
    async with aiofiles.open("app/rules/rules.json", "r") as f:
        data = await f.read()
        rules = json.loads(data)
        camera_coordinates = rules["cameras"][str(camera_id)]["coordinates"]
        return camera_coordinates

