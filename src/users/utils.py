from src.settings import settings
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def encode_token(
        payload: dict,
        expire_timedelta: timedelta | None = None
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=settings.auth.expire_access_token_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        payload=payload,
        key=settings.auth.secret_key.read_text(),
        algorithm=settings.auth.algorithm
    )
    return encoded


def decode_jwt(
    token: str | bytes
) -> dict:
    decoded = jwt.decode(
        jwt=token,
        key=settings.auth.public_key.read_text(),
        algorithms=[settings.auth.algorithm],
    )
    return decoded


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_token(
        payload=jwt_payload,
        expire_timedelta=expire_timedelta,
    )

def create_access_token(user) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
    )


def create_refresh_token(user) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth.expire_refresh_token_days),
    )

def hashing_password(password: str)-> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode(), salt=salt).decode()


def check_password(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password.encode())
