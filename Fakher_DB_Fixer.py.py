# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - محرك المزامنة الهيدروليكي المطور (نسخة القرص D)
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
اسم الملف وصيغته: Fakher_DB_Fixer.py
الوظيفة: توحيد المسارات السيادية في القرص D وإصلاح هياكل الجداول لمنع التعارض
"""
import sqlite3
import os

# تعديل المسار الحصين ليكون في القرص D بناءً على ذاكرة الحاسوب المعتمدة لديك
TARGET_DIR = "D:/Fakher_System"
DB_TRUCK = os.path.join(TARGET_DIR, "Fakher_Central_Database_2600.db")
DB_CAR = os.path.join(TARGET_DIR, "Fakher_System_2026.db")

def fix_all_infrastructure():
    print("🚀 [منظومة فاخر]: جاري بدء تأمين المسارات السيادية وتصفير الرواسب في القرص D...")
    
    # خوارزمية إنشاء المجلد تلقائياً في القرص D إذا لم يكن موجوداً
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # ----------------------------------------------------
    # 1. تهيئة وتأمين قاعدة بيانات الشاحنات الموحدة (Fakher_Central_Database_2600.db)
    # ----------------------------------------------------
    try:
        # الاتصال بقاعدة البيانات في المسار الجديد بالقرص D
        conn = sqlite3.connect(DB_TRUCK)
        cursor = conn.cursor()
        
        # إنشاء جدول الشاحنات الموحد بالهيكلية البرمجية المعتمدة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Truck_Main_Registry_2600 (
                serial_num TEXT PRIMARY KEY, 
                plate_num TEXT, 
                chassis_num TEXT,
                driver_name TEXT, 
                truck_model TEXT, 
                route_line TEXT,
                work_nature TEXT, 
                current_km TEXT, 
                unit_type TEXT DEFAULT 'Kilometer', 
                auth_code TEXT,
                current_odometer REAL,
                whatsapp_phone TEXT
            )
        """)
        
        # التأكد التلقائي من وجود الأعمدة الحيوية لمنع أخطاء البنية أثناء الربط
        for col in ["unit_type", "auth_code", "current_odometer", "whatsapp_phone"]:
            try:
                cursor.execute(f"ALTER TABLE Truck_Main_Registry_2600 ADD COLUMN {col} TEXT")
            except sqlite3.OperationalError:
                pass # العمود مضاف مسبقاً، تخطي بأمان
                
        conn.commit()
        conn.close()
        print("✅ تم تأمين وضبط هيكلية جدول الشاحنات الموحد في القرص D بنجاح.")
    except Exception as e:
        print(f"⚠️ خطأ أثناء تهيئة قاعدة بيانات الشاحنات: {e}")
        
    # ----------------------------------------------------
    # 2. تهيئة وتأمين قاعدة بيانات السيارات والصيانة (Fakher_System_2026.db)
    # ----------------------------------------------------
    try:
        conn2 = sqlite3.connect(DB_CAR)
        cursor2 = conn2.cursor()
        
        # إنشاء جدول هوية سيارات الصالون الإدارية
        cursor2.execute("""
            CREATE TABLE IF NOT EXISTS Car_Master (
                admin_num TEXT PRIMARY KEY, 
                driver_name TEXT, 
                plate_num TEXT,
                chassis_num TEXT, 
                unit_type TEXT, 
                current_odometer REAL, 
                auth_code TEXT,
                permit_end_year TEXT,
                permit_end_month TEXT,
                permit_end_day TEXT
            )
        """)
        
        # إنشاء جدول سجل صيانة الشاحنات والسيارات
        cursor2.execute("""
            CREATE TABLE IF NOT EXISTS Truck_Maintenance_Logs (
                serial_num TEXT, 
                plate_num TEXT, 
                driver_name TEXT, 
                km_reading REAL,
                workshop_name TEXT, 
                replacement_type TEXT, 
                item_name TEXT, 
                prod_date TEXT, 
                sub_type TEXT, 
                capacity TEXT, 
                supplier_name TEXT, 
                fault_details TEXT, 
                log_date TEXT
            )
        """)
        
        # إنشاء جدول سجلات الحظر والتلاعب الأمني للعدادات الخلفية
        cursor2.execute("""
            CREATE TABLE IF NOT EXISTS Security_Tamper_Logs (
                log_time TEXT, 
                v_type TEXT, 
                v_id TEXT, 
                driver TEXT, 
                err_desc TEXT
            )
        """)
        
        conn2.commit()
        conn2.close()
        print("✅ تم تأمين وضبط جداول السيارات وسجلات الأمان في القرص D بنجاح.")
    except Exception as e:
        print(f"⚠️ خطأ أثناء تهيئة قاعدة بيانات السيارات والصيانة: {e}")

    print("🏁 تم الانتهاء من ضبط البنية التحتية البرمجية 100% في المجلد السيادي D:/Fakher_System.")

if __name__ == "__main__":
    fix_all_infrastructure()