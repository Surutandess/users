from src.database import async_session_maker
from sqlalchemy import select
from .models import UsersORM


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
