from fastapi import Request, status
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.core.exceptions.utils import ErrorCode
from src.core.utils.jwt_util import JWTUtil
import logging

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        open_routes = [
            "/openapi.json",
            "/docs",
            "/docs/oauth2-redirect",
            "/redoc",
            "/api/v1/auth/customer/cpf",
            "/api/v1/auth/customer/anonymous",
            "/api/v1/auth/employee",
            "/api/v1/health"
        ]

        if any(request.url.path.startswith(route) for route in open_routes):
            return await call_next(request)

        bearer = HTTPBearer()
        try:
            token = await bearer(request)
            payload = JWTUtil.decode_token(token.credentials)
            request.state.user = payload
        except ValueError as e:
            logging.error(f"Unauthorized access: {e}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": {
                        "code": ErrorCode.UNAUTHORIZED.value,
                        "message": ErrorCode.UNAUTHORIZED.description,
                        "details": str(e),
                    }
                },
            )
        except Exception as e:
            logging.error(f"Forbidden access: {e}")
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "error": {
                        "code": ErrorCode.FORBIDDEN.value,
                        "message": ErrorCode.FORBIDDEN.description,
                        "details": str(e),
                    }
                },
            )

        return await call_next(request)
