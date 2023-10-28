from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from core.handlers.basic import get_start, get_hello, unknown_command, get_info
from core.filters.iscontact import IsTrueContact
import asyncio
import logging
from core.settings import settings
from aiogram.filters import Command, CommandStart
from core.utils.commands import set_commands
from core.handlers.callback import get_query
from core.utils.callbackdata import QueryInfo
from core.handlers import form
from core.handlers import question_form, project_form
from core.utils.statesquestion import QuestionSteps
from core.utils.statesproject import ProjectSteps
from core.utils.statesform import StepsForm

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text="Бот запущен!")

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот остановлен!")


async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # dp.message.register(get_img, F.photo)
    # dp.callback_query.register(select_macbook, F.data.startswith('mac_'))
    dp.callback_query.register(question_form.get_question_form, QueryInfo.filter(F.query=='question'))
    dp.message.register(question_form.get_question_form, F.text=='Задать вопрос')
    dp.message.register(question_form.get_question, QuestionSteps.GET_QUESTION)

    dp.message.register(project_form.get_project_form, F.text=="Проекты")
    dp.message.register(project_form.get_project, ProjectSteps.GET_PROJECT)

    dp.message.register(form.get_form, Command(commands='form')) 
    dp.message.register(form.get_name, StepsForm.GET_NAME)
    dp.message.register(form.get_last_name, StepsForm.GET_LAST_NAME)
    dp.message.register(form.get_age, StepsForm.GET_AGE)

    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(get_info, Command(commands='info'))

    dp.message.register(unknown_command, F.text)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())