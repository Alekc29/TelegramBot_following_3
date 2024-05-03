import random

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           Message,
                           ReplyKeyboardRemove)

from config import (CHANNEL_ID, BOT_NAME,
                    CHANNEL_LINK, BASE_USERS,
                    BASE_LOT)
from core.keyboards.replykey import client_en_profile, client_profile
from core.utils.data_base import DataBase

router = Router()

EMOJIS = ['😁', '🤭', '🤣', '😱', '🎁', '😻', '🤗', '🤢', '☺']
REF_ID = ''
USER_ID = ''
USER_NAME = ''
LANG = 'RU'


def created_kbr(emj):
    button_list = []
    random.shuffle(emj)
    col = 0
    row = 0
    button_list.append([])
    for item in emj:
        col += 1
        button_list[row].append(InlineKeyboardButton(text=item,
                                                     callback_data=item))
        if col == 3:
            col = 0
            row += 1
            button_list.append([])
    return InlineKeyboardMarkup(inline_keyboard=button_list)


@router.message(Command(commands=['start', 'run']))
async def get_start(message: Message, bot: Bot, state: FSMContext):
    global REF_ID, USER_ID, USER_NAME
    start_command = message.text
    REF_ID = str(start_command[7:])
    USER_ID = message.from_user.id
    USER_NAME = message.from_user.first_name
    await message.answer(f'Выбери: "{random.choice(EMOJIS)}"',
                         reply_markup=created_kbr(EMOJIS))


@router.callback_query(F.data.in_(EMOJIS))
async def checked_correct(cq: CallbackQuery, bot: Bot):
    global REF_ID, USER_ID, USER_NAME
    capch_color = cq.message.text.split('"')[1]
    if (cq.data == capch_color):
        await cq.message.answer(
            'Верно! Capcha пройдена.\n'
            'Для продолжения работы перейдите в свой профиль.'
        )
        if REF_ID != USER_ID:
            db = DataBase(BASE_USERS)
            if not db.user_exists(USER_ID):
                db.add_user(USER_ID,
                            USER_NAME,
                            REF_ID)
                lot = DataBase(BASE_LOT)
                lot.add_user(USER_ID,
                             USER_NAME,
                             REF_ID)
                if not lot.user_exists(REF_ID):
                    lot.add_user(REF_ID)
            else:
                await bot.send_message(USER_ID,
                                       'Вы уже были зарегистрированы.')
    else:
        await cq.message.answer(f'Другой символ! "{random.choice(EMOJIS)}"',
                                reply_markup=created_kbr(EMOJIS))
    await cq.answer()


@router.message(Command(commands=['language']))
async def get_lang(message: Message, bot: Bot):
    global LANG
    if LANG == 'RU':
        LANG = 'EN'
        await message.answer('Success', reply_markup=client_en_profile)
    else:
        LANG = 'RU'
        await message.answer('Русский', reply_markup=client_profile)
    await message.delete()


@router.message(Command(commands=['help']))
async def get_help(message: Message, bot: Bot):
    global LANG
    if LANG == 'RU':
        await message.answer(
            'Если возникает ошибка при работе с базой бота, наберите /start. '
            'Если ошибка сохраниться, сообщите администратору.'
        )
    else:
        await message.answer(
            'If an error occurs when working '
            'with the bot database, type /start. '
            'If the error persists, inform the administrator.'
        )
    await message.delete()


def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    return False


