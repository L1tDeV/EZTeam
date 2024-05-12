from aiogram.filters.callback_data import CallbackData

class QueryInfo(CallbackData, prefix='qe'):
    query: str