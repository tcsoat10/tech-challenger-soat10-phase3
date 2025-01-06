from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.core.exceptions.base_exception import BaseAppException
from src.adapters.driver.api.v1.routes.health_check import router as health_check_router
from src.adapters.driver.api.v1.routes.category_routes import router as category_routes
from src.adapters.driver.api.v1.routes.product_routes import router as product_routes
from src.adapters.driver.api.v1.routes.permission_routes import router as permission_routes
from src.adapters.driver.api.v1.routes.profile_routes import router as profile_routes
from src.adapters.driver.api.v1.routes.order_item_routes import router as order_item_routes
from src.adapters.driver.api.v1.routes.profile_permission_routes import router as profile_permission_routes
from src.adapters.driver.api.v1.routes.payment_method_routes import router as payment_method_routes
from src.adapters.driver.api.v1.routes.role_routes import router as role_routes

app = FastAPI(title="Tech Challenger SOAT10 - FIAP")

@app.exception_handler(BaseAppException)
async def global_app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Ocorreu um erro inesperado no servidor."},
    )

# Adicionando rotas da versão 1
app.include_router(health_check_router, prefix="/api/v1")
app.include_router(category_routes, prefix="/api/v1", tags=["categories"])
app.include_router(product_routes, prefix="/api/v1", tags=["products"])
app.include_router(order_item_routes, prefix="/api/v1", tags=["order-items"])
app.include_router(permission_routes, prefix="/api/v1", tags=["permissions"])
app.include_router(profile_routes, prefix="/api/v1", tags=["profiles"])
app.include_router(profile_permission_routes, prefix='/api/v1', tags=['profile-permissions'])
app.include_router(payment_method_routes, prefix="/api/v1", tags=["payment-methods"])
app.include_router(role_routes, prefix="/api/v1", tags=["roles"])
