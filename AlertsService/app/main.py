from app.apis import changerulesapi
from app.apis import changecoordinates
from app.apis import getcoordinatesapi
from app.apis import getrestrictionsapi
from app.apis import addcameraapi
from fastapi import FastAPI
import uvicorn
import app.services.kafkaconsume

app = FastAPI()
app.include_router(router=changerulesapi.router)
app.include_router(router=changecoordinates.router)
app.include_router(router=getcoordinatesapi.router)
app.include_router(router=getrestrictionsapi.router)
app.include_router(router=addcameraapi.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8002, reload=False)