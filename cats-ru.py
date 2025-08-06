import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения списка пород кошек
def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Функция для получения картинки кошки по породе
def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']

# Функция для получения информации о породе кошек
def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None

# Функция для перевода текста с английского на русский с помощью Google Translate API
def translate_text(text, source_lang='en', target_lang='ru'):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': source_lang,
        'tl': target_lang,
        'dt': 't',
        'q': text,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Ответ приходит как вложенный список: [[['перевод', ...], ...], ...]
        result = response.json()
        # собираем переводы из вложенных списков
        translated_segments = [segment[0] for segment in result[0]]
        return ''.join(translated_segments)
    else:
        return text  # В случае ошибки возвращаем исходный текст

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Напиши мне название породы кошки, и я пришлю тебе её фото и описание.")

@dp.message()
async def send_cat_info(message: Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info:
        # Получаем url картинки
        cat_image_url = get_cat_image_by_breed(breed_info['id'])
        # Переводим все текстовые данные
        name_ru = await asyncio.get_event_loop().run_in_executor(None, translate_text, breed_info['name'])
        origin_ru = await asyncio.get_event_loop().run_in_executor(None, translate_text, breed_info['origin'])
        description_ru = await asyncio.get_event_loop().run_in_executor(None, translate_text, breed_info['description'])
        temperament_ru = await asyncio.get_event_loop().run_in_executor(None, translate_text, breed_info['temperament'])
        life_span = breed_info['life_span']
        info = (
            f"Порода: {name_ru}\n"
            f"Происхождение: {origin_ru}\n"
            f"Описание: {description_ru}\n"
            f"Темперамент: {temperament_ru}\n"
            f"Продолжительность жизни: {life_span} лет"
        )
        await message.answer_photo(photo=cat_image_url, caption=info)
    else:
        await message.answer("Порода не найдена. Попробуйте еще раз.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())