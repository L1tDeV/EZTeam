from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import QueryInfo

def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Задать вопрос', callback_data=QueryInfo(query='question'))
    keyboard_builder.button(text='Поиск человека', callback_data=QueryInfo(query='find_pers'))
    keyboard_builder.button(text='Проекты компании', callback_data=QueryInfo(query='projects'))
    
    # keyboard_builder.button(text='Profile Dev', url='https://t.me/SmaF1_1')

    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()
