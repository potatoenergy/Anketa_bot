# Импортируем необходимые модули
from models import People
from sqlalchemy import select

# Определяем функцию для получения пользователя из базы данных по его ID
async def get_user(session, tg_user):
    query = select(People).where(People.act_tg_id == tg_user)
    query_result = await session.execute(query)
    user = query_result.scalars().first()
    return user

# Определяем функцию для создания нового пользователя в базе данных
async def create_user(session, tg_user, tg_username, tg_fullname):
    user = People(act_tg_id=tg_user, act_full_name=tg_fullname, act_city=None, act_age=None, act_work_experience=None, act_education=None, act_skills=None)
    session.add(user)
    return True

# Определяем функцию для получения данных пользователя из базы данных по его ID
async def get_people(session, tg_user):
    query = select(People).where(People.act_tg_id == tg_user)
    query_result = await session.execute(query)
    people = query_result.scalars().first()
    return people