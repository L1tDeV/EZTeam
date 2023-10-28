from aiogram import Bot
from aiogram.types import CallbackQuery
from core.utils.callbackdata import QueryInfo

# async def select_macbook(call:CallbackQuery, bot:Bot):
#     model = call.data.split('_')[1]
#     answer = f'{call.message.from_user.first_name}, ты выбрал Apple MacBook {model}'
#     await call.message.answer(answer)
#     await call.answer()

async def get_query(call:CallbackQuery, bot:Bot,callback_data: QueryInfo):
    query = callback_data.query
    answer = f'{call.message.from_user.first_name}, ты выбрал {query}'
    await call.message.answer(answer)
    await call.answer()