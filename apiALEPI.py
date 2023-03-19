from alepiLibrary import referenciasDisponiveis
from fastapi import FastAPI, Query

app = FastAPI(title="API ALEPI", description="API para consulta da Remuneração do Servidor", version="0.1.0")

@app.get("/folha")
async def read_item():
    return {'referencias':'s'}

@app.get("/referencias")
async def read_item():
    return referenciasDisponiveis()