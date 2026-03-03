from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.logger import logger
from pydantic import BaseModel
from app.agentsfuncs.agentreporter import agent_report_func

router = APIRouter()

class BotMessage(BaseModel):
    report: str

@router.post("/ai_report_parse")
async def ai_report_parsee(message: BotMessage):
    logger.debug("Получен поный отчет пробую отдать ллм и предоставить проанализрованный.")
    try:
        agent_report = await agent_report_func(message.report)
        logger.debug("Отчет успешно проанализирован, результат анализа вовращаю..")
        return JSONResponse(status_code=200, content={"report": agent_report})
    except Exception as e:
        logger.error(f"Отчет не удалось проанилизировать и вернуть результатю. {e}")
        raise HTTPException (status_code=500, detail=str(e))