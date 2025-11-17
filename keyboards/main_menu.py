from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_for_store(store_info, is_admin: bool = False):
    """Меню для користувача з визначеним магазином"""
    keyboard = [
        [KeyboardButton(text="✅ Магазин відкритий")],
        [KeyboardButton(text="🏪 Інформація про магазин")],
        [KeyboardButton(text="📊 Статус всіх магазинів")],
    ]
    
    if is_admin:
        keyboard.append([KeyboardButton(text="📋 Список магазинів")])
    
    keyboard.append([KeyboardButton(text="↩️ На головну")])
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def main_menu_for_selection(is_admin: bool = False):
    """Меню для користувача без визначеного магазину"""
    keyboard = [
        [KeyboardButton(text="📱 Увійти з робочого номеру")],
        [KeyboardButton(text="🏪 Обрати магазин вручну")],
        [KeyboardButton(text="📊 Статус всіх магазинів")],
    ]
    
    if is_admin:
        keyboard.append([KeyboardButton(text="📋 Список магазинів")])
    
    keyboard.append([KeyboardButton(text="ℹ️ Допомога")])
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

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

def phone_keyboard():
    """Клавіатура для запиту номера"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Надіслати мій номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def stores_keyboard(stores):
    """Клавіатура зі списком магазинів для ручного вибору"""
    keyboard = []
    for store in stores:
        btn_text = f"🏪 {store['store_id']} - {store['address_main'][:30]}..."
        keyboard.append([KeyboardButton(text=btn_text)])
    keyboard.append([KeyboardButton(text="↩️ Скасувати")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="↩️ Скасувати")]],
        resize_keyboard=True
    )

def back_to_main_keyboard():
    """Клавіатура з кнопкою На головну"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="↩️ На головну")]],
        resize_keyboard=True
    )
