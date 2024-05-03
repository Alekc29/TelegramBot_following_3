from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == 'Привет')
async def get_hello(message: Message):
    await message.answer('И тебе привет!')


@router.message()
async def get_echo(message: Message):
    await message.answer(
        'Такой команды я не знаю! В меню есть все доступные команды.'
    )
