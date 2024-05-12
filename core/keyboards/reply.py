from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='🤔 Задать вопрос')
    keyboard_builder.button(text='🔍 Поиск человека')
    keyboard_builder.button(text='💻 Проекты компании')

    # keyboard_builder.button(text='Геолокация', request_location=True)
    # keyboard_builder.button(text='Контакт', request_contact=True)

    # keyboard_builder.button(text='Викторина', request_poll=KeyboardButtonPollType())
    keyboard_builder.adjust(3) #сколько кнопок будет в каждом ряду
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=False, 
                               input_field_placeholder='Выбери информацию для отправки боту или создай викторину')
    
def get_reply_admin_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='📝 Добавить ответ на вопрос')
    keyboard_builder.button(text='✍🏻 Добавить проект')
    keyboard_builder.button(text='➕ Редактировать доступ к боту')
    keyboard_builder.button(text='⭐ Редактировать список администраторов')
    keyboard_builder.button(text='❌ Выйти')

    # keyboard_builder.button(text='Геолокация', request_location=True)
    # keyboard_builder.button(text='Контакт', request_contact=True)

    # keyboard_builder.button(text='Викторина', request_poll=KeyboardButtonPollType())
    keyboard_builder.adjust(2) #сколько кнопок будет в каждом ряду
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=False, 
                               input_field_placeholder='Выбери информацию для отправки боту или создай викторину')
   