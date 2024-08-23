from .utils import create_access_token, create_refresh_token, decode_jwt, hashing_password, check_password
from .depends import find_one_user, add_new_user
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from .schemas import UsersCreate
from typing import Annotated
from .models import UsersORM
from src.settings import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/account/sign/in/",
)

async def register_new_user(user: UsersCreate):
    data = user.model_dump()
    hashed_password = hashing_password(password=user.password)
    data.update(password=hashed_password)
    new_user = UsersORM(**data)
    answer = await add_new_user(user=new_user)
    return answer


async def login_user(username: str, password: str):
    creadentials = HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    one_user = await find_one_user(username=username)
    if one_user is None:
        raise creadentials
    if not check_password(hashed_password=one_user.password, password=password):
        raise creadentials
    access_token = create_access_token(user=one_user)
    refresh_token = create_refresh_token(user=one_user)
    return [access_token, refresh_token]


async def get_current_user_depends(token: Annotated[str, Depends(oauth2_scheme)]):
    decoded_token = decode_jwt(token=token)
    username: str = decoded_token.get("sub")
    current_user = await find_one_user(username=username)
    return current_user


async def get_super_user(user: UsersORM = Depends(get_current_user_depends)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

async def get_active_user(user: UsersORM = Depends(get_current_user_depends)):
    if user.is_banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user


async def add_super_user():
    one_user = await find_one_user(username=settings.ADMIN_USERNAME)
    if one_user is None:
        hashed_password = hashing_password(password=settings.ADMIN_PASSWORD)
        superuser_schemas = {
            "username": settings.ADMIN_USERNAME,
            "email": settings.ADMIN_EMAIL,
            "password": hashed_password,
            "is_admin": True,
            "is_banned": False,
        }
        superuser = UsersORM(**superuser_schemas)
        await add_new_user(user=superuser)
        print("Super user was created successfully")
    print("Super user was detected")
