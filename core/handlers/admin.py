from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, ReplyKeyboardRemove

from config import ADMIN_ID, BASE_LOT, BASE_USERS, CHANNEL_ID, DEV_ID
from core.keyboards.replykey import admin
from core.utils.class_fsm import FSMPost, FSMPostTop
from core.utils.data_base import DataBase
from core.utils.export_database_csv import export_csv

router = Router()


@router.message(Command('moderator'))
async def get_admin_keyboards(message: Message):
    if message.from_user.id in [DEV_ID, ADMIN_ID]:
        await message.answer('Что босс надо?',
                             reply_markup=admin)
        await message.delete()
    else:
        await message.answer('Вы не являетесь администратором бота.')
        await message.delete()


@router.message(F.text == 'Рассылка')
async def mailing_post_bot(message: Message, state: FSMContext):
    ''' функция для получения сообщения для рассылки по всем пользователям. '''
    if message.from_user.id in [DEV_ID, ADMIN_ID]:
        await message.answer('Набери пост для рассылки по юзерам.')
        await message.delete()
        await state.set_state(FSMPost.post)


@router.message(F.text == 'отмена')
async def cancel_handler(message: Message,
                         state: FSMContext,
                         bot: Bot):
    ''' Выход из машины состояний. '''
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply('Ok')


async def send_message_to_users(users, message: Message, bot: Bot):
    ''' функция для рассылки сообщения по списку пользователей '''
    for user in users:
        try:
            await bot.send_message(user[0],
                                   f'{message.text}')
        except Exception:
            await bot.send_message(
                DEV_ID,
                f'Произошла ошибка при отправке сообщения юзеру: {user[0]}'
            )


@router.message(FSMPost.post)
async def send_mailing_bot(message: Message,
                           bot: Bot,
                           state: FSMContext):
    ''' функция ловит сообщение для рассылки по всем пользователям. '''
    if message.from_user.id in [DEV_ID, ADMIN_ID]:
        db = DataBase(BASE_USERS)
        users = db.get_users()
        await send_message_to_users(users, message, bot)
        await message.answer(
            f"Рассылка сообщения завершена. Отправлено сообщений: {len(users)}"
        )
        await state.clear()


@router.message(F.text == 'Статистика')
async def get_statistics(message: Message):
    if message.from_user.id in [DEV_ID, ADMIN_ID]:
        db = DataBase(BASE_USERS)
        db_lot = DataBase(BASE_LOT)
        export_csv()
        file = FSInputFile("users.csv")
        try:
            top_table = db_lot.get_top_rang_users()
            count_all = db.count_all_users()
            count_lot = db_lot.count_all_users()
            list_top_table = ''
            inc = 0
            for top_user in top_table:
                inc += 1
                list_top_table += (f'\n{inc:<4} '
                                   f'id: {top_user[0]:<14} '
                                   f'ранг: {top_user[1]}')
            await message.answer(
                f'Таблица лидеров: ```{list_top_table}```'
                f'\nКоличество юзеров в лотерее: {count_lot}'
                f'\nКоличество юзеров в общей базе: {count_all}',
                parse_mode='MarkdownV2'
            )
            await message.answer_document(file, caption='База лотереи')
            await message.delete()
        except Exception as ex:
            print(ex)
            await message.answer('Произошла ошибка при обращении к базе.')


@router.message(F.text == 'Клиент')
async def change_client_command(message: Message):
    if message.from_user.id in [DEV_ID, ADMIN_ID]:
        await message.answer('Вы перешли в клиентскую часть.',
                             reply_markup=ReplyKeyboardRemove())
        await message.delete()


@router.message(F.text == 'Рассылка по топам')
async def mailing_post_top_bot(message: Message, state: FSMContext):
    ''' функция для получения сообщения для рассылки по топам. '''
    if message.from_user.id in [DEV_ID, ADMIN_ID]:
        await message.answer('Набери пост для рассылки по топам.')
        await message.delete()
        await state.set_state(FSMPostTop.post_top)


@router.message(FSMPostTop.post_top)
async def send_top_mailing_bot(message: Message,
                               bot: Bot,
                               state: FSMContext):
    ''' функция ловит сообщение для рассылки по топам. '''
    if message.from_user.id in [DEV_ID, ADMIN_ID]:
        db = DataBase(BASE_LOT)
        users = db.get_top_rang_users()
        await send_message_to_users(users, message, bot)
        await message.answer(
            f"Рассылка сообщения завершена. Отправлено сообщений: {len(users)}"
        )
        await state.clear()


@router.message(F.text == 'Новая лотерея')
async def start_new_lot(message: Message):
    if message.from_user.id in [DEV_ID, ADMIN_ID]:
        try:
            db = DataBase(BASE_LOT)
            db.del_table()
            await message.answer(
                'База старой лотереи удалена. Новая база создана.'
            )
            await message.delete()
        except Exception:
            await message.answer('Произошла ошибка при удалении базы.')


@router.message(Command('del_bot'))
async def del_bot_base(message: Message, bot: Bot):
    if message.from_user.id in [DEV_ID, ADMIN_ID]:
        db = DataBase(BASE_USERS)
        users = db.get_users()
        for user in users:
            try:
                await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user[0])
            except Exception:
                db.del_user(user[0])
                await message.answer(f'Удалён юзер: {user[1]} id: {user[0]}')
        await message.delete()
