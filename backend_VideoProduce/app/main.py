from fastapi import FastAPI
from app.api import post
import uvicorn
import os
from app.core.config import check_env

if not os.getenv("ENV_CHECKED"):
    check_env()
    os.environ["ENV_CHECKED"] = "1"

app = FastAPI()

app.include_router(post.router)

if __name__=="__main__":
    uvicorn.run("app.main:app", port=8000, reload=False)