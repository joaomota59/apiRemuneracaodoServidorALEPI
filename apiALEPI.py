from alepiLibrary import AlepiLibrary
from fastapi import FastAPI, Query

app = FastAPI(title="API ALEPI", description="API para consulta da Remuneração do Servidor", version="0.1.0")

api = AlepiLibrary()

@app.get("/folha")
async def read_item( ano : int = 2023, mes : int = 1, page : int = 1):

    folhaRef = api.getFolhaPagamento(ano = ano, mes = mes,page = page)

    return {
        "folha": folhaRef[0],
        "quantidadePaginas": folhaRef[1]
    }

@app.get("/referencias")
async def read_item():
    ref = api.referenciasDisponiveis()
    return ref