from datetime import datetime , timezone, timedelta
import jwt

from core.config import settings

def _create_token(data: dict, secret_key: str, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.jwt.algorithm)
    return encoded_jwt


def create_access_token(data: dict):
    delta = timedelta(minutes=settings.jwt.access_secret_minutes)
    return _create_token(
        data=data, secret_key=settings.jwt.access_secret_key, expires_delta=delta
    )


def create_refresh_token(data: dict):
    delta = timedelta(days=settings.jwt.refresh_secret_day)
    return _create_token(
        data=data, secret_key=settings.jwt.refresh_secret_key, expires_delta=delta
    )


async def validate_token(access_token: str):
    pass
    
    # payload = jwt.decode(
    #     access_token,
    #     settings.jwt.access_secret_key,
    #     algorithms=[settings.jwt.algorithm]
    # )
    
    
    

