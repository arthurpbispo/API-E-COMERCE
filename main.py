from fastapi import FastAPI
from api.rota_autenticar import router as rota_autenticar
from utils.banco import criar_tabelas

app = FastAPI()
app.include_router(rota_autenticar)

criar_tabelas()




