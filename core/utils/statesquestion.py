from aiogram.fsm.state import StatesGroup, State

class QuestionSteps(StatesGroup):
    GET_QUESTION = State()

class QueAnswAdd(StatesGroup):
    GET_QUESTION = State()
    GET_ANSWER = State()