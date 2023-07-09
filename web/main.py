from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from endpoints.link import router as parser_router
import uvicorn

app = FastAPI()

app.include_router(parser_router, tags=["Parser"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=False
    )
