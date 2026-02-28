from app.apis import changerulesapi
from app.apis import changecoordinates
from app.apis import getcoordinatesapi
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(router=changerulesapi.router)
app.include_router(router=changecoordinates.router)
app.include_router(router=getcoordinatesapi.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8002, reload=False)