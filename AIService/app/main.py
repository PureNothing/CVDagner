from fastapi import FastAPI
from app.apis import aiapi
from app.apis import tenminreportapi
from app.apis import newcameraapi
import uvicorn
from app.services import kafkaconsume

app = FastAPI()
app.include_router(router=aiapi.router)
app.include_router(router=tenminreportapi.router)
app.include_router(router=newcameraapi.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8003, reload=False)