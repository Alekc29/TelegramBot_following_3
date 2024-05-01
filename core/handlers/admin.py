from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import DEV_ID
from core.keyboards.replykey import admin
from core.utils.class_fsm import FSMPost, FSMPostTop
from core.utils.data_base import DataBase

router = Router()


@router.message(Command('moderator'))
async def get_admin_keyboards(message: Message):
    if message.from_user.id == DEV_ID:
        await message.answer('Что босс надо?',
                             reply_markup=admin)
        await message.delete()
    else:
        await message.answer('Вы не являетесь администратором бота.')
        await message.delete()


@router.message(F.text == 'Рассылка')
async def mailing_post_bot(message: Message, state: FSMContext):
    ''' функция для получения сообщения для рассылки по всем пользователям. '''
    if message.from_user.id == DEV_ID:
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
    if message.from_user.id == DEV_ID:
        db = DataBase('users.db')
        users = db.get_users()
        await send_message_to_users(users, message, bot)
        await message.answer(
            f"Рассылка сообщения завершена. Отправлено сообщений: {len(users)}"
        )
        await state.clear()


@router.message(F.text == 'Статистика')
async def get_statistics(message: Message):
    if message.from_user.id == DEV_ID:
        db = DataBase('users.db')
        await message.answer(f'Кол-во юзеров: {db.count_all_users()}')
        await message.delete()


@router.message(F.text == 'Клиент')
async def change_client_command(message: Message):
    if message.from_user.id == DEV_ID:
        await message.answer('Вы перешли в клиентскую часть.',
                             reply_markup=ReplyKeyboardRemove())
        await message.delete()


@router.message(F.text == 'Рассылка по топам')
async def mailing_post_top_bot(message: Message, state: FSMContext):
    ''' функция для получения сообщения для рассылки по топам. '''
    if message.from_user.id == DEV_ID:
        await message.answer('Набери пост для рассылки по топам.')
        await message.delete()
        await state.set_state(FSMPostTop.post_top)


@router.message(FSMPostTop.post_top)
async def send_top_mailing_bot(message: Message,
                           bot: Bot,
                           state: FSMContext):
    ''' функция ловит сообщение для рассылки по топам. '''
    if message.from_user.id == DEV_ID:
        db = DataBase('lot.db')
        users = db.get_top_rang_users()
        await send_message_to_users(users, message, bot)
        await message.answer(
            f"Рассылка сообщения завершена. Отправлено сообщений: {len(users)}"
        )
        await state.clear()


@router.message(F.text == 'Новая лотерея')
async def change_client_command(message: Message):
    if message.from_user.id == DEV_ID:
        try:
            db = DataBase('lot.db')
            db.del_table()
            await message.answer('База старой лотереи удалена. Новая база создана.')
            await message.delete()
        except:
            await message.answer('Произошла ошибка при удалении базы.')