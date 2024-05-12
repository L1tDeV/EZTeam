from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.statesproject import ProjectSteps, CreateProject
from core.utils.callbackdata import QueryInfo
from sqlite_aio.sqlite import get_project_lst, get_check_lst, is_admin, create_project_db

# db_projects = ['Паркоматика']
# db_answers=['Паркоматика - инструмент для менеджмента и автоматизации оплаты парковок в Москве, Санкт-Петербурге и других городах.|\n\n✔️Котов Аркадий Дмитриевич']



def find_answer(project, db_projects,db_answers):
    if project in db_projects:
        need_el = list(db_answers[db_projects.index(project)].split('|'))
        return f'Вот подробности о проекте <b>{project}</b>:\n\n{need_el[0]}\n\nПроектом занимаются:{need_el[1]}\n\nУ них ты можешь узнать о проекте больше, чем знаю я.'
    else:
        return f'Что-то не припоминаю такого проекта🤔'

async def get_project_form(message:Message, state:FSMContext):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl = await get_check_lst(user_id, username)
    if fl:
        global db_projects, db_answers
        db_projects, db_answers = get_project_lst()
        lst_proj = ''
        for el in db_projects:
            lst_proj+='\n✔️'+el
        answ = f'✨Ты хочешь узнать о проектах компании? Хорошо, я тебе помогу.\n\n🌐У нас есть следующие проекты:\n{lst_proj}\n\nЧтобы узнать о проекте поподробнее, введи его название.'
        await message.answer(answ)
        await state.set_state(ProjectSteps.GET_PROJECT)
    else:
        await message.answer(f'{message.from_user.first_name}, этот бот не для вас :(')

async def get_project(message:Message, state:FSMContext):
    txt=message.text
    await message.answer(find_answer(txt, db_projects,db_answers))
    await state.clear()

async def get_create_project_form(message:Message, state:FSMContext):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl_1 = await get_check_lst(user_id, username)
    fl = await is_admin(user_id, username)
    if fl and fl_1:
        await message.answer(f'Введите наименование проекта:')
        await state.set_state(CreateProject.GET_PROJECT)
    else:
        await message.answer(f'{message.from_user.first_name}, этот раздел не для Вас :(')

async def get_create_project_descr(message:Message, state:FSMContext):
    await state.update_data(project=message.text)
    await message.answer(f'Опишите проект:')
    await state.set_state(CreateProject.GET_DESCR)

async def get_create_project_people(message:Message, state:FSMContext):
    await state.update_data(descr=message.text)
    await message.answer(f'Введите ФИО людей, занимающихся проектом через разделитель "|". Например, Человек|Человек.')
    await state.set_state(CreateProject.GET_PEOPLE)

async def create_project(message:Message, state:FSMContext):
    data = await state.get_data()
    project = data.get('project')
    descr = data.get('descr')
    people = message.text
    fl = await create_project_db(project, descr, people)
    if fl:
        await message.answer(f'Проект успешно добавлен!')
    else:
        await message.answer(f'Произошла ошибка :(')
    await state.clear()