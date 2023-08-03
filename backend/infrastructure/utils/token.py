from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError

from ..core.settings import Settings

settings = Settings()


def create_access_token(username: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {"sub": username}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        return username
    except JWTError:
        raise
