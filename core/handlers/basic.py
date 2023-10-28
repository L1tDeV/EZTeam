from aiogram import Bot
from aiogram.types import Message
from core.keyboards.inline import get_inline_keyboard
from core.keyboards.reply import get_reply_keyboard
import json

async def get_start(message:Message, bot:Bot):
    # await bot.send_message(message.from_user.id, f'Hi, {message.from_user.first_name}! Welcome to SmaF1 bot')
    # await message.answer(f'Hi, {message.from_user.first_name}! Welcome to SmaF1 bot')
    # await message.reply(f'Hi, {message.from_user.first_name}! Welcome to SmaF1 bot')
    # await message.answer(f'<b>Bold text</b>')
    # await message.answer(f'<s>Зачеркнутый текст</s>')
    # await message.answer(f'<tg-spoiler>Spoiler</tg-spoiler>')
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в бота EZTeam!👋 \n'
                         f'Давай в кратце расскажу, кто я и для чего создан!🤔')
    await message.answer(f'Как ты уже мог понять, я - бот, так что со мной, к сожалению, особо не поболтаешь😕 (хотя я был бы не прочь поговорить 😉), но я могу помочь тебе с твоими вопросами.🙃 \n'
                         f'\n'
                         f'С чем я могу помочь:\n'
                         f'✅ Решение частозадаваемых бытовых вопросов (вопросы, по типу: "Как и куда отдавать заявление на отпуск?")\n'
                         f'✅ Быстро найти необходимую тебе информацию. \n'
                         f'✅ Рассказать тебе о проектах компании, кто над ними работает, а также дать информацию о сотрудниках компании.',
                        reply_markup={get_inline_keyboard(), get_reply_keyboard()})
    
async def unknown_command(message:Message, bot:Bot):
    await message.answer(f'Извини, но я не знаю такой команды😕')

async def get_info(message:Message, bot:Bot):
    await message.answer(f'{message.from_user.first_name}, ты наверное забыл, что я могу 🤔, давай напомню. \n')
    await message.answer(f'Как ты уже мог понять, я - бот, так что со мной, к сожалению, особо не поболтаешь😕 (хотя я был бы не прочь поговорить 😉), но я могу помочь тебе с твоими вопросами.🙃 \n'
                         f'\n'
                         f'С чем я могу помочь:\n'
                         f'✅ Решение частозадаваемых бытовых вопросов (вопросы, по типу: "Как и куда отдавать заявление на отпуск?")\n'
                         f'✅ Быстро найти необходимую тебе информацию. \n'
                         f'✅ Рассказать тебе о проектах компании, кто над ними работает, а также дать информацию о сотрудниках компании.',
                        reply_markup=get_inline_keyboard())

async def get_img(message: Message, bot:Bot):
    await message.answer(f'Ну ок, сохраню.')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.png')

async def get_hello(message:Message, bot:Bot):
    await message.answer(f'Ну здоров!')
    json_str = json.dumps(message.dict(), default=str)
    print(json_str)