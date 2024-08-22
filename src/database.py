from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.settings import settings


class Model(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


async_engine = create_async_engine(url=settings.DB_URL)
async_session_maker = async_sessionmaker(bind=async_engine)
