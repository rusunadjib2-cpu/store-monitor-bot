import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.store_actions import router as store_router
from scheduler import ReportScheduler

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
import os

# Автоматичний імпорт даних при запуску
if os.getenv("IMPORT_DATA") or not db.get_all_stores():
    from import_data import import_from_excel
    import_from_excel("stores_data.xlsx")
    print("✅ Дані магазинів імпортовано!")
if __name__ == "__main__":
    asyncio.run(main())
import os

# Автоматичний імпорт даних при запуску
if os.getenv("IMPORT_DATA") or not db.get_all_stores():
    from import_data import import_from_excel
    import_from_excel("stores_data.xlsx")
    print("✅ Дані магазинів імпортовано!")

if name == "__main__":
    asyncio.run(main())

