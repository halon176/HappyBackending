from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello():
    return {"saluto": "ciao"}


@app.get("/auguri/{nome}")
async def auguri(nome):
    return {"AUGURI": nome}
