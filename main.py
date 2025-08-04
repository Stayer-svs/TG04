import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработка команды /start — показывает простое меню с кнопками "Привет" и "Пока"
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f'Привет, {message.from_user.first_name}! Выбери действие:',
        reply_markup=kb.simple_menu
    )

# Обработка reply-кнопки "Привет"
@dp.message(F.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

# Обработка reply-кнопки "Пока"
@dp.message(F.text == "Пока")
async def say_goodbye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Обработка команды /links — показывает 3 инлайн-кнопки с URL-ссылками
@dp.message(Command('links'))
async def show_links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=kb.url_links)

# Обработка команды /dynamic — показывает кнопку "Показать больше"
@dp.message(Command('dynamic'))
async def dynamic_menu(message: Message):
    await message.answer("Нажмите, чтобы показать больше:", reply_markup=kb.show_more_button)

# Обработка callback-кнопки "Показать больше"
@dp.callback_query(F.data == 'show_more')
async def show_options(callback: CallbackQuery):
    await callback.message.edit_text("Выберите опцию:", reply_markup=kb.options_buttons)

# Обработка callback-кнопок "Опция 1" и "Опция 2"
@dp.callback_query(F.data.in_(['option_1', 'option_2']))
async def option_selected(callback: CallbackQuery):
    option_text = "Опция 1" if callback.data == 'option_1' else "Опция 2"
    await callback.answer()
    await callback.message.answer(f"Вы выбрали: {option_text}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
