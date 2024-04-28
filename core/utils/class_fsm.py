from aiogram.fsm.state import State, StatesGroup


class FSMPost(StatesGroup):
    post = State()
