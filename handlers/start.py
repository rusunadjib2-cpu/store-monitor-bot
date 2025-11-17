from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Contact
from database import db
from keyboards.main_menu import main_menu_for_store, main_menu_for_selection, phone_keyboard
from config import ADMIN_IDS  # Додано імпорт

router = Router()

# Словник для тимчасового зберігання стану користувачів
user_states = {}

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    
    # Додаємо користувача як адміна, якщо він в списку адмінів
    if user_id in ADMIN_IDS:  # Використовуємо ADMIN_IDS з config
        db.add_admin(user_id, username, full_name)
    
    is_admin = db.is_admin(user_id)
    
    welcome_text = """
🏪 Вітаю в системі моніторингу магазинів!

Оберіть спосіб входу:
📱 Увійти з робочого номеру - система автоматично визначить ваш магазин
🏪 Обрати магазин вручну - якщо використовуєте особистий телефон

*Адміністратори мають додаткові функції*
    """
    
    await message.answer(welcome_text, reply_markup=main_menu_for_selection(is_admin))

@router.message(F.text == "📱 Увійти з робочого номеру")
async def request_work_phone(message: types.Message):
    await message.answer(
        "📱 Натисніть кнопку нижче, щоб надіслати ваш робочий номер телефону.\n"
        "Система автоматично знайде ваш магазин:",
        reply_markup=phone_keyboard()
    )

@router.message(F.text == "🏪 Обрати магазин вручну")
async def select_store_manually(message: types.Message):
    from handlers.store_actions import show_stores_for_selection
    await show_stores_for_selection(message)

@router.message(F.text == "🔄 Змінити магазин")
async def change_store(message: types.Message):
    # Очищаємо стан користувача
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    is_admin = db.is_admin(user_id)
    await message.answer(
        "🔄 Оберіть спосіб ідентифікації магазину:",
        reply_markup=main_menu_for_selection(is_admin)
    )

@router.message(F.contact)
async def handle_contact(message: types.Message):
    """Обробка надісланого контакту"""
    contact: Contact = message.contact
    user_id = message.from_user.id
    user_phone = contact.phone_number
    
    # Шукаємо магазин за номером телефону
    store = db.get_store_by_phone(user_phone)
    
    if store:
        # Магазин знайдено - зберігаємо в стані користувача
        user_states[user_id] = {
            'store_id': store['store_id'],
            'from_work_phone': True
        }
        
        is_admin = db.is_admin(user_id)
        
        success_text = f"""
✅ Магазин автоматично ідентифіковано!

🏪 ID: {store['store_id']}
📍 Адреса: {store['address_main']}
{store['address_additional'] if store['address_additional'] else ''}
📞 Робочий номер: {store['phone']}
🕒 Графік: {store['schedule']}

Тепер ви можете позначати магазин відкритим.
        """
        
        await message.answer(success_text, reply_markup=main_menu_for_store(store, is_admin))
        
    else:
        # Магазин не знайдено
        is_admin = db.is_admin(user_id)
        error_text = f"""
❌ Магазин не знайдено

Номер {user_phone} не прив'язаний до жодного магазину.

Можливі причини:
• Ви використовуєте особистий номер замість робочого
• Робочий номер не додано в систему
• Помилка в базі даних

Спробуйте Обрати магазин вручну або зверніться до адміністратора.
        """
        await message.answer(error_text, reply_markup=main_menu_for_selection(is_admin))

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
📋 Інструкція по використанню:

Для співробітників:

📱 Увійти з робочого номеру - автоматична ідентифікація магазину
🏪 Обрати магазин вручну - вибір магазину зі списку
✅ Магазин відкритий - позначити відкриття магазину
🏪 Інформація про магазин - дані вашого магазину
🔄 Змінити магазин - обрати інший магазин

Для адміністраторів:
📊 Статус всіх магазинів - перегляд статусів
📋 Список магазинів - всі магазини з контактами

Автоматичні звіти:
🕒 7:50 - попередній звіт про невідкриті магазини
🕒 8:00 - фінальний звіт про невідкриті магазини
    """
    await message.answer(help_text)
@router.message(F.text == "↩️ На головну")
async def back_to_main_menu(message: types.Message):
    """Повернення в головне меню"""
    user_id = message.from_user.id
    is_admin = db.is_admin(user_id)
    
    # Очищаємо стан користувача
    if user_id in user_states:
        del user_states[user_id]
    
    await message.answer(
        "Головне меню:",
        reply_markup=main_menu_for_selection(is_admin)
    )
@router.message(F.text == "↩️ На головну")
async def back_to_main_menu(message: types.Message):
    """Повернення в головне меню"""
    user_id = message.from_user.id
    
    # Очищаємо стан користувача
    if user_id in user_states:
        del user_states[user_id]
    
    is_admin = db.is_admin(user_id)
    await message.answer(
        "Головне меню:",
        reply_markup=main_menu_default(is_admin)
    )
@router.message(F.text == "↩️ На головну")
async def back_to_main_menu(message: types.Message):
    """Повернення в головне меню"""
    user_id = message.from_user.id
    
    # Очищаємо стан користувача
    if user_id in user_states:
        del user_states[user_id]
    
    is_admin = db.is_admin(user_id)
    await message.answer(
        "Головне меню:",
        reply_markup=main_menu_default(is_admin)
    )
