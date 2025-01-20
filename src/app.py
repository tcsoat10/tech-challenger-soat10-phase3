from fastapi import FastAPI
from src.adapters.driver.api.v1.middleware.auth_middleware import AuthMiddleware
from src.adapters.driver.api.v1.middleware.custom_error_middleware import CustomErrorMiddleware
from src.adapters.driver.api.v1.routes.health_check import router as health_check_router
from src.adapters.driver.api.v1.routes.category_routes import router as category_routes
from src.adapters.driver.api.v1.routes.product_routes import router as product_routes
from src.adapters.driver.api.v1.routes.permission_routes import router as permission_routes
from src.adapters.driver.api.v1.routes.profile_routes import router as profile_routes
from src.adapters.driver.api.v1.routes.order_item_routes import router as order_item_routes
from src.adapters.driver.api.v1.routes.profile_permission_routes import router as profile_permission_routes
from src.adapters.driver.api.v1.routes.payment_method_routes import router as payment_method_routes
from src.adapters.driver.api.v1.routes.role_routes import router as role_routes
from src.adapters.driver.api.v1.routes.payment_status_routes import router as payment_status_routes
from src.adapters.driver.api.v1.routes.user_routes import router as user_routes
from src.adapters.driver.api.v1.routes.user_profile_routes import router as user_profile_routes
from src.adapters.driver.api.v1.routes.person_routes import router as person_routes
from src.adapters.driver.api.v1.routes.customer_routes import router as customer_routes
from src.adapters.driver.api.v1.routes.employee_routes import router as employee_routes
from src.adapters.driver.api.v1.routes.order_status_routes import router as order_status_routes
from src.adapters.driver.api.v1.routes.order_routes import router as order_routes
from src.adapters.driver.api.v1.routes.auth_routes import router as auth_routes
from src.adapters.driver.api.v1.routes.payment_routes import router as payment_routes
from src.adapters.driver.api.v1.routes.order_payment_routes import router as order_payment_routes

app = FastAPI(title="Tech Challenger SOAT10 - FIAP")

app.add_middleware(CustomErrorMiddleware)
app.add_middleware(AuthMiddleware)

# Adicionando rotas da versão 1
app.include_router(health_check_router, prefix="/api/v1")
app.include_router(auth_routes, prefix="/api/v1", tags=['auth'])
app.include_router(category_routes, prefix="/api/v1", tags=["categories"])
app.include_router(product_routes, prefix="/api/v1", tags=["products"])
app.include_router(order_item_routes, prefix="/api/v1", tags=["order-items"])
app.include_router(permission_routes, prefix="/api/v1", tags=["permissions"])
app.include_router(profile_routes, prefix="/api/v1", tags=["profiles"])
app.include_router(profile_permission_routes, prefix='/api/v1', tags=['profile-permissions'])
app.include_router(payment_method_routes, prefix="/api/v1", tags=["payment-methods"])
app.include_router(role_routes, prefix="/api/v1", tags=["roles"])
app.include_router(payment_status_routes, prefix="/api/v1", tags=["payment-status"])
app.include_router(user_routes, prefix="/api/v1", tags=["user"])
app.include_router(user_profile_routes, prefix="/api/v1", tags=["user-profiles"])
app.include_router(person_routes, prefix="/api/v1", tags=["persons"])
app.include_router(customer_routes, prefix="/api/v1", tags=["customers"])
app.include_router(employee_routes, prefix="/api/v1", tags=["employees"])
app.include_router(order_status_routes, prefix="/api/v1", tags=["order-status"])
app.include_router(order_routes, prefix="/api/v1", tags=["order"])
app.include_router(payment_routes, prefix="/api/v1", tags=["payment"])
app.include_router(order_payment_routes, prefix="/api/v1", tags=["order-payment"])
