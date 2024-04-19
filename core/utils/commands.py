from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands_main(bot: Bot):
    commands = [
        BotCommand(
            command='profile',
            description='Ваш профиль'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='language',
            description='Сменить язык'
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
