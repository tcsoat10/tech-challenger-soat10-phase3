from fastapi import Request
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.exceptions.forbidden_exception import ForbiddenException
from src.core.exceptions.unauthorized_access_exception import UnauthorizedAccessException
from src.core.utils.jwt_util import JWTUtil

class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        open_routes = [
            "/openapi.json",
            "/docs",
            "/docs/oauth2-redirect",
            "/redoc",
            "/auth/customer/cpf",
            "/auth/customer/anonymous"
            "/auth/employee",
            "/api/v1/health"
        ]

        if any(request.url.path.startswith(route) for route in open_routes):
            return await call_next(request)

        bearer = HTTPBearer()
        try:
            token = await bearer(request)
            payload = JWTUtil.decode_token(token.credentials)
        except ValueError as e:
            raise UnauthorizedAccessException(details=str(e))
        except Exception:
            raise ForbiddenException()

        request.state.user = payload
        return await call_next(request)
