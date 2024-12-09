from fastapi import FastAPI
from src.adapters.api.v1.routes.health_check import router as health_check_router

app = FastAPI(title="Tech Challenger SOAT10 - FIAP")

# Adicionando rotas da versão 1
app.include_router(health_check_router, prefix="/api/v1")
