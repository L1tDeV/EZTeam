from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from core.handlers.basic import get_start, admin_sign, unknown_command, get_info, get_profile, out_admin
from core.filters.iscontact import IsTrueContact
import asyncio
import logging
from core.settings import settings
from aiogram.filters import Command, CommandStart
from core.utils.commands import set_commands
from core.handlers.callback import get_query
from core.utils.callbackdata import QueryInfo
from core.handlers import form
from core.handlers import question_form, project_form, find_form
from core.utils.statesquestion import QuestionSteps, QueAnswAdd
from core.utils.statesproject import ProjectSteps, CreateProject
from core.utils.statespeople import FindPeopleSteps
from core.utils.statesform import StepsForm
from sqlite_aio.sqlite import db_start
from core.handlers import edit_lists
from core.utils.statescheck_admin import CheckStates, AdminStates

# async def on_startup(_):
#     await db_start()

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text="Бот запущен!")

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот остановлен!")


async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    await db_start()
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(admin_sign, F.text == "/admin")

    # dp.message.register(get_img, F.photo)
    # dp.callback_query.register(select_macbook, F.data.startswith('mac_'))
    dp.callback_query.register(question_form.get_question_form, QueryInfo.filter(F.query=='question'))
    dp.message.register(question_form.get_question_form, F.text=='🤔 Задать вопрос')
    dp.message.register(question_form.get_question_form, F.text=='Задать вопрос')
    dp.message.register(question_form.get_question, QuestionSteps.GET_QUESTION)

    dp.callback_query.register(find_form.get_people_data, QueryInfo.filter(F.query=='find_pers'))
    dp.message.register(find_form.get_people_data, F.text=='🔍 Поиск человека')
    dp.message.register(find_form.get_people_data, F.text=='Поиск человека')
    dp.message.register(find_form.get_people_info, FindPeopleSteps.GET_PEOPLE)

    dp.callback_query.register(project_form.get_project_form, QueryInfo.filter(F.query=='projects'))
    dp.message.register(project_form.get_project_form, F.text=="💻 Проекты компании")
    dp.message.register(project_form.get_project_form, F.text=="Проекты компании")
    dp.message.register(project_form.get_project, ProjectSteps.GET_PROJECT)

    dp.message.register(question_form.create_question_form, F.text=="📝 Добавить ответ на вопрос")
    dp.message.register(question_form.get_answ_form, QueAnswAdd.GET_QUESTION)
    dp.message.register(question_form.create_que_ans, QueAnswAdd.GET_ANSWER)

    dp.message.register(project_form.get_create_project_form, F.text=="✍🏻 Добавить проект")
    dp.message.register(project_form.get_create_project_descr, CreateProject.GET_PROJECT)
    dp.message.register(project_form.get_create_project_people, CreateProject.GET_DESCR)
    dp.message.register(project_form.create_project, CreateProject.GET_PEOPLE)

    dp.message.register(edit_lists.get_check_edit_form, F.text=="➕ Редактировать доступ к боту")
    dp.message.register(edit_lists.get_check_id, CheckStates.GET_DEL_OR_ADD)
    dp.message.register(edit_lists.checks_edit, CheckStates.GET_CHECKS_ID)

    dp.message.register(edit_lists.get_admin_edit_form, F.text=="⭐ Редактировать список администраторов")
    dp.message.register(edit_lists.get_admin_id, AdminStates.GET_DEL_OR_ADD)
    dp.message.register(edit_lists.admins_edit, AdminStates.GET_ADMINS_ID)


    dp.message.register(form.get_form, Command(commands='form')) 
    dp.message.register(form.get_name, StepsForm.GET_NAME)
    dp.message.register(form.get_birthday, StepsForm.GET_BIRTHDAY)
    dp.message.register(form.get_phone, StepsForm.GET_PHONE)
    dp.message.register(form.get_age, StepsForm.GET_PROJECTS)

    dp.message.register(get_profile, Command(commands='profile'))

    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(get_info, Command(commands='info'))

    dp.message.register(out_admin, F.text=="❌ Выйти")

    dp.message.register(unknown_command, F.text)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())