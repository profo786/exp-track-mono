from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Decode JWT issued by auth service and return user id (sub)."""
    settings = get_settings()
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        sub = payload.get("sub")
        user_id = int(sub)
    except (JWTError, ValueError, TypeError):
        raise credentials_exc

    if user_id is None:
        raise credentials_exc

    return user_id
