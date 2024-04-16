from datetime import datetime
from functools import cache

import asyncpg
from fastapi import FastAPI, Response
from fastapi.responses import ORJSONResponse, StreamingResponse

app = FastAPI(
    default_response_class=ORJSONResponse
)


@app.get("/")
async def read_root():
    return [{"username": "user" + str(i), "id": i, "timestamp": datetime.now()} for i in range(1000)]


@cache
def get_items():
    return [{"username": "user" + str(i), "id": i, "timestamp": datetime.now()} for i in range(1000)]


@app.get("/cached")
async def read_cached():
    return get_items()


@app.get("/status")
async def response_status():
    return Response(status_code=200)


@app.get("/db_obj")
async def db_obj():
    conn = await asyncpg.connect(user="postgres", database="testing", host="localhost")

    values = await conn.fetch("SELECT * FROM USERS")
    await conn.close()
    return values


@app.get("/db_json")
async def db_json():
    conn = await asyncpg.connect(user="postgres", database="testing", host="localhost")
    query = "select json_agg(c) from (select * from users) as c"
    values = await conn.fetchrow(query)
    await conn.close()
    return StreamingResponse(content=values, media_type="application/json")
