from aiogram import F, types
from database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from models import People
from states.data_collection import Form
from aiogram.fsm.context import FSMContext
from loader import dp, bot


@dp.message(Form.photo)
async def process_photo_and_save_db(message: types.Message, state: FSMContext):
    try:
        photo_id = message.photo[-1].file_id
        await state.update_data(photo_id=photo_id)
        user_data = await state.get_data()

        async with SessionLocal() as session:
            result = await session.execute(
                select(People).where(People.telegram_user_id == message.from_user.id))
            existing_user = result.scalars().first()

            if existing_user:
                existing_user.full_name = user_data['name']
                existing_user.location = user_data['location']
                existing_user.photo_id = user_data['photo_id']
            else:
                new_user = People(telegram_user_id=message.from_user.id,
                                  full_name=user_data['name'],
                                  location=user_data['location'],
                                  photo_id=user_data['photo_id'])
                session.add(new_user)

            await session.commit()
            await session.flush()

        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=photo_id,
            caption=f"Вас зовут: {user_data['name']}\n"
                     f"Ваш адрес или геолокация: {user_data['location']}\n"
                     f"Ваше фото (прикрепленное ниже) сохранено в базе данных.\n"
                     f"Обязательно проверьте, нет ли ошибок, и благодарим за ответы!"
        )
        await state.clear()
    except SQLAlchemyError as e:
        await bot.send_message(message.from_user.id, text=f"Произошла ошибка при работе с базой данных: {e}")
    except Exception as e:
        await bot.send_message(message.from_user.id, text=f"Произошла неизвестная ошибка: {e}")

