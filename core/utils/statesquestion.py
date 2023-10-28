from aiogram.fsm.state import StatesGroup, State

class QuestionSteps(StatesGroup):
    GET_QUESTION = State()