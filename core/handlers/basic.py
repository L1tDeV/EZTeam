from aiogram import Bot
from aiogram.types import Message
from core.keyboards.inline import get_inline_keyboard
from core.keyboards.reply import get_reply_keyboard, get_reply_admin_keyboard
from sqlite_aio.sqlite import get_check_lst, get_user_prof, is_admin
import json

async def get_start(message:Message, bot:Bot):
    # await bot.send_message(message.from_user.id, f'Hi, {message.from_user.first_name}! Welcome to SmaF1 bot')
    # await message.answer(f'Hi, {message.from_user.first_name}! Welcome to SmaF1 bot')
    # await message.reply(f'Hi, {message.from_user.first_name}! Welcome to SmaF1 bot')
    # await message.answer(f'<b>Bold text</b>')
    # await message.answer(f'<s>Зачеркнутый текст</s>')
    # await message.answer(f'<tg-spoiler>Spoiler</tg-spoiler>')
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl = await get_check_lst(user_id, username)
    print(fl)
    if fl:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать в бота EZTeam!👋 Давай в кратце расскажу, кто я и для чего создан!🤔\n\nКак ты уже мог понять, я - бот, так что со мной, к сожалению, особо не поболтаешь😕 (хотя я был бы не прочь поговорить 😉), но я могу помочь тебе с твоими вопросами.🙃\n\nС чем я могу помочь:\n\n✅ Решение частозадаваемых бытовых вопросов (вопросы, по типу: "Когда выдают зарплату?")\n✅ Быстро найти необходимую тебе информацию. \n✅ Рассказать тебе о проектах компании, кто над ними работает, а также дать информацию о сотрудниках компании.',
                        reply_markup=get_reply_keyboard())
        #, reply_markup=get_inline_keyboard()
    else:
        await message.answer(f'{message.from_user.first_name}, этот бот не для вас :(')
    json_str = json.dumps(message.dict(), default=str)
    print(json_str)
    
async def unknown_command(message:Message, bot:Bot):
    await message.answer(f'Извини, но я не знаю такой команды😕')

async def get_profile(message:Message, bot:Bot):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl = await get_check_lst(user_id, username)
    if fl:
        user = await get_user_prof(user_id)
        data_user=f'Данные:\r\n\n'\
        f'ФИО: {user[1]}\r\n'\
        f'Дата рождения: {user[2]}\r\n'\
        f'Номер телефона: {user[4]}\r\n'\
        f'Проекты: {user[5]}\r\n'
        await message.answer(data_user)
    else:
        await message.answer(f'{message.from_user.first_name}, этот бот не для вас :(')


async def get_info(message:Message, bot:Bot):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl = await get_check_lst(user_id, username)
    if fl:
        await message.answer(f'{message.from_user.first_name}, ты наверное забыл, что я могу 🤔, давай напомню. \n\n \nДавай в кратце расскажу, кто я и для чего создан!🤔\n\nКак ты уже мог понять, я - бот, так что со мной, к сожалению, особо не поболтаешь😕 (хотя я был бы не прочь поговорить 😉), но я могу помочь тебе с твоими вопросами.🙃\n\nС чем я могу помочь:\n\n✅ Решение частозадаваемых бытовых вопросов (вопросы, по типу: "Как и куда отдавать заявление на отпуск?")\n✅ Быстро найти необходимую тебе информацию. \n✅ Рассказать тебе о проектах компании, кто над ними работает, а также дать информацию о сотрудниках компании.',)
    else:
        await message.answer(f'{message.from_user.first_name}, этот бот не для вас :(')

async def get_img(message: Message, bot:Bot):
    await message.answer(f'Ну ок, сохраню.')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.png')

async def admin_sign(message:Message, bot:Bot):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl = await is_admin(user_id,username)
    if fl:
        await message.answer(f'Успешный вход. (^.^)', 
                             reply_markup=get_reply_admin_keyboard())
    else:
        await message.answer(f'Извините, но Вы не являетесь администратором.')
        json_str = json.dumps(message.dict(), default=str)
        print(json_str)

async def out_admin(message:Message, bot:Bot):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl = await get_check_lst(user_id, username)
    if fl:
        await message.answer(f'Вы вышли из режима администратора', reply_markup=get_reply_keyboard())
    else:
        await message.answer(f'{message.from_user.first_name}, этот бот не для вас :(')

