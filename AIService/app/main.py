from fastapi import FastAPI
from app.apis.aiapi import router
import uvicorn
from app.services import kafkaconsume

app = FastAPI()
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8003, reload=False)