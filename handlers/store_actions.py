from aiogram import Router, types, F
from aiogram.filters import Command
from database import db
from keyboards.main_menu import main_menu_for_store, main_menu_for_selection, stores_keyboard, main_menu_default
from handlers.start import user_states

router = Router()

@router.message(F.text == "📊 Статус всіх магазинів")
async def show_all_stores_status(message: types.Message):
    """Статус магазинів для всіх користувачів"""
    all_stores = db.get_all_stores()
    opened_stores = db.get_today_opened_stores()
    
    if not all_stores:
        await message.answer("❌ Інформація тимчасово недоступна")
        return
    
    opened_count = len(opened_stores)
    total_count = len(all_stores)
    
    response = f"""
📊 Статус магазинів на {message.date.strftime('%d.%m.%Y %H:%M')}

✅ Відкрито: {opened_count}/{total_count}
❌ Не відкрито: {total_count - opened_count}/{total_count}

📈 Прогрес: {round((opened_count/total_count)*100)}%

Список магазинів:
"""
    
    for store in all_stores:
        status = "✅" if store['store_id'] in opened_stores else "❌"
        response += f"\n{status} {store['store_id']} - {store['address_main']}"
    
    await message.answer(response)

@router.message(F.text == "📋 Список магазинів")
async def show_all_stores_list(message: types.Message):
    if not db.is_admin(message.from_user.id):
        await message.answer("❌ Доступ заборонено. Ця функція тільки для адміністраторів.")
        return
    
    all_stores = db.get_all_stores()
    
    if not all_stores:
        await message.answer("❌ Магазини не знайдені в базі даних")
        return
    
    response = "📋 **Список всіх магазинів:**\n\n"
    
    for store in all_stores:
        response += f"🏪 **{store['store_id']}**\n"
        response += f"📍 {store['address_main']}\n"
        response += f"📞 {store['phone']}\n"
        response += f"🕒 {store['schedule']}\n"
        response += f"────────────────────\n"
    
    await message.answer(response)

async def show_stores_for_selection(message: types.Message):
    """Показати список магазинів для ручного вибору"""
    stores = db.get_all_stores()
    
    if not stores:
        await message.answer("❌ Магазини не знайдені в базі даних")
        return
    
    await message.answer(
        "🏪 Оберіть ваш магазин зі списку:",
        reply_markup=stores_keyboard(stores)
    )

@router.message(F.text.startswith("🏪"))
async def handle_store_selection(message: types.Message):
    """Обробка вибору магазину зі спику"""
    if message.text == "↩️ Скасувати":
        is_admin = db.is_admin(message.from_user.id)
        await message.answer("Операцію скасовано", reply_markup=main_menu_default(is_admin))
        return
    
    try:
        # Парсимо ID магазину з тексту кнопки
        store_id = message.text.split(" - ")[0].replace("🏪 ", "").strip()
        store = db.get_store_by_id(store_id)
        
        if store:
            # Зберігаємо вибір користувача
            user_id = message.from_user.id
            user_states[user_id] = {
                'store_id': store['store_id'],
                'from_work_phone': False  # Обрано вручну
            }
            
            is_admin = db.is_admin(user_id)
            
            store_info = f"""
✅ Магазин обрано!

🏪 ID: {store['store_id']}
📍 Адреса: {store['address_main']}
{store['address_additional'] if store['address_additional'] else ''}
📞 Робочий номер: {store['phone']}
🕒 Графік: {store['schedule']}

Тепер ви можете позначати магазин відкритим.
            """
            await message.answer(store_info, reply_markup=main_menu_for_store(store, is_admin))
        else:
            await message.answer("❌ Магазин не знайдено")
    
    except Exception as e:
        await message.answer("❌ Помилка при обробці запиту")

