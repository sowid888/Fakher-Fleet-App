import sqlite3
import os

# تحديد المسار التلقائي في القرص D (في نفس مجلد الملف)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Fakher_Central_Database_2600.db")

def create_central_vault():
    print("⏳ جاري إنشاء وتجهيز الخزنة المركزية في القرص D...")
    
    # الاتصال بالخزنة (سيتم إنشاؤها تلقائياً إذا لم تكن موجودة)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. جدول هوية الشاحنات الرئيسي (معتمد كود رقم 1)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Truck_Identity_2600 (
            truck_id TEXT PRIMARY KEY,       -- رقم الشاحنة في المنظومة
            chassis_number TEXT,             -- رقم الشاسي
            plate_number TEXT,               -- رقم اللوحة
            truck_model TEXT,                -- موديل/طراز الشاحنة
            max_tonnage REAL,                -- الحمولة القصوى (بالطن)
            status TEXT DEFAULT 'نشط',        -- حالة الشاحنة
            notes TEXT                      -- ملاحظات
        )
    ''')

    # 2. جدول هوية السيارات الصغرى
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cars_Identity_2600 (
            car_id TEXT PRIMARY KEY,
            chassis_number TEXT,
            plate_number TEXT,
            car_model TEXT,
            status TEXT DEFAULT 'نشط'
        )
    ''')

    # 3. جدول الصيانة والتنبيهات (للعمليات المجدولة)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Operations_Log_2600 (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT,
            operation_type TEXT,
            odometer_reading REAL,
            log_date DATE
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ تم إنشاء الخزنة المركزية بنجاح بنسبة 100% في المسار:\n{DB_PATH}")

if __name__ == "__main__":
    create_central_vault()