@router.message(Command(commands=['profile']))
async def get_profile(message: Message, bot: Bot):
    ''' Выдаёт информацию из базы пользователю. '''
    global LANG
    if check_sub_channel(
        await bot.get_chat_member(chat_id=CHANNEL_ID,
                                  user_id=message.from_user.id)
    ):
        db = DataBase(BASE_LOT)
        try:
            all_users = db.count_all_users()
            referals_user = db.get_referals(message.from_user.id)
            count_referals = db.count_referals(message.from_user.id)
            count_follow = 0
            rang = 0
            print(len(referals_user))
            if len(referals_user) > 0:
                for user in referals_user:
                    try:
                        if check_sub_channel(
                            await bot.get_chat_member(
                                chat_id=CHANNEL_ID,
                                user_id=user[0]
                            )
                        ):
                            count_follow += 1
                    except Exception:
                        db.del_user(user[0])
                        if LANG == 'RU':
                            await message.answer(
                                f'Пользователь {user[1]} удален из телеграмма.'
                            )
                        else:
                            await message.answer(
                                f'The user {user[1]} has been '
                                'deleted from telegram.'
                            )
                db.add_rang(message.from_user.id, count_follow)
                rang = count_follow
                rang += int(db.get_rang_ref(message.from_user.id) // 2)
                db.add_rang(message.from_user.id,
                            rang)
            if LANG == 'RU':
                await message.answer(
                    f'Профиль: {message.from_user.first_name}\n'
                    f'Количество приглашенных друзей: {count_referals}\n'
                    f'Количество подписанных на канал друзей: {count_follow}\n'
                    f'Ваш ранг: {rang}\n'
                    f'Всего пользователей: {all_users}',
                    reply_markup=client_profile
                )
            else:
                await message.answer(
                    f'Profile: {message.from_user.first_name}\n'
                    f'Number of invited friends: {count_referals}\n'
                    f'Number of friends subscribed to the channel: '
                    f'{count_follow}\n'
                    f'Your rank: {rang}\n'
                    f'Total users: {all_users}',
                    reply_markup=client_en_profile
                )
            await message.delete()
        except Exception as ex:
            print(ex)
            if LANG == 'RU':
                await message.answer(
                    'Произошла ошибка при обращении к базе.'
                )
            else:
                await message.answer(
                    'An error occurred while accessing the database.'
                )
    else:
        if LANG == 'RU':
            await message.answer(f'Подпишитесь на канал. {CHANNEL_LINK}',
                                 reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f'Subscribe to the channel. {CHANNEL_LINK}',
                                 reply_markup=ReplyKeyboardRemove())


@router.message(F.text.in_(['Таблица лидеров', 'Topboard']))
async def get_stats(message: Message, bot: Bot):
    ''' Выдаёт 10 лидеров из базы по числу рефералов. '''
    global LANG
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID,
                         user_id=message.from_user.id)):
        db = DataBase(BASE_LOT)
        try:
            top_table = db.get_top_rang_users()
            list_top_table = ''
            inc = 0
            for top_user in top_table:
                inc += 1
                list_top_table += (f'\n{inc:<4} '
                                   f'id: {top_user[0]:<14} '
                                   f'ранг: {top_user[1]}')
            place_in_top = db.get_pos_rang_user(message.from_user.id)
            if LANG == 'RU':
                await message.answer(f'Таблица лидеров: ```{list_top_table}```'
                                     f'\nВаше место: {place_in_top}',
                                     reply_markup=client_profile,
                                     parse_mode='MarkdownV2')
            else:
                await message.answer(
                    f'Topboard: ```{list_top_table}```'
                    f'\nYour place: {place_in_top}',
                    reply_markup=client_profile,
                    parse_mode='MarkdownV2'
                )
            await message.delete()
        except Exception as ex:
            print(ex)
            if LANG == 'RU':
                await message.answer('Произошла ошибка при обращении к базе.')
            else:
                await message.answer(
                    'An error occurred while accessing the database.'
                )
    else:
        if LANG == 'RU':
            await message.answer(f'Подпишитесь на канал. {CHANNEL_LINK}',
                                 reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f'Subscribe to the channel. {CHANNEL_LINK}',
                                 reply_markup=ReplyKeyboardRemove())


@router.message(F.text.in_(['Пригласить друзей', 'Invite friends']))
async def get_friends_link(message: Message, bot: Bot):
    ''' Выдаёт ссылку для привлечения рефералов. '''
    global LANG
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID,
                         user_id=message.from_user.id)):
        if LANG == 'RU':
            await message.answer(
                f'Ваша реферальная ссылка: \n'
                f'https://t.me/{BOT_NAME}?start={message.from_user.id}'
            )
        else:
            await message.answer(
                f'Your referral link: \n'
                f'https://t.me/{BOT_NAME}?start={message.from_user.id}'
            )
        await message.delete()
    else:
        if LANG == 'RU':
            await message.answer(f'Подпишитесь на канал. {CHANNEL_LINK}',
                                 reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f'Subscribe to the channel. {CHANNEL_LINK}',
                                 reply_markup=ReplyKeyboardRemove())
