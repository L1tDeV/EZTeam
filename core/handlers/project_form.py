from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.statesproject import ProjectSteps
from core.utils.callbackdata import QueryInfo

db_projects = ['Паркоматика']
db_answers=['Вот подробности о проекте <b>Паркоматика</b>:\nПаркоматика - инструмент для менеджмента и автоматизации оплаты парковок в Москве, Санкт-Петербурге и других городах.\nПроектом занимаются:\n\n✔️Аркадий Котов +7-960-643-28-96\n\nУ них ты можешь узнать о проекте больше, чем знаю я.']

def find_answer(project, db_projects,db_answers):
    if project in db_projects:
        return f'{db_answers[db_projects.index(project)]}'
    else:
        return f'Что-то не припоминаю такого проекта🤔'


async def get_project_form(message:Message, state:FSMContext):
    await message.answer(f'Ты хочешь узнать о проектах компании? Хорошо, я тебе помогу.\nУ нас есть следующие проекты:\n\n🅿️Паркоматика\n\nЧтобы узнать о проекте поподробнее, введи его название.')
    await state.set_state(ProjectSteps.GET_PROJECT)

async def get_project(message:Message, state:FSMContext):
    txt=message.text
    await message.answer(find_answer(txt, db_projects,db_answers))
    await state.clear()