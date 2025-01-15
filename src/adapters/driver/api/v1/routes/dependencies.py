from typing import List, Optional
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.forbidden_exception import ForbiddenException
from src.core.utils.jwt_util import JWTUtil

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class PermissionChecker:
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = set(required_permissions)

    def __call__(self, request: Request, token: str = Depends(oauth2_scheme)):
        jwt_payload = JWTUtil.decode_token(token)

        profile = jwt_payload.get("profile", {})
        if not profile:
            raise BadRequestException(message="Invalid JWT payload: 'profile' must be a non-empty object.")

        permissions = profile.get("permissions", [])
        if not permissions or not isinstance(permissions, list):
            raise BadRequestException(message="Invalid JWT payload: 'permissions' must be a non-empty list.")
        
        profile_name = profile.get("name")

        user_permissions = set(permissions)

        if self.required_permissions.intersection(user_permissions):
            if profile_name in ["administrator"]:
                return (0, profile_name) # Unrestricted access to all resources.
            
            if profile_name in ["manager"]:
                return (1, profile_name)  # Limited access to own resources and unrestricted access to other resources.
            
            if profile_name in ["employee"]:
                return (2, profile_name) # Restricted access to own resources and unrestricted access to other resources.
            
            if profile_name in ["customer"]:
                return (3, profile_name) # Restricted access to own resources.
            
            if profile_name in ["anonymous"]:
                return (4, profile_name) # Restricted access to own resources.

        raise ForbiddenException(
            message="Forbidden: Missing required permissions or access is restricted to own resources."
        )