@router.message(F.text == "✅ Магазин відкритий")
async def mark_store_opened(message: types.Message):
    user_id = message.from_user.id
    
    # Перевіряємо, чи має користувач обраний магазин
    if user_id not in user_states:
        is_admin = db.is_admin(user_id)
        await message.answer(
            "❌ Спочатку оберіть ваш магазин",
            reply_markup=main_menu_default(is_admin)
        )
        return
    
    store_id = user_states[user_id]['store_id']
    from_work_phone = user_states[user_id]['from_work_phone']
    
    store = db.get_store_by_id(store_id)
    if not store:
        await message.answer("❌ Магазин не знайдено")
        return
    
    # Позначаємо магазин відкритим
    success = db.mark_store_opened(
        store_id, 
        user_id, 
        store['phone'] if from_work_phone else None,
        from_work_phone
    )
    
    if success:
        method = "автоматично" if from_work_phone else "вручну"
        response = f"""
✅ Магазин успішно відкрито!

🏪 ID: {store['store_id']}
📍 Адреса: {store['address_main']}
🕒 Час відкриття: {message.date.strftime('%H:%M')}
👤 Відкрито: {message.from_user.full_name}
📱 Метод: {method}

Дякуємо за оперативність!
        """
    else:
        response = "ℹ️ Магазин вже було відкрито сьогодні раніше"
    
    is_admin = db.is_admin(user_id)
    await message.answer(response, reply_markup=main_menu_for_store(store, is_admin))

@router.message(F.text == "🏪 Інформація про магазин")
async def show_store_info(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_states:
        is_admin = db.is_admin(user_id)
        await message.answer(
            "❌ Спочатку оберіть ваш магазин",
            reply_markup=main_menu_default(is_admin)
        )
        return
    
    store_id = user_states[user_id]['store_id']
    store = db.get_store_by_id(store_id)
    
    if not store:
        await message.answer("❌ Магазин не знайдено")
        return
    
    # Перевіряємо, чи відкрито сьогодні
    opened_stores = db.get_today_opened_stores()
    status = "✅ Відкрито сьогодні" if store_id in opened_stores else "❌ Ще не відкрито"
    
    method = "Автоматично (робочий номер)" if user_states[user_id]['from_work_phone'] else "Вручну"
    
    store_info = f"""
🏪 Інформація про ваш магазин

📋 ID: {store['store_id']}
📍 Адреса: {store['address_main']}
{store['address_additional'] if store['address_additional'] else ''}
📞 Робочий номер: {store['phone']}
🕒 Графік: {store['schedule']}
📊 Статус: {status}
🔧 Метод ідентифікації: {method}
    """
    
    is_admin = db.is_admin(user_id)
    await message.answer(store_info, reply_markup=main_menu_for_store(store, is_admin))

@router.message(Command("status"))
async def show_public_status(message: types.Message):
    """Публічний статус для всіх користувачів"""
    all_stores = db.get_all_stores()
    opened_stores = db.get_today_opened_stores()
    
    if not all_stores:
        await message.answer("❌ Інформація тимчасово недоступна")
        return
    
    opened_count = len(opened_stores)
    total_count = len(all_stores)
    
    response = f"""
📊 СТАТУС МАГАЗИНІВ 
на {message.date.strftime('%d.%m.%Y %H:%M')}

✅ Відкрито: {opened_count}/{total_count}
❌ Не відкрито: {total_count - opened_count}/{total_count}

📈 Прогрес: {round((opened_count/total_count)*100)}%
    
ℹ️ Статус оновлюється в реальному часі
    """
    
    await message.answer(response)

@router.message(F.text == "↩️ На головну")
async def back_to_main_from_store(message: types.Message):
    """Повернення на головну з меню магазину"""
    user_id = message.from_user.id
    
    # Очищаємо стан користувача
    if user_id in user_states:
        del user_states[user_id]
    
    is_admin = db.is_admin(user_id)
    await message.answer(
        "Головне меню:",
        reply_markup=main_menu_default(is_admin)
    )
