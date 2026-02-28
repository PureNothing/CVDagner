from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.logger import logger
from pydantic import BaseModel
from app.funcs.update_coordinates import update_coordinates_func

class Body(BaseModel):
    camera_id: int
    coordinates: list

router = APIRouter()

@router.post("/change_coordinates")
async def change_coordinates_funct(message: Body):
    try:
        logger.debug("Получен запрос на изменение коордиант, обрабатыва..")
        await update_coordinates_func(coordinates=message.coordinates, camera_id=message.camera_id)
        logger.debug("Коордианты успешно обновлены")
        return JSONResponse(status_code=200, content={"status": "Координаты успешно обновлены."})
    except Exception as e:
        logger.error(f"Ошибка при обновлении координат. {e}")
        raise HTTPException(status_code=500, detail=str(e))
