from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.core.exceptions.base_exception import BaseAppException
from src.adapters.driver.api.v1.routes.health_check import router as health_check_router

app = FastAPI(title="Tech Challenger SOAT10 - FIAP")

@app.exception_handler(BaseAppException)
async def global_app_exception_handler(request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )

# Adicionando rotas da versão 1
app.include_router(health_check_router, prefix="/api/v1")
