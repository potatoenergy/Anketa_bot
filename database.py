from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///./database.db", echo=True)

SessionLocal = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def async_db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# SQLALCHEMY_DB_URL = 'sqlite:///./database.db'
#
# engine = create_engine(
#     SQLALCHEMY_DB_URL, connect_args={'check_same_thread': False}
# )
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
#
# def create_db():
#     Base.metadata.create_all(engine)
