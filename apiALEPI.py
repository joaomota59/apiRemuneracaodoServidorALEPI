from alepiLibrary import AlepiLibrary
from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel

app = FastAPI(title="API ALEPI", description="API para consulta da Remuneração do Servidor", version="0.1.0")

api = AlepiLibrary()

class Item(BaseModel):
    id: str
    value: str

class Message(BaseModel):
    message: str

@app.get("/folha", status_code=status.HTTP_200_OK, responses={404: {"model": Message}})
async def read_item(
    response: Response,
    ano: int = Query(2023, description="Ano da Folha de Pagamento"), 
    mes: int = Query(1, description="Mês da Folha de Pagamento 1=Janeiro, 2=Fevereiro, 3=Março ..."), 
    page: int = Query(1, description="Paginação da Folha de pagamento 1=Primeira página, 2=Segunda página ...")
    ):

    folhaRef = api.getFolhaPagamento(ano = ano, mes = mes,page = page)

    if folhaRef[0] == "Mês não disponível": response.status_code = 404

    return {
        "folha": folhaRef[0],
        "quantidadePaginas": folhaRef[1]
    }

@app.get("/referencias", status_code=status.HTTP_200_OK)
async def read_item():
    ref = api.referenciasDisponiveis()
    return ref