from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import json
import asyncio

TOKEN = "7798013268:AAHUswLgDnMBR164Tc0IZlS92hs14ECkGvw"
bot = Bot(token=TOKEN)
dp = Dispatcher()


def load_cities():
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            return json.load(f)['cities']
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return []


CITIES = load_cities()


# ================== Клавиатуры ==================
def make_start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🚀 Начать"))
    return builder.as_markup(resize_keyboard=True)


def make_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="🌍 Найти город"),
        KeyboardButton(text="✨ О боте")
    )
    return builder.as_markup(resize_keyboard=True)


def make_travel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="🔍 Новый поиск"),
        KeyboardButton(text="✨ О боте")
    )
    return builder.as_markup(resize_keyboard=True)


# ================== Обработчики ==================
@dp.message(Command("start"))
async def start(message: types.Message):
    start_text = (
        "Привет, будущий путешественник! 👋\n"
        "Я твой цифровой гид по России 🇷🇺\n\n"
        "Готов открывать новые места вместе? "
        "Жми кнопку ниже и погнали! ⬇️"
    )
    await message.answer(start_text, reply_markup=make_start_keyboard())


@dp.message(F.text == "🚀 Начать")
async def start_journey(message: types.Message):
    await message.answer(
        "Супер! Давай сделаем это путешествие незабываемым! 🌟\n"
        "Что тебя интересует?",
        reply_markup=make_main_keyboard()
    )


@dp.message(F.text == "✨ О боте")
async def about(message: types.Message):
    text = (
        "🌟 Я — твой персональный помощник для путешествий!\n\n"
        "В моих знаниях:\n"
        "✅ 15 крупнейших городов России\n"
        "✅ Население и регионы\n"
        "✅ Топовые достопримечательности\n\n"
        "Просто напиши город — и я расскажу всё, что знаю! 😉"
    )
    await message.answer(text)


@dp.message(F.text == "🌍 Найти город")
async def start_search(message: types.Message):
    await message.answer(
        "Отлично! Напиши мне название города,\n"
        "например: <i>Санкт-Петербург</i> или <i>Казань</i> 🏙",
        reply_markup=make_travel_keyboard(),
        parse_mode="HTML"
    )


@dp.message(F.text)
async def handle_city(message: types.Message):
    city_name = message.text.strip().lower()
    found = False

    for city in CITIES:
        if city['name'].lower() == city_name:
            response = (
                    f"🌈 <b>{city['name']}</b> — отличный выбор! Вот что я знаю:\n\n"
                    f"👨👩👧👦 <i>Жителей:</i> {city['population']}\n"
                    f"🗺 <i>Регион:</i> {city['region']}\n\n"
                    "🔝 <u>Главные места:</u>\n" +
                    "\n".join(f"▪️ {lm} 👀" for lm in city['landmarks'])
            )
            await message.answer(response, parse_mode="HTML")
            found = True
            break

    if not found:
        await message.answer(
            "Ой-ой 😯 Такой город мне не знаком...\n"
            "Попробуй что-то из этого списка:\n"
            "• Москва\n• Санкт-Петербург\n• Казань\n"
            "Или проверь написание 🧐",
            parse_mode="HTML"
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())