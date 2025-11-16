import sqlite3
import openpyxl
from database import db

def import_from_excel(file_path: str):
    """
    Імпорт даних з Excel файлу без pandas
    """
    try:
        # Відкриваємо Excel файл
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        
        print(f"Імпорт даних з {file_path}")
        
        imported_count = 0
        error_count = 0
        
        # Пропускаємо заголовок і читаємо дані
        for row in sheet.iter_rows(min_row=2, values_only=True):  # min_row=2 пропускає заголовок
            try:
                if not row or row[0] is None:  # Пропускаємо порожні рядки
                    continue
                
                store_id = str(row[0]).strip() if row[0] else ""  # Колонка A
                address_main = str(row[1]).strip() if row[1] else ""  # Колонка B
                address_additional = str(row[2]).strip() if len(row) > 2 and row[2] else ""  # Колонка C
                schedule = str(row[3]).strip() if len(row) > 3 and row[3] else ""  # Колонка D
                phone = str(row[4]).strip() if len(row) > 4 and row[4] else ""  # Колонка E
                
                # Перевіряємо обов'язкові поля
                if store_id and store_id != 'nan' and phone and phone != 'nan':
                    db.add_store(store_id, phone, address_main, address_additional, schedule)
                    print(f"✅ Додано магазин: {store_id} - {phone} - {address_main}")
                    imported_count += 1
                else:
                    print(f"❌ Пропущено: відсутній store_id або phone")
                    error_count += 1
                    
            except Exception as e:
                print(f"❌ Помилка в рядку: {e}")
                error_count += 1
        
        print(f"\n📊 Підсумок імпорту:")
        print(f"✅ Успішно імпортовано: {imported_count}")
        print(f"❌ Помилок: {error_count}")
        
    except Exception as e:
        print(f"❌ Помилка імпорту: {e}")

if name == "__main__":
    import_from_excel("stores_data.xlsx")
