from fastapi import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.core.exceptions.base_exception import BaseAppException

class CustomErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except BaseAppException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "code": exc.detail.get("code"),
                        "message": exc.detail.get("message"),
                        "details": exc.detail.get("details"),
                    }
                },
            )
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={"error": {"message": "Internal server error"}}
            )
