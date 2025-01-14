from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.forbidden_exception import ForbiddenException
from src.core.utils.jwt_util import JWTUtil

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, request: Request, token: str = Depends(oauth2_scheme)):
        jwt_payload = JWTUtil.decode_token(token)

        permissions = jwt_payload.get("permissions", [])
        if not isinstance(permissions, list):
            raise BadRequestException(message="Invalid JWT payload: 'permissions' must be a list.")

        if not JWTUtil.validate_permissions(jwt_payload, self.required_permission):
            raise ForbiddenException(message=f"Forbidden: Missing required permission '{self.required_permission}'.")
