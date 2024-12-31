from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.core.exceptions.base_exception import BaseAppException
from src.adapters.driver.api.v1.routes.health_check import router as health_check_router
from src.adapters.driver.api.v1.routes.category_routes import router as category_routes
from src.adapters.driver.api.v1.routes.product_routes import router as product_routes
from src.adapters.driver.api.v1.routes.permission_routes import router as permission_routes

app = FastAPI(title="Tech Challenger SOAT10 - FIAP")

@app.exception_handler(BaseAppException)
async def global_app_exception_handler(request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )

# Adicionando rotas da versão 1
app.include_router(health_check_router, prefix="/api/v1")
app.include_router(category_routes, prefix="/api/v1", tags=["categories"])
app.include_router(product_routes, prefix="/api/v1", tags=["products"])
app.include_router(permission_routes, prefix="/api/v1", tags=["permissions"])
