from aiogram.fsm.state import StatesGroup, State

class FindPeopleSteps(StatesGroup):
    GET_PEOPLE = State()