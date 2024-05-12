from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='info',
            description='Информация о боте'
        ),
        BotCommand(
            command='form',
            description='Создать/редактировать свой профиль в боте'
        ),
        BotCommand(
            command='profile',
            description='Посмотреть свой профиль'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())