import aiofiles
import json

async def add_camera_func(camera_id: int, coordinates: list, place: str):
    async with aiofiles.open("app/rules/rules.json", "r") as f:
        data = await f.read()
        rules = json.loads(data)
        rules["cameras"][str(camera_id)] = {
            "coordinates": coordinates,
            "rules": {
                "Пехота": {"threshold": 2},
                "Танк": {"threshold": 2},
                "БМП (Боевая Машина Пехоты)": {"threshold": 2},
                "БТР (Бронетранспортер)": {"threshold": 2},
                "Бронемашина": {"threshold": 2},
                "Артиллерия": {"threshold": 2},
                "РСЗО (Ракетная Система Залпового Огня)": {"threshold": 2},
                "БПЛА (Беспилотный Летательный Аппарат)": {"threshold": 2},
            },
            "restrictions": place
        }
    async with aiofiles.open("app/rules/rules.json", "w") as f:
        await f.write(json.dumps(rules))






