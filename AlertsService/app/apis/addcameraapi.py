from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.logger import logger
from pydantic import BaseModel
from app.funcs.add_camera import add_camera_func

class Body(BaseModel):
    camera_id: int
    coordinates: list
    place: str

router = APIRouter()

@router.post("/add_camera")
async def change_coordinates_funct(message: Body):
    try:
        logger.debug("Получен запрос на добавление камеры, обрабатываю..")
        await add_camera_func(coordinates=message.coordinates, camera_id=message.camera_id, place=message.place)
        logger.debug("Камера успешно добавлена")
        return JSONResponse(status_code=200, content={"status": "Камера успешно добавлена."})
    except Exception as e:
        logger.error(f"Ошибка при добавление камеры. {e}")
        raise HTTPException(status_code=500, detail=str(e))