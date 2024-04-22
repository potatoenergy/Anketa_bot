from aiogram.fsm.state import StatesGroup, State


class MegaphoneStates(StatesGroup):
    text_type = State()
    pic_text_type = State()
    gif_text_type = State()
