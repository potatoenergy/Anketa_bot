# Импортируем необходимые модули
import re

from aiogram import F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import SessionLocal
from loader import bot, dp
from models import People
from states import data_collection
from utils import queries
from utils.notify import notify_admins


# Обработчик для кнопок "yes" и "no" при повторном заполнении анкеты
@dp.callback_query(F.data.in_(["yes", "no"]))
async def handle_repeat_choice(callback_query: types.CallbackQuery,
                               state: FSMContext):
    message_id = callback_query.message.message_id
    if callback_query.data == "yes":
        # Если пользователь выбрал "yes", спрашиваем его имя
        await callback_query.message.answer(
            "Давай познакомимся: Как тебя зовут?")
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
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Да", callback_data="yes")
            ], [InlineKeyboardButton(text="Нет", callback_data="no")]])
            await message.answer(
                "Вы уже заполнили анкету. Хотите заполнить ее снова?",
                reply_markup=keyboard)
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
        await state.update_data(
            act_city=f'{message.location.latitude}, {message.location.longitude}'
        )
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
        await message.answer(
            "Пожалуйста, введите корректный возраст (число от 1 до 100)")


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
    # Проверяем, есть ли у пользователя Username
    if message.from_user.username:
        # Если у пользователя есть Username, предлагаем ему разрешить использовать его для связи
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Да", callback_data="yes_username")
        ], [
            InlineKeyboardButton(text="Нет", callback_data="no_username")
        ]])
        await message.answer(
            f"Хотите разрешить использовать ваш Username ({message.from_user.username}) для связи?",
            reply_markup=keyboard)
        await state.set_state(data_collection.Form.act_contact)
    else:
        # Если у пользователя нет Username, предлагаем ему указать другой способ связи
        await message.answer("Пожалуйста, укажите удобный способ связи с вами.")
        await state.set_state(data_collection.Form.act_contact)

# Обработчик для выбора использования Username для связи
@dp.callback_query(F.data.in_(["yes_username", "no_username"]))
async def handle_username_choice(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "yes_username":
        # Если пользователь разрешил использовать свой Username, сохраняем его в состоянии
        await state.update_data(act_contact=f"https://t.me/{callback_query.from_user.username}")
        await save_data_and_notify_admins(callback_query, state)
    else:
        # Если пользователь не хочет использовать свой Username, предлагаем ему указать другой способ связи
        await callback_query.message.answer("Пожалуйста, укажите удобный способ связи с вами.")
    # Удаляем сообщение с кнопками "yes" и "no"
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

# Обработчик для сбора контактной информации пользователя (сообщение)
@dp.message(data_collection.Form.act_contact)
async def process_contact_message(message: types.Message, state: FSMContext):
    contact_info = message.text
    if is_valid_url(contact_info) or is_valid_email(contact_info):
        # Если введенная информация является ссылкой или email, сохраняем ее в состоянии
        await state.update_data(act_contact=contact_info)
        await save_data_and_notify_admins(message, state)
    else:
        # Если введенная информация не является ссылкой или email, отправляем сообщение об ошибке
        await message.answer("Пожалуйста, введите корректную ссылку или email.")

# Функция для проверки, является ли строка ссылкой
def is_valid_url(url):
    pattern = re.compile(
        r'^(https?://)?'  # schema
        r'((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|'  # domain name
        r'((\d{1,3}\.){3}\d{1,3}))'  # OR ip (v4) address
        r'(\:\d+)?(\/[-a-z\d%_.~+]*)*'  # port and path
        r'(\?[;&a-z\d%_.~+=-]*)?'  # query string
        r'(\#[-a-z\d_]*)?$', re.IGNORECASE)  # fragment locator
    return bool(pattern.match(url))

# Функция для проверки, является ли строка email
def is_valid_email(email):
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email))

# Функция для сохранения данных в базу данных и отправки уведомления администраторам
async def save_data_and_notify_admins(message: types.Message, state: FSMContext):
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
        people.act_contact = user_data['act_contact']
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
    notification_message += f"Навыки: {user_data['act_skills']}\n"
    notification_message += f"Контакт: {user_data['act_contact']}"
    # Отправляем сообщение администраторам
    await notify_admins(notification_message)
