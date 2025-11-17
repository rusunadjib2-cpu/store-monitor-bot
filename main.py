import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.store_actions import router as store_router
from scheduler import ReportScheduler
from database import db

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Ініціалізація бота та диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Підключення роутерів
    dp.include_router(start_router)
    dp.include_router(store_router)
    
    # Запуск планувальника звітів
    scheduler = ReportScheduler(bot)
    scheduler.start_scheduler()
    
    logger.info("🤖 Бот запущено!")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Помилка: {e}")
    finally:
        scheduler.stop_scheduler()
        await bot.session.close()

# Автоматичний імпорт даних при запуску
if os.getenv("IMPORT_DATA") or not db.get_all_stores():
    from import_data import import_from_excel
    import_from_excel("stores_data.xlsx")
    print("✅ Дані магазинів імпортовано!")

if __name__ == "__main__":
    asyncio.run(main())
def main_menu_default(is_admin: bool = False):
    """Головне меню для повернення"""
    keyboard = [
        [KeyboardButton(text="📱 Увійти з робочого номеру")],
        [KeyboardButton(text="🏪 Обрати магазин вручну")],
    ]
    
    if is_admin:
        keyboard.append([KeyboardButton(text="📊 Статус всіх магазинів")])
        keyboard.append([KeyboardButton(text="📋 Список магазинів")])
    
    keyboard.append([KeyboardButton(text="ℹ️ Допомога")])
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

