# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
import os

# المسار السيادي المعتمد
DB_PATH = "D:/Fakher_System/Fakher_System_2026.db"

class DriverGateway:
    def __init__(self):
        self.init_gateway_db()

    def init_gateway_db(self):
        """إنشاء سجلات وصول السائقين للمراقبة"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Driver_Incoming_Messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_name TEXT,
                plate_num TEXT,
                odo_reading REAL,
                message_type TEXT,
                status TEXT,
                received_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def process_data(self, name, plate, odo, m_type):
        """معالجة أمنية فورية للبيانات"""
        # 1. حفظ أولي للبيانات
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Driver_Incoming_Messages (driver_name, plate_num, odo_reading, message_type, status, received_at) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, plate, odo, m_type, "NEW", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        print(f"✅ تم تسجيل رسالة من {name} (شاحنة: {plate}) - العداد: {odo}")
        
        # هنا سنستدعي "العقل المركزي" في الخطوة القادمة للتحليل
        return "تم الحفظ بنجاح"

# اختبار المحرك
if __name__ == "__main__":
    gateway = DriverGateway()
    print("🚀 محرك بوابة الاستقبال (Gateway) يعمل الآن في الخلفية...")