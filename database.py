# Импортируем необходимые модули
import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# Создаем асинхронный движок базы данных
engine = create_async_engine("sqlite+aiosqlite:///./database.db", echo=True)
# Создаем фабрику асинхронных сессий
SessionLocal = async_sessionmaker(bind=engine)

# Определяем базовый класс для моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass

# Определяем функцию для создания таблиц в базе данных
async def create_tables() -> None:
    try:
        async with engine.begin() as conn:
            # Создаем таблицы в базе данных
            await conn.run_sync(Base.metadata.create_all)
        logging.info("Tables created successfully")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")
        raise e