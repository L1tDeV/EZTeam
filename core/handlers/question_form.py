from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.statesquestion import QuestionSteps
from core.utils.callbackdata import QueryInfo
from aiogram.types import InputFile 

db_questions = ['Когда выдается (дадут, выдают) Заработная плата (зп, ЗП, ЗарПлата)', 'Как оформить (оформлять, оформение) командировку (командировочный, командировка, командировки)']
db_answers=['Заработная плата начисляется на карту 15 и 30 числа каждого месяца.', '✔️Пишешь заявление\n✔️Получаешь "Суточные" в бухгалтерии\n✔️Во время командировки сохраняешь все чеки\n✔️По возвращению пишешь отчет по шаблону: https://shablon']

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
        return db_answers[db_questions.index(pred_ques[pred_ques_kol.index(max_kol)])]

async def get_question_form(message:Message, state:FSMContext):
    await message.answer(f'Введите свой вопрос:')
    await state.set_state(QuestionSteps.GET_QUESTION)

async def get_question(message:Message, state:FSMContext):
    txt=''
    if '?' in message.text:
        txt = message.text[:len(message.text)-1]
    else:
        txt=message.text
    answer = find_answer(list(txt.split()), db_questions,db_answers)
    await message.answer(answer)
    await state.clear()