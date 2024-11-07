# Импортируем необходимые модули
from aiogram import types, F
from aiogram.filters import StateFilter
from states import data_collection
from keyboards import default
from aiogram.fsm.context import FSMContext
from database import SessionLocal
from models import People
from utils import queries
from loader import dp, bot
from utils.notify import notify_admins
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Определяем обработчик для callback query с данными "yes" или "no"
@dp.callback_query(F.data.in_(["yes", "no"]))
async def handle_repeat_choice(callback_query: types.CallbackQuery, state: FSMContext):
    message_id = callback_query.message.message_id
    if callback_query.data == "yes":
        # Если пользователь выбрал "yes", спрашиваем его имя
        await callback_query.message.answer("Давай познакомимся: Как тебя зовут?")
        await state.set_state(data_collection.Form.act_full_name)
    else:
        # Если пользователь выбрал "no", завершаем опрос
        await callback_query.message.answer("Ок, тогда до свидания!")
        await state.clear()
    # Удаляем сообщение с кнопками "yes" и "no"
    await bot.delete_message(callback_query.from_user.id, message_id)

# Определяем обработчик для сообщения с текстом "Заполнить анкету"
@dp.message(StateFilter(None), F.text == 'Заполнить анкету')
async def collect_start(message: types.Message, state: FSMContext):
    async with SessionLocal() as session:
        # Проверяем, заполнял ли пользователь анкету ранее
        people = await queries.get_people(session, message.from_user.id)
        if people is not None:
            # Если пользователь уже заполнял анкету, предлагаем ему заполнить ее снова
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Да", callback_data="yes")],
                [InlineKeyboardButton(text="Нет", callback_data="no")]
            ])
            await message.answer("Вы уже заполнили анкету. Хотите заполнить ее снова?", reply_markup=keyboard)
            await state.set_state(data_collection.Form.repeat)
        else:
            # Если пользователь еще не заполнял анкету, спрашиваем его имя
            await message.answer("Давай познакомимся: Как тебя зовут?")
            await state.set_state(data_collection.Form.act_full_name)

# Определяем обработчик для сообщения с текстом "Да" или "Нет" в состоянии "repeat"
@dp.message(data_collection.Form.repeat)
async def process_repeat(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        # Если пользователь выбрал "Да", спрашиваем его имя
        await message.answer("Давай познакомимся: Как тебя зовут?")
        await state.set_state(data_collection.Form.act_full_name)
    else:
        # Если пользователь выбрал "Нет", завершаем опрос
        await message.answer("Ок, тогда до свидания!")
        await state.clear()

# Определяем обработчик для сообщения с именем пользователя в состоянии "act_full_name"
@dp.message(data_collection.Form.act_full_name)
async def process_name(message: types.Message, state: FSMContext):
    # Сохраняем имя пользователя в состоянии
    await state.update_data(act_full_name=message.text)
    # Спрашиваем город пользователя
    await message.answer("Введите город")
    await state.set_state(data_collection.Form.act_city)

# Определяем обработчик для сообщения с городом пользователя в состоянии "act_city"
@dp.message(data_collection.Form.act_city)
async def process_city(message: types.Message, state: FSMContext):
    if message.location:
        # Если пользователь отправил геолокацию, сохраняем ее в состоянии
        await state.update_data(act_city=f'{message.location.latitude}, {message.location.longitude}')
    else:
        # Если пользователь отправил текстовое сообщение, сохраняем его в состоянии
        await state.update_data(act_city=message.text)
    # Спрашиваем возраст пользователя
    await message.answer("Введите возраст")
    await state.set_state(data_collection.Form.act_age)

# Определяем обработчик для сообщения с возрастом пользователя в состоянии "act_age"
@dp.message(data_collection.Form.act_age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        # Пытаемся преобразовать текстовое сообщение в число
        age = int(message.text)
        if age < 1 or age > 100:
            # Если число не в диапазоне от 1 до 100, выбрасываем исключение
            raise ValueError("Возраст должен быть от 1 до 100 лет")
        # Сохраняем возраст пользователя в состоянии
        await state.update_data(act_age=age)
        # Спрашиваем опыт работы пользователя
        await message.answer("Введите опыт работы")
        await state.set_state(data_collection.Form.act_work_experience)
    except ValueError:
        # Если преобразование не удалось, просим пользователя ввести корректный возраст
        await message.answer("Пожалуйста, введите корректный возраст (число от 1 до 100)")

# Определяем обработчики для сообщений с опытом работы, образованием и навыками пользователя
@dp.message(data_collection.Form.act_work_experience)
async def process_work_experience(message: types.Message, state: FSMContext):
    await state.update_data(act_work_experience=message.text)
    await message.answer("Введите образование")
    await state.set_state(data_collection.Form.act_education)

@dp.message(data_collection.Form.act_education)
async def process_education(message: types.Message, state: FSMContext):
    await state.update_data(act_education=message.text)
    await message.answer("Введите навыки")
    await state.set_state(data_collection.Form.act_skills)

@dp.message(data_collection.Form.act_skills)
async def process_skills(message: types.Message, state: FSMContext):
    await state.update_data(act_skills=message.text)
    # Получаем данные пользователя из состояния
    user_data = await state.get_data()

    async with SessionLocal() as session:
        # Проверяем, заполнял ли пользователь анкету ранее
        people = await queries.get_people(session, message.from_user.id)
        if people is None:
            # Если пользователь еще не заполнял анкету, создаем новую запись в базе данных
            people = People(act_tg_id=message.from_user.id)
            session.add(people)
            notification_header = "🆕 Новая заявка:"
        else:
            # Если пользователь уже заполнял анкету, обновляем существующую запись в базе данных
            notification_header = "✏️ Редактирование заявки:"
        # Обновляем данные пользователя в записи в базе данных
        people.act_full_name = user_data['act_full_name']
        people.act_city = user_data['act_city']
        people.act_age = user_data['act_age']
        people.act_work_experience = user_data['act_work_experience']
        people.act_education = user_data['act_education']
        people.act_skills = user_data['act_skills']
        await session.commit()

    # Благодарим пользователя за заполнение анкеты
    await message.answer("Спасибо за заполнение анкеты!")
    # Очищаем состояние пользователя
    await state.clear()

    # Формируем сообщение с данными пользователя для отправки администраторам
    notification_message = f"{notification_header}\n"
    notification_message += f"Пользователь: {message.from_user.id}\n"
    notification_message += f"Имя: {user_data['act_full_name']}\n"
    notification_message += f"Город: {user_data['act_city']}\n"
    notification_message += f"Возраст: {user_data['act_age']}\n"
    notification_message += f"Опыт работы: {user_data['act_work_experience']}\n"
    notification_message += f"Образование: {user_data['act_education']}\n"
    notification_message += f"Навыки: {user_data['act_skills']}"
    # Отправляем сообщение администраторам
    await notify_admins(notification_message)