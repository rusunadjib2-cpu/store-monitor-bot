import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Налаштування
BOT_TOKEN = "ВАШ_ТОКЕН_ТУТ"  # Замініть на реальний токен
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Перевірити статус")],
            [types.KeyboardButton(text="Допомога")]
        ],
        resize_keyboard=True
    )
    await message.answer("Вітаю! Оберіть опцію:", reply_markup=keyboard)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Це бот для моніторингу магазинів. Використовуйте кнопки для навігації.")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущено!")
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
