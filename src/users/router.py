from .auth import register_new_user, login_user, get_active_user
from .depends import edit_one_user
from fastapi import status, Form, APIRouter, Response, Depends
from .schemas import UsersRead, UsersCreate, TokenRead, UsersEdit
from .models import UsersORM


user_router = APIRouter(
    prefix="/account",
    tags=["users"]
)


@user_router.post(
    path="/register/new/user/",
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


#should create endpoint for logout
@user_router.post("/logout/")
async def logout_user(response: Response, user: UsersORM = Depends(get_active_user)):
    print(f"User with username {user.username} was logout")
    response.delete_cookie(key="access_token", domain="localhost")
    response.delete_cookie(key="refresh_token", domain="localhost")


@user_router.get(
    path="/get/current/user/",
    response_model=UsersRead,
)
async def get_current_user(user: UsersORM = Depends(get_active_user)):
    return user


@user_router.patch(path="/edt/one/user/", response_model=UsersRead)
async def edit_user(schemas: UsersEdit,user: UsersORM = Depends(get_active_user)):
    user_edit = await edit_one_user(username=user.username, model=schemas)
    return user_edit
