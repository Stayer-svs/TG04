from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Простое меню с reply-кнопками "Привет" и "Пока"
simple_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True
)

# Инлайн-кнопки с URL-ссылками
url_links = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://ria.ru/")],
        [InlineKeyboardButton(text="Музыка", url="https://my.mail.ru/music")],
        [InlineKeyboardButton(text="Видео", url="https://rutube.ru/")]
    ]
)

# Кнопка "Показать больше"
show_more_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ]
)

# Кнопки "Опция 1" и "Опция 2", которые появляются после нажатия "Показать больше"
options_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ]
)
