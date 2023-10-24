from aiogram.fsm.state import StatesGroup, State


class RegStudent(StatesGroup):
    login = State()
    password = State()
