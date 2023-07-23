from fastapi import FastAPI, Request, Response
from jsonrpcserver import Result, Success, dispatch, method
import uvicorn
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()


@method
def ping() -> Result:
    return Success("pong")


@app.post("/")
async def index(request: Request):
    return Response(dispatch(await request.body()))


if __name__ == "__main__":
    PORT = os.getenv("PORT")
    uvicorn.run("main:app", port=5000, reload=True)
