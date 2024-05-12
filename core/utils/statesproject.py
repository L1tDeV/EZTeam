from aiogram.fsm.state import StatesGroup, State

class ProjectSteps(StatesGroup):
    GET_PROJECT = State()

class CreateProject(StatesGroup):
    GET_PROJECT = State()
    GET_DESCR = State()
    GET_PEOPLE = State()