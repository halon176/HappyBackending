from fastapi import FastAPI, Depends, Request, HTTPException

app = FastAPI()


async def esempio_yield():
    print("Inizio sessione")
    session = "sessioneeee!"
    yield session
    print("Fine sessione")


@app.get("/elenco")
async def elenco(a=Depends(esempio_yield)):
    return a


async def param(a: int, b: int):
    return {"a": a, "b": b}


@app.get("/elenco_con_parametri")
async def elenco_par(ingresso: dict = Depends(param)):
    return ingresso


class ABClass:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b


@app.get("/elenco_class")
async def elenco_class(ab_params: ABClass = Depends()):
    return ab_params


class AuthGuard:
    def __init__(self, nome: str):
        self.nome = nome

    def __call__(self, request: Request):
        if "cookie_sicuro" not in request.cookies:
            raise HTTPException(status_code=401)
        return True


oggetto_autenticazione = AuthGuard("guardiano")


@app.get("/super_privato", dependencies=[Depends(oggetto_autenticazione)])
async def super_privata():
    return "dati super privati"
