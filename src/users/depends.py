from src.database import async_session_maker
from sqlalchemy import select, update
from .schemas import UsersEdit
from .models import UsersORM
from .utils import hashing_password


async def find_one_user(username: str) -> UsersORM | None:
    async with async_session_maker() as session:
        stmt = select(UsersORM).where(UsersORM.username == username)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def add_new_user(user):
    async with async_session_maker() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def edit(data: dict, username: str):
    async with async_session_maker() as session:
        stmt = update(UsersORM).where(UsersORM.username == username).values(**data)
        await session.execute(stmt)
        await session.commit()

async def edit_one_user(username: str, model: UsersEdit):
    data = model.model_dump(exclude_unset=True)
    if data.get("password"):
        data.update(password=hashing_password(password=data.get("password")))
    await edit(username=username, data=data)
    edited_user = await find_one_user(username=username)
    return edited_user
