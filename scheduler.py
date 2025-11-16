from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from database import db
from config import ADMIN_IDS
import datetime
import logging

logger = logging.getLogger(__name__)

class ReportScheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
    
    async def send_report(self, report_type: str):
        """Надсилання звіту про невідкриті магазини"""
        not_opened_stores = db.get_not_opened_stores()
        current_time = datetime.datetime.now().strftime('%H:%M')
        
        if report_type == "first":
            title = f"🕒 ЗВІТ О 7:50 - МАГАЗИНИ ЩЕ НЕ ВІДКРИТІ"
        else:
            title = f"⏰ ЗВІТ О 8:00 - МАГАЗИНИ ЩЕ НЕ ВІДКРИТІ"
        
        if not_opened_stores:
            message = f"""
{title}

❌ Не відкрито {len(not_opened_stores)} магазинів:

"""
            for store in not_opened_stores:
                message += f"\n🏪 {store['store_id']}"
                message += f"\n📍 {store['address_main']}"
                message += f"\n📞 {store['phone']}"
                message += f"\n🕒 Графік: {store['schedule']}"
                message += f"\n────────────────────"
            
            message += f"\n\n*Час формування звіту: {current_time}*"
        else:
            message = f"""
{title}

🎉 Всі магазини успішно відкриті!

*Час формування звіту: {current_time}*
"""
        
        # Надсилаємо звіт всім адміністраторам
        for admin_id in ADMIN_IDS:
            try:
                await self.bot.send_message(admin_id, message)
            except Exception as e:
                logger.error(f"Помилка відправки адміністратору {admin_id}: {e}")
    
    async def clear_daily_data(self):
        """Щоденне очищення даних про відкриття"""
        try:
            # Отримуємо вчорашню дату
            yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Видаляємо старі записи (можна змінити на певну кількість днів)
            cursor = db.conn.cursor()
            cursor.execute('DELETE FROM store_openings WHERE DATE(open_time) = ?', (yesterday,))
            db.conn.commit()
            
            logger.info(f"✅ Дані за {yesterday} очищено")
            
            # Сповіщення адмінів
            for admin_id in ADMIN_IDS:
                try:
                    await self.bot.send_message(admin_id, f"🔄 Дані за {yesterday} автоматично очищено. Початок нового робочого дня!")
                except Exception as e:
                    logger.error(f"Помилка сповіщення адміністратора {admin_id}: {e}")
                    
        except Exception as e:
            logger.error(f"Помилка очищення даних: {e}")
    
    def start_scheduler(self):
        """Запуск планувальника"""
        # Перший звіт о 7:50
        self.scheduler.add_job(
            self.send_report,
            trigger=CronTrigger(hour=7, minute=50),
            args=["first"],
            id="first_report"
        )
        
        # Другий звіт о 8:00
        self.scheduler.add_job(
            self.send_report,
            trigger=CronTrigger(hour=8, minute=0),
            args=["second"],
            id="second_report"
        )
        
        # Очищення даних о 00:01
        self.scheduler.add_job(
            self.clear_daily_data,
            trigger=CronTrigger(hour=0, minute=1),
            id="clear_data"
        )
        
        self.scheduler.start()
        logger.info("🕒 Планувальник звітів запущено")

    def stop_scheduler(self):
        """Зупинка планувальника"""
        self.scheduler.shutdown()
