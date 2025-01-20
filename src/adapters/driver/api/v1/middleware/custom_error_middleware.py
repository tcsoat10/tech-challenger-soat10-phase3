import logging
import traceback
from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.core.exceptions.utils import ErrorCode
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
            logging.error(f"Unhandled exception: {exc}")
            traceback.print_exc()

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": {
                        "code": str(ErrorCode.INTERNAL_SERVER_ERROR),
                        "message": "Internal server error",
                        "details": str(exc),
                    }
                }
            )
