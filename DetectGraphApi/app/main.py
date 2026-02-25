from app.core.config import check_env
import os
from app.graphapi.graphapi import router
import uvicorn
from fastapi import FastAPI
import app.services.kafkaconsume


if not os.getenv("ENV_CHECKED"):
    check_env()
    os.environ["ENV_CHECKED"] = "1"



app = FastAPI()
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8001, reload=True)