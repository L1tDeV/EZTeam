from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.statesquestion import QuestionSteps, QueAnswAdd
from core.utils.callbackdata import QueryInfo
from aiogram.types import InputFile 
from sqlite_aio.sqlite import get_questions_lst, get_check_lst, is_admin, create_question

def find_answer(question, db_questions,db_answers):
    pred_ques = []
    pred_ques_kol = []
    for word in question:
        if pred_ques == []:
            for ques in db_questions:
                if word.lower() in ques.lower():
                    pred_ques.append(ques)
                    pred_ques_kol.append(0)
        else:
            for ques in pred_ques:
                if word.lower() in ques.lower():
                    pred_ques_kol[pred_ques.index(ques)]+=1
    if len(pred_ques_kol)!=0:
        max_kol = max(pred_ques_kol)
    else:
        max_kol=0
    if pred_ques_kol.count(max_kol)>1:
        return f'Не удалось дать четкий ответ, пожалуйста, переформулируйте вопрос и задайте его заново.'
    elif max_kol==0 and (len(pred_ques)>1 or len(pred_ques)==0):
        return f'Извините, у меня нет ответа на данный вопрос.'
    else:
        return f'{db_answers[db_questions.index(pred_ques[pred_ques_kol.index(max_kol)])]}'

async def get_question_form(message:Message, state:FSMContext):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl = await get_check_lst(user_id, username)
    if fl:
        await message.answer(f'Введите свой вопрос:')
        await state.set_state(QuestionSteps.GET_QUESTION)
    else:
        await message.answer(f'{message.from_user.first_name}, этот бот не для вас :(')

async def get_question(message:Message, state:FSMContext):
    db_questions, db_answers = get_questions_lst()
    txt=''
    if '?' in message.text:
        txt = message.text[:len(message.text)-1]
    else:
        txt=message.text
    answer = find_answer(list(txt.split()), db_questions,db_answers)
    await message.answer(answer)
    await state.clear()

async def create_question_form(message:Message, state:FSMContext):
    username = str(message.from_user.username)
    user_id = str(message.from_user.id)
    fl_1 = await get_check_lst(user_id, username)
    fl_2 = await is_admin(user_id, username)
    if fl_1 and fl_2:
        await message.answer(f'Введите вопрос:')
        await state.set_state(QueAnswAdd.GET_QUESTION)
    else:
        await message.answer(f'Этот раздел не для Вас.')

async def get_answ_form(message:Message, state:FSMContext):
    await state.update_data(question = message.text)
    await message.answer(f'Введите ответ:')
    await state.set_state(QueAnswAdd.GET_ANSWER)

async def create_que_ans(message:Message, state:FSMContext):
    answer = message.text
    data = await state.get_data()
    question = data.get('question')
    fl = await create_question(question, answer)
    if fl:
        await message.answer(f'Вопрос успешно добавлен!')
    else:
        await message.answer(f'Произошла ошибка :(')
    await state.clear()
