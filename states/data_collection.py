from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    location = State()
    photo = State()

