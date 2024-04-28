import re
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.keyboards.replykey import client_profile
from core.utils.data_base import DataBase
from config import DEV_ID, CHANNEL_ID, BOT_NAME, CHANNEL_LINK

router = Router()


def check_sub_channel(chat_member):
    print(chat_member.status)
    if chat_member.status != 'ChatMemberStatus.LEFT':
        return True
    else:
        return False


@router.message(Command('profile'))
async def get_profile(message: Message, bot: Bot):
    ''' Выдаёт информацию из базы пользователю. '''
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID,
                                                   user_id=message.from_user.id)):
        db = DataBase('users.db')
        try:
            all_users = db.count_all_users()
            referals_user = db.get_referals(message.from_user.id)
            count_referals = db.count_referals(message.from_user.id)
            count_follow = 0
            for user in referals_user:
                if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user[0])):
                    count_follow += 1
            await message.answer(f'Профиль: {message.from_user.first_name}\n'
                                 f'Количество подписанных на канал рефералов: {count_follow}\n'
                                 f'Количество рефералов: {count_referals}\n'
                                 f'Всего пользователей: {all_users}',
                                 reply_markup=client_profile)
            await message.delete()
        except Exception as ex:
            print(ex)
            await message.answer('Произошла ошибка при обращении к базе.')
    else:
        await bot.send_message(message.from_user.id,
                               f'Подпишитесь на канал. {CHANNEL_LINK}',
                               reply_markup=ReplyKeyboardRemove)


@router.message(F.text == 'Таблица лидеров')
async def get_stats(message: Message, bot: Bot):
    ''' Выдаёт 10 лидеров из базы по числу рефералов. '''
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID,
                         user_id=message.from_user.id)):
        db = DataBase('users.db')
        try:
            top_table = db.get_top_users()
            list_top_table = ''
            inc = 0
            for top_user in top_table:
                if inc > 0:
                    list_top_table += f'\n{inc}) id: {top_user[0]} друзей: {top_user[1]}'
                inc += 1
            await message.answer(f'Таблица лидеров: {list_top_table}',
                                 reply_markup=client_profile)
            await message.delete()
        except Exception as ex:
            print(ex)
            await message.answer('Произошла ошибка при обращении к базе.')
    else:
        await bot.send_message(message.from_user.id,
                               f'Подпишитесь на канал. {CHANNEL_LINK}',
                               reply_markup=ReplyKeyboardRemove)


@router.message(F.text == 'Пригласить друзей')
async def get_stats(message: Message, bot: Bot):
    ''' Выдаёт ссылку для привлечения рефералов. '''
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID,
                         user_id=message.from_user.id)):
        await message.answer(f'Ваша реферальная ссылка: \n'
                             f'https://t.me/{BOT_NAME}?start={message.from_user.id}')
        await message.delete()
    else:
        await bot.send_message(message.from_user.id,
                               f'Подпишитесь на канал. {CHANNEL_LINK}',
                               reply_markup=ReplyKeyboardRemove)
