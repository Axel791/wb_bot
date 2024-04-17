from aiogram.fsm.state import State, StatesGroup


class StatForm(StatesGroup):
    date_from = State()
    flag = State()
