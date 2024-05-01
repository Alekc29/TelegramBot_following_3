import random

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext

from core.utils.data_base import DataBase

router = Router()

EMOJIS = ['😁','🤭','🤣','😱','🎁','😻','🤗','🤢','☺']
REF_ID = ''
USER_ID = ''
USER_NAME = ''


def created_kbr(emj):
    button_list = []
    random.shuffle(emj)
    col = 0
    row = 0
    button_list.append([])
    for item in emj:
        col += 1
        button_list[row].append(InlineKeyboardButton(text=item, callback_data=item))
        if col == 3:
            col = 0
            row += 1
            button_list.append([])
    keyboard = InlineKeyboardMarkup(inline_keyboard=button_list)
    return keyboard


@router.message(Command(commands=['start', 'run']))
async def get_start(message: Message, bot: Bot, state: FSMContext):
    global REF_ID, USER_ID, USER_NAME
    start_command = message.text
    REF_ID = str(start_command[7:])
    USER_ID = message.from_user.id
    USER_NAME = message.from_user.first_name
    await message.answer(f'Выбери: "{random.choice(EMOJIS)}"', reply_markup=created_kbr(EMOJIS))


@router.callback_query(F.data.in_(EMOJIS))
async def checked_correct(cq: CallbackQuery, bot: Bot):
    global REF_ID, USER_ID, USER_NAME
    capch_color = cq.message.text.split('"')[1] 
    if(cq.data == capch_color):
        await cq.message.answer('Верно! Capcha пройдена.\n'
                                'Для продолжения работы перейдите в свой профиль.')
        if REF_ID != USER_ID:
            db = DataBase('users.db')
            if not db.user_exists(USER_ID):
                db.add_user(USER_ID,
                            USER_NAME,
                            REF_ID)
                lot = DataBase('lot.db')
                lot.add_user(USER_ID,
                             USER_NAME,
                             REF_ID)
                if not lot.user_exists(REF_ID):
                    lot.add_user(REF_ID)
            else:
                await bot.send_message(USER_ID, 'Вы уже были зарегистрированы.')
    else:
        await cq.message.answer(f'Другой символ! "{random.choice(EMOJIS)}"',
                                reply_markup=created_kbr(EMOJIS))
    await cq.answer()


@router.message(F.text == 'Привет')
async def get_hello(message: Message):
    await message.answer('И тебе привет!')


@router.message()
async def get_echo(message: Message):
    await message.answer(
        'Такой команды я не знаю! В меню есть все доступные команды.'
    )

