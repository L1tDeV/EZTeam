from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.statespeople import FindPeopleSteps
from core.utils.callbackdata import QueryInfo
from aiogram.types import InputFile 
from sqlite_aio.sqlite import get_users_lst, get_check_lst

# db_people = [['Котов','Аркадий', 'Дмитриевич', '16.05.1980','+7-960-643-28-96','Паркоматика'],[['Лютый','Никита', 'Артемович', '03.10.2006','+7-960-535-56-69','Паркоматика']]]

db_people = get_users_lst()

def find_people(question, db_people):
    que_lst = list(question.split())
    lst_ind = []
    lst_sovp = []
    for inf in que_lst:
        for people in db_people:
            ind = db_people.index(people)
            for el in people:
                if inf.lower() in el.lower() and ind not in lst_ind:
                    lst_ind.append(ind)
                    lst_sovp.append(1)
                elif inf.lower() in el.lower() and ind in lst_ind:
                    lst_sovp[lst_ind.index(ind)] +=1
    lst_answ = []
    for ind in lst_ind:
        if lst_sovp[lst_ind.index(ind)] == max(lst_sovp):
                lst_answ.append(db_people[ind])

    return lst_answ



async def get_people_data(message:Message, state:FSMContext):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl = await get_check_lst(user_id, username)
    if fl:
        await message.answer(f'Введите имя, фамилию и отчество человека через пробел (можно что-то одно):')
        await state.set_state(FindPeopleSteps.GET_PEOPLE)
    else:
        await message.answer(f'{message.from_user.first_name}, этот бот не для вас :(')

async def get_people_info(message:Message, state:FSMContext):
    txt=message.text
    db_people = get_users_lst()
    lst_answ = find_people(txt, db_people)
    if len(lst_answ)>0:
        answ = f''
        for people in lst_answ:
            person = f'✔️'
            birthday = f'🗓️Дата рождения: '
            phone = f'📱Номер телефона: '
            projects = f'💻Проекты: '
            for inf in people:
                if people.index(inf)==0:
                    person +=inf + '\n'
                elif people.index(inf)==1:
                    birthday += inf+ '\n'
                elif people.index(inf)==2:
                    phone += inf+ '\n'
                elif people.index(inf)==3:
                    projects+= inf+ '\n'
            answ += person+birthday+phone+projects+'\n'
        await message.answer(f'По Вашему запросу были найдены следующие члены компании😉:\n\n {answ}')
    else:
        await message.answer(f'По Вашему запросу никого не удалось найти😕')
    await state.clear()