from requests import Request

from .auth import register_new_user, login_user, oauth2_scheme, get_current_user_depends
from fastapi import status, Form, APIRouter, Response, Depends
from .schemas import UsersRead, UsersCreate, TokenRead
from typing import Annotated


user_router = APIRouter(
    prefix="/account",
    tags=["users"]
)


@user_router.post(
    path="/",
    response_model=UsersRead,
    status_code=status.HTTP_201_CREATED
)
async def register_user(users: UsersCreate):
    user = await register_new_user(user=users)
    return user


@user_router.post(
    path="/sign/in/",
    response_model=TokenRead
)
async def sign_in_user(
        response: Response,
        username: str =  Form(),
        password: str = Form()
):
    tokens = await login_user(username=username, password=password)
    response.set_cookie(key="access_token", value=f"Bearer {tokens[0]}", httponly=True)
    response.set_cookie(key="refresh_token", value=f"Bearer {tokens[1]}", httponly=True)
    return {"access_token": tokens[0], "refresh_token": tokens[1]}


@user_router.get(
    path="/get/current/user/",
    response_model=UsersRead,
)
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    one_user = await get_current_user_depends(token=token)
    return one_user
