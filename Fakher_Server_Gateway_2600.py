# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - خادم الربط الوسيط المركزي (Server API Gateway)
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم المعتمد للملف: Fakher_Server_Gateway_2600.py
الوظيفة: الوسيط الذكي والمحمي للربط بين تطبيق أندرويد، شبكة الإنترنت، وقاعدة البيانات المركزية.
"""

from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# مسار قاعدة البيانات المركزية
TARGET_DIR = "C:/Fakher_System"
DB_PATH = os.path.join(TARGET_DIR, "Fakher_Central_Database_2600.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# 1. نقطة التحقق من الرمز السري للسائق (Auth PIN)
# ==========================================
@app.route('/api/v1/driver/login', methods=['POST'])
def driver_login():
    data = request.get_json() or {}
    serial_num = data.get('serial_num')
    pin_code = data.get('pin_code')

    if not serial_num or not pin_code:
        return jsonify({"status": "error", "message": "الرجاء إدخال الرقم الإداري والرمز السري"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # البحث في جدول الشاحنات أولاً
    cursor.execute("SELECT serial_num, driver_name, pin_code FROM Truck_Main_Registry_2600 WHERE serial_num = ?", (serial_num,))
    truck = cursor.fetchone()

    if truck:
        if str(truck['pin_code']) == str(pin_code):
            conn.close()
            return jsonify({
                "status": "success",
                "vehicle_type": "truck",
                "driver_name": truck['driver_name'],
                "message": "تم تسجيل الدخول بنجاح للشاحنة"
            }), 200
    else:
        # البحث في جدول السيارات إذا لم يجد الشاحنة
        cursor.execute("SELECT serial_num, driver_name, pin_code FROM Car_Main_Registry_2600 WHERE serial_num = ?", (serial_num,))
        car = cursor.fetchone()
        if car and str(car['pin_code']) == str(pin_code):
            conn.close()
            return jsonify({
                "status": "success",
                "vehicle_type": "car",
                "driver_name": car['driver_name'],
                "message": "تم تسجيل الدخول بنجاح للسيارة"
            }), 200

    conn.close()
    return jsonify({"status": "unauthorized", "message": "الرمز السري أو الرقم الإداري غير صحيح"}), 401

# ==========================================
# 2. نقطة استدعاء بيانات هوية المركبة للتطبيق
# ==========================================
@app.route('/api/v1/vehicle/info', methods=['POST'])
def get_vehicle_info():
    data = request.get_json() or {}
    serial_num = data.get('serial_num')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Truck_Main_Registry_2600 WHERE serial_num = ?", (serial_num,))
    row = cursor.fetchone()
    
    table_name = "Truck"
    if not row:
        cursor.execute("SELECT * FROM Car_Main_Registry_2600 WHERE serial_num = ?", (serial_num,))
        row = cursor.fetchone()
        table_name = "Car"

    conn.close()

    if row:
        vehicle_data = dict(row)
        vehicle_data.pop('auth_code', None)  # إخفاء المفاتيح السيادية من العرض
        return jsonify({"status": "success", "type": table_name, "data": vehicle_data}), 200
    
    return jsonify({"status": "not_found", "message": "المركبة غير مسجلة في قاعدة البيانات"}), 404

# ==========================================
# 3. نقطة استلام بلاغات وتقارير السائقين من أندرويد
# ==========================================
@app.route('/api/v1/driver/report', methods=['POST'])
def receive_driver_report():
    data = request.get_json() or {}
    serial_num = data.get('serial_num')
    report_text = data.get('report_text')
    km_reading = data.get('km_reading')

    if not serial_num or not report_text:
        return jsonify({"status": "error", "message": "بيانات البلاغ غير مكتملة"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # إنشاء جدول للبلاغات الواردة عبر الإنترنت إذا لم يكن موجوداً
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Drivers_Online_Reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_num TEXT,
                km_reading TEXT,
                report_text TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            INSERT INTO Drivers_Online_Reports (serial_num, km_reading, report_text)
            VALUES (?, ?, ?)
        """, (serial_num, km_reading, report_text))
        
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "تم استلام البلاغ وتوثيقه في الخزنة المركزية بنجاح"}), 200

    except Exception as e:
        return jsonify({"status": "database_error", "message": str(e)}), 500

# تشغيل خادم الربط المحلي وعلى شبكة الإنترنت/الأنترانت
if __name__ == '__main__':
    # يعمل على المنفذ 5000 ويستقبل الاتصالات من جميع الأجهزة المرتبطة بالشبكة
    app.run(host='0.0.0.0', port=5000, debug=True)