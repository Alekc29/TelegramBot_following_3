from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассылка'),
            KeyboardButton(text='Статистика'),
        ],
        [
            KeyboardButton(text='Рассылка по топам'),
            KeyboardButton(text='Клиент'),
        ],
        [
            KeyboardButton(text='Новая лотерея'),
            KeyboardButton(text='отмена'),
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

client_en_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Invite friends'),
            KeyboardButton(text='Topboard'),
        ]
    ],
    resize_keyboard=True
)
