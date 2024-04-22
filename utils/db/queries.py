from sqlalchemy import select

import models


async def get_user(session, id_user):
    query = select(models.User).where(models.User.id_user == id_user)
    query_result = await session.execute(query)
    user = query_result.scalar_one_or_none()
    return user


async def create_user(session, id_user,
                      tg_username,
                      tg_fullname):
    user = models.User(id_user=id_user,
                       tg_username=tg_username,
                       tg_fullname=tg_fullname)

    session.add(user)

    return True
