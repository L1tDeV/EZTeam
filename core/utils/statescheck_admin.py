from aiogram.fsm.state import StatesGroup, State

class CheckStates(StatesGroup):
    GET_DEL_OR_ADD = State()
    GET_CHECKS_ID = State()

class AdminStates(StatesGroup):
    GET_DEL_OR_ADD = State()
    GET_ADMINS_ID = State()