# Импортируем необходимые модули
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем объект Engine для подключения к базе данных
engine = create_engine("sqlite:///database.db")

# Создаем базовый класс для моделей
Base = declarative_base()


# Определяем модель User
class User(Base):
    """
    User model.
    """

    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    act_tg_id = Column(Integer, unique=True, nullable=False)
    act_username = Column(String, nullable=True)
    act_full_name = Column(String, nullable=True)


# Определяем модель People
class People(Base):
    """
    People model.
    """

    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    act_tg_id = Column(Integer, unique=True, nullable=False)
    act_full_name = Column(String, nullable=False)
    act_city = Column(String, nullable=True)
    act_age = Column(Float, nullable=True, default=None)
    act_work_experience = Column(String, nullable=True, default=None)
    act_education = Column(String, nullable=True, default=None)
    act_skills = Column(String, nullable=True, default=None)
    act_contact = Column(String, nullable=True, default=None)


# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем фабрику сессий
Session = sessionmaker(bind=engine)
# Создаем объект сессии
session = Session()
