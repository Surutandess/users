from pydantic import BaseModel, EmailStr
from typing import Optional


class UsersBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: Optional[bool] = False
    is_banned: Optional[bool] = False


class UsersCreate(UsersBase):
    password: Optional[str] = None


class UsersRead(UsersBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class UsersEdit(UsersCreate):
    pass


class TokenRead(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
