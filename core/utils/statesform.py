from aiogram.fsm.state import StatesGroup, State

class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_BIRTHDAY = State()
    GET_PHONE = State()
    GET_PROJECTS = State()