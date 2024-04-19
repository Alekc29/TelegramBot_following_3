from aiogram.types import (KeyboardButton,
                           ReplyKeyboardMarkup,)

admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/Рассылка'),
            KeyboardButton(text='/Статистика'),
            KeyboardButton(text='/Клиент'),
        ]
    ],
    resize_keyboard=True
)

client_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пригласить друзей'),
            KeyboardButton(text='Таблица лидеров'),
        ]
    ],
    resize_keyboard=True
)
