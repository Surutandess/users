from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from src.database import Model


class UsersORM(Model):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(length=1024), unique=True)
    email: Mapped[str] = mapped_column(String(length=356), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
