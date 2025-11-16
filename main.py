import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Налаштування
BOT_TOKEN = "8543789016:AAGxz8IRWvgY4TPnQNpfd4jfCW6ZYljLG3M"

# Ініціалізація
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📱 Надіслати номер", request_contact=True)],
            [types.KeyboardButton(text=ℹ️ Допомога")]
        ],
        resize_keyboard=True
    )
    await message.answer("🤖 Бот запущений! Натисніть кнопку нижче.", reply_markup=keyboard)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("ℹ️ Це тестовий бот для моніторингу магазинів")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("🤖 Бот запущено!")
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
