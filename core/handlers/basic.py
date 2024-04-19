from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from core.utils.data_base import DataBase

router = Router()


@router.message(Command(commands=['start', 'run']))
async def get_start(message: Message, bot: Bot):
    db = DataBase('users.db')
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.first_name)
    await message.answer(
        'Привет! Я робот.'
    )


@router.message(F.text == 'Привет')
async def get_hello(message: Message):
    await message.answer('И тебе привет!')


@router.message()
async def get_echo(message: Message):
    await message.answer(
        'Такой команды я не знаю! В меню есть все доступные команды.'
    )

