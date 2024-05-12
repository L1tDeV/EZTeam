from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm
from core.handlers.find_form import db_people
from sqlite_aio.sqlite import create_user, edit_user
from sqlite_aio.sqlite import get_check_lst

async def get_form(message:Message, state:FSMContext):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl = await get_check_lst(user_id, username)
    if fl:
        await message.answer(f'{message.from_user.first_name}, начинаем заполнять, Введи свои ФИО через пробел.')
        await state.set_state(StepsForm.GET_NAME)
    else:
        await message.answer(f'{message.from_user.first_name}, этот бот не для вас :(')

async def get_name(message:Message, state:FSMContext):
    await message.answer(f'Твое ФИО через пробел \r\n{message.text}\r\nТеперь введи дату рождения (в формате: 05.10.1998).')
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_BIRTHDAY)

async def get_birthday(message:Message, state:FSMContext):
    await message.answer(f'Твоя дата рождения: \r\n{message.text}\r\nВведи свой номер телефона (формат: +7-960-645-32-45).')
    await state.update_data(birthday=message.text)
    await state.set_state(StepsForm.GET_PHONE)

async def get_phone(message:Message, state:FSMContext):
    await message.answer(f'Твой телефон: \r\n{message.text}\r\nВведи через запятую проекты, которыми занимаешься.')
    await state.update_data(phone=message.text)
    await state.set_state(StepsForm.GET_PROJECTS)

async def get_age(message:Message, state:FSMContext):
    context_data = await state.get_data()
    name=context_data.get('name')
    phone=context_data.get('phone')
    birthday=context_data.get('birthday')
    projects = message.text
    data_user=f'Данные:\r\n\n'\
    f'ФИО: {name}\r\n'\
    f'Дата рождения: {birthday}\r\n'\
    f'Номер телефона: {phone}\r\n'\
    f'Проекты: {projects}\r\n'
    send_lst = []
    # for i in list(name.split()):
    #     send_lst.append(i)
    send_lst.append(name)
    send_lst.append(birthday)
    send_lst.append(phone)
    send_lst.append(projects)
    id_user = str(message.from_user.id)
    fl = await create_user(id_user, send_lst)
    # db_people.append(send_lst)
    # print(db_people)
    if fl:
        await message.answer(data_user)
        await message.answer(f'Данные сохранены.😉 Поздравляем с регистрацией.')
    else:
        fl = await edit_user(id_user, send_lst)
        if fl:
            await message.answer(data_user)
            await message.answer(f'Ваши данные отредактированы.😉')
        else:
            await message.answer(f'Произошла ошибка с заполнением данных :(')
    await state.clear()