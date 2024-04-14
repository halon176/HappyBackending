from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    default_response_class=ORJSONResponse
)


@app.get("/")
async def read_root():
    return [{"username": "user" + str(i), "id": i, "timestamp": datetime.now()} for i in range(1000)]
