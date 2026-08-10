import sqlite3
import os
import time
import requests
import json
from datetime import datetime

# مسار قاعدة البيانات المركزية لبرنامج الشركة
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Fakher_Central_Database_2600.db")

# رابط Firebase Realtime Database
FIREBASE_URL = "https://algazi26-default-rtdb.firebaseio.com/Reports.json"

class FirebaseCentralListener:
    def __init__(self):
        self.processed_ids = set()
        self.init_incoming_tables()

    def init_incoming_tables(self):
        """إنشاء جداول استقبال البلاغات الواردة داخل الخزنة المركزية"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # جدول بلاغات الشاحنات الواردة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Truck_Reports_Incoming_2600 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firebase_key TEXT UNIQUE,
                    driver_phone TEXT,
                    driver_name TEXT,
                    truck_identifier TEXT,
                    plate_number TEXT,
                    odometer_reading REAL,
                    report_details TEXT,
                    receive_time TEXT
                )
            ''')

            # جدول بلاغات السيارات الواردة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Car_Reports_Incoming_2600 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firebase_key TEXT UNIQUE,
                    driver_phone TEXT,
                    driver_name TEXT,
                    car_identifier TEXT,
                    plate_number TEXT,
                    odometer_reading REAL,
                    report_details TEXT,
                    receive_time TEXT
                )
            ''')

            conn.commit()
            conn.close()
            print("✅ تم تجهيز جداول استقبال البلاغات في الخزنة المركزية بنجاح.")
        except Exception as e:
            print(f"🛑 خطأ أثناء تهيئة جداول الاستقبال: {e}")

    def verify_driver_and_route(self, phone, vehicle_code):
        """التحقق من رقم الهاتف في ملفات الهوية (شاحنة أم سيارة)"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. البحث في جدول هوية الشاحنات
        cursor.execute("SELECT serial_number, plate_number FROM Truck_Identity_Full_2600 WHERE whatsapp_no=?", (phone,))
        truck = cursor.fetchone()
        if truck:
            conn.close()
            return "Truck", truck[1]

        # 2. البحث في جدول هوية السيارات
        cursor.execute("SELECT serial_number, plate_number FROM Car_Identity_Full_2600 WHERE whatsapp_no=?", (phone,))
        car = cursor.fetchone()
        if car:
            conn.close()
            return "Car", car[1]

        conn.close()
        return None, None

    def process_report(self, report_key, data):
        """معالجة وتوجيه البلاغ الوارد من السيرفر"""
        phone = data.get("driver_phone", "").strip()
        driver_name = data.get("driver_name", "").strip()
        vehicle_code = data.get("vehicle_code", "").strip()  # مثل: إيسوزو تيربو / إيسوزو عادي
        plate_no = data.get("plate_number", "").strip()
        odometer = data.get("odometer_reading", 0.0)
        report_text = data.get("report_text", "").strip()
        rec_time = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        v_type, registered_plate = self.verify_driver_and_route(phone, vehicle_code)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if v_type == "Truck":
            cursor.execute('''
                INSERT OR IGNORE INTO Truck_Reports_Incoming_2600 
                (firebase_key, driver_phone, driver_name, truck_identifier, plate_number, odometer_reading, report_details, receive_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (report_key, phone, driver_name, vehicle_code, plate_no or registered_plate, odometer, report_text, rec_time))
            print(f"🚚 [تم التوجيه بنجاح]: بلاغ شاحنة جديدة من السائق ({driver_name}) - المركبة: ({vehicle_code})")

        elif v_type == "Car":
            cursor.execute('''
                INSERT OR IGNORE INTO Car_Reports_Incoming_2600 
                (firebase_key, driver_phone, driver_name, car_identifier, plate_number, odometer_reading, report_details, receive_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (report_key, phone, driver_name, vehicle_code, plate_no or registered_plate, odometer, report_text, rec_time))
            print(f"🚗 [تم التوجيه بنجاح]: بلاغ سيارة جديدة من السائق ({driver_name}) - المركبة: ({vehicle_code})")

        else:
            print(f"⚠️ [تحذير أمني]: بلاغ مرفوض! رقم الهاتف ({phone}) غير مسجل في هوية الشاحنات أو السيارات.")

        conn.commit()
        conn.close()

    def start_listening(self):
        """بدء حلقة المراقبة اللحظية للبلاغات من Firebase"""
        print("🌐 بدء الاستماع المباشر لسيرفر Firebase (algazi26)...")
        while True:
            try:
                response = requests.get(FIREBASE_URL, timeout=10)
                if response.status_code == 200 and response.json():
                    reports = response.json()
                    for r_key, r_data in reports.items():
                        if r_key not in self.processed_ids:
                            self.process_report(r_key, r_data)
                            self.processed_ids.add(r_key)
            except Exception as e:
                print(f"🔄 جاري إعادة الاتصال بالسيرفر... ({e})")
            
            time.sleep(5)  # الفحص كل 5 ثوانٍ

if __name__ == "__main__":
    listener = FirebaseCentralListener()
    listener.start_listening()