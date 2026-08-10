# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - أداة الفحص الجنائي الرقمي والربط المركزي
الوظيفة: فحص البنية التحتية وإنشاء جداول استقبال بيانات تطبيق السائقين تلقائياً.
"""

import sqlite3
import os

DB_PATH = "Fakher_System_2026.db"

def init_and_inspect_database():
    print("==================================================")
    print("🔍 جاري بدء الفحص الشامل وتهيئة الخزنة السيادية...")
    print("==================================================")
    
    # الاتصال بقاعدة البيانات (سيتم إنشاؤها تلقائياً إن لم تكن موجودة)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. إنشاء جدول استقبال قراءات العدادات (إذا لم يكن موجوداً) للربط مع أسطول الـ 200 آلية
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS odometer_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            plate_num TEXT NOT NULL,
            vehicle_type TEXT,
            odo_reading REAL NOT NULL,
            log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. إنشاء جدول استقبال بلاغات الأعطال الفنية (إذا لم يكن موجوداً)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fault_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            plate_num TEXT NOT NULL,
            vehicle_type TEXT,
            fault_category TEXT NOT NULL,
            fault_detail TEXT NOT NULL,
            report_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        print("✅ تم التأكد من جاهزية جداول الاستقبال المركزية (العدادات والأعطال).")
        
        # 3. جلب أسماء الجداول المتواجدة فعلياً للفحص
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"✅ تم العثور على ({len(tables)}) جداول نشطة داخل الخزنة الرقمية:")
        
        # 4. فحص تفاصيل كل جدول
        for table in tables:
            print(f"\n📋 [الجدول الحالي]: {table}")
            print("-" * 40)
            
            cursor.execute(f"PRAGMA table_info({table});")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            print(f"🔹 الأعمدة المتوفرة: {column_names}")
            
            cursor.execute(f"SELECT * FROM {table} LIMIT 3;")
            rows = cursor.fetchall()
            if rows:
                print("📊 عينة من البيانات المخزنة بداخل هذا الجدول:")
                for r in rows:
                    print(f"   -> {r}")
            else:
                print("   ❌ هذا الجدول فارغ حالياً وجاهز لاستقبال البيانات الجديدة.")
                
        conn.close()
    except Exception as e:
        print(f"❌ حدث خطأ أثناء عملية الفحص والتهيئة: {str(e)}")

if __name__ == "__main__":
    init_and_inspect_database()
    input("\n🎯 اضغط Enter لإغلاق شاشة الفحص والمتابعة...")