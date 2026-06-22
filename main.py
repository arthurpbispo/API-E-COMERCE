from fastapi import FastAPI
from api.rota_autenticar import router as rota_autenticar
from api.rota_controle_estoque import router as rota_estoque
from utils.banco import criar_tabelas

app = FastAPI()
app.include_router(rota_autenticar)
app.include_router(rota_estoque)

criar_tabelas()




