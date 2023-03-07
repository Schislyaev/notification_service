"""
Сервис для эмуляции обработки токена АПИ.

Так как сервис использует авторизацию по токену через gRPC,
вся валидация проходит на стороне gRPC. Для того что бы
сохранить правильное отражение схемы в документации используется
урезанный функционал класса JWTBearer
"""

from datetime import datetime
from typing import Any

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.settings import settings


def decode_jwt(token: str) -> dict[str, Any] | None:
    try:
        decoded_token = jwt.decode(
            token,
            settings.jwt_secret.get_secret_value(),
            algorithms=[settings.jwt_algorithm.get_secret_value()])
        return decoded_token if datetime.fromtimestamp(decoded_token["exp"]) >= datetime.utcnow() else None
    except Exception:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        if settings.log_level == 'DEBUG':
            return True

        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except Exception:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
