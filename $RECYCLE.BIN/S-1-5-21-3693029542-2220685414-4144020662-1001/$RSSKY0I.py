# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - واجهة إدارة حركة السيطرة المركزية (توليد بوابة ويب سيارات الصالون)
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد: Fakher_Car_Driver_WhatsApp_2600.py
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

DB_PATH = "Fakher_System_2026.db"

class FakherCarDriverWhatsApp2600:
    def __init__(self, root):
        self.root = root
        self.root.title("منظومة فاخر 2600 - السيطرة المركزية لتوليد ملفات السيارات")
        self.root.geometry("650x400")
        self.root.configure(bg="#0f172a")
        
        self.init_car_database()
        self.generate_html_car_gateway()
        self.build_control_ui()

    def init_car_database(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS car_odometer_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plate_num TEXT,
                    driver_name TEXT,
                    km_reading REAL,
                    date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS car_fuel_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plate_num TEXT,
                    driver_name TEXT,
                    liters REAL,
                    bill_number TEXT,
                    payment_type TEXT,
                    station_name TEXT,
                    date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Car_Fault_Logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plate_num TEXT,
                    driver_name TEXT,
                    fault_category TEXT,
                    fault_detail TEXT,
                    log_date TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database Error: {e}")

    def generate_html_car_gateway(self):
        html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة سائق السيارات الصالون والفرعية - فاخر 2600</title>
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #0f172a; color: #ffffff; text-align: center; padding: 10px; margin: 0; }
        .container { max-width: 500px; margin: auto; background: #1e293b; padding: 15px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3); }
        h2 { color: #38bdf8; font-size: 1.4rem; margin-bottom: 5px; }
        h3 { color: #f43f5e; font-size: 1.1rem; margin-top: 0; }
        .section { background: #0f172a; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #334155; text-align: right; }
        .section-title { font-weight: bold; color: #38bdf8; margin-bottom: 8px; display: block; font-size: 1rem; }
        label { display: block; margin: 6px 0 3px 0; font-size: 0.9rem; color: #cbd5e1; }
        input, select, textarea { width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #475569; background: #334155; color: #fff; font-size: 1rem; box-sizing: border-box; font-weight: bold; }
        .btn { display: width; width: 100%; padding: 12px; margin: 8px 0; border: none; border-radius: 5px; font-size: 1rem; font-weight: bold; cursor: pointer; color: white; }
        .btn-km { background-color: #e11d48; }
        .btn-fuel { background-color: #ca8a04; color: black; }
        .btn-fault { background-color: #16a34a; margin: 5px 0; font-size: 0.95rem; }
        .btn-free { background-color: #7c3aed; }
        .alert-box { background: #4c0519; border: 1px solid #f43f5e; padding: 8px; border-radius: 5px; color: #fecdd3; font-size: 0.85rem; margin-top: 8px; font-weight: bold; }
    </style>
</head>
<body>

<div class="container">
    <h2>📱 بوابة سائق السيارات الصالون والفرعية 📱</h2>
    <h3>منظومة فاخر السيادية 2600</h3>
    
    <!-- 1. هوية السيارة والسائق -->
    <div class="section">
        <span class="section-title">👤 [ 1. هوية السيارة والسائق الثابتة ]</span>
        <label>اسم المستخدم / السائق:</label>
        <input type="text" id="driver_name" value="محمد علي الناشري">
        
        <label>رقم اللوحة المعدنية:</label>
        <input type="text" id="plate_num" value="أ ب 200">
    </div>

    <!-- 2. قراءات العداد -->
    <div class="section">
        <span class="section-title">📟 [ 2. قراءات العداد الحركية اليومية ]</span>
        <label>قراءة العداد الحالية (كم / ميل):</label>
        <input type="number" id="current_km" placeholder="ادخل العداد الحالي">
        <button class="btn btn-km" onclick="sendOdometer()">🚀 إرسال قراءة العداد الحالية فقط</button>
    </div>

    <!-- 3. وقود السيارة -->
    <div class="section">
        <span class="section-title">⛽ [ 3. مراقبة تزويد وقود السيارة ]</span>
        <label>الكمية (لتر):</label>
        <input type="number" id="fuel_liters" placeholder="عدد اللترات">
        
        <label>رقم الفاتورة:</label>
        <input type="text" id="bill_number" placeholder="رقم الفاتورة">
        
        <label>نوع التعبئة:</label>
        <select id="payment_type">
            <option>اتفاق شركة (بالآجل)</option>
            <option>كاش (مسترد عند الوصول)</option>
        </select>
        
        <label>المحطة:</label>
        <input type="text" id="station_name" placeholder="اسم المحطة">
        
        <button class="btn btn-fuel" onclick="sendFuel()">⛽ إرسال وقود السيارة وحساب الاستهلاك</button>
    </div>

    <!-- 4. الأعطال المعتمدة للسيارات -->
    <div class="section">
        <span class="section-title">🛠️ [ 4. قائمة تسجيل أعطال السيارة المعتمدة ]</span>
        
        <label style="color: #f87171; font-weight: bold;">⚙️ أعطال ميكانيكية:</label>
        <button class="btn btn-fault" onclick="sendFault('حرارة المحرك مرتفعة', 'ميكانيكية')">حرارة المحرك مرتفعة</button>
        <button class="btn btn-fault" onclick="sendFault('صوت غريب أسفل السيارة', 'ميكانيكية')">صوت غريب أسفل السيارة</button>
        <button class="btn btn-fault" onclick="sendFault('نقص مستمر في زيت المحرك', 'ميكانيكية')">نقص مستمر في زيت المحرك</button>
        <button class="btn btn-fault" onclick="sendFault('تهريب ماء الرديتر', 'ميكانيكية')">تهريب ماء الرديتر</button>
        
        <label style="color: #facc15; font-weight: bold; margin-top: 10px;">⚡ أعطال كهربائية:</label>
        <button class="btn btn-fault" onclick="sendFault('البطارية ضعيفة والسيارة لا تعمل', 'كهربائية')">البطارية ضعيفة والسيارة لا تعمل</button>
        <button class="btn btn-fault" onclick="sendFault('مكيف السيارة لا يبرد', 'كهربائية')">مكيف السيارة لا يبرد</button>
        <button class="btn btn-fault" onclick="sendFault('الانارة الأمامية أو الخلفية عاطلة', 'كهربائية')">الانارة عاطلة</button>
        
        <label style="color: #60a5fa; font-weight: bold; margin-top: 10px;">🛑 أعطال البريك:</label>
        <button class="btn btn-fault" onclick="sendFault('صوت صفير عند الضغط على البريك', 'البريك')">صوت صفير عند البريك</button>
        <button class="btn btn-fault" onclick="sendFault('البريك ضعيف ويحتاج مسافة طويلة', 'البريك')">البريك ضعيف جداً</button>
    </div>

    <!-- 5. ملاحظات حرة -->
    <div class="section">
        <span class="section-title">🎙️ [ 5. ملاحظات وأعطال حرة ]</span>
        <textarea id="manual_fault" rows="3" placeholder="اكتب هنا أي عطل أو شكوى حرة..."></textarea>
        <button class="btn btn-free" onclick="sendFreeFault()">🚀 إرسال البلاغ الحر للسيارة</button>
    </div>

    <!-- صندوق التنبيهات الدوري المخصص للسيارات -->
    <div class="section" style="border-color: #f43f5e;">
        <span class="section-title" style="color: #f43f5e;">🔔 [ صندوق التنبيهات الدوري للسيارات الصالون ]</span>
        <div class="alert-box">⚠️ تنبيه أمن وسلامة: فحص مستوى زيت المحرك والماء الاحتياطي قبل تشغيل السيارة صباحاً.</div>
        <div class="alert-box">🧼 تذكير النظافة: يرجى تنظيف وتطهير مقصورة السيارة الصالون نهاية كل أسبوع.</div>
    </div>
</div>

<script>
    // ضع رقمك المعتمد هنا بدلاً من الرقم التجريبي
    const MY_PHONE = "966500000000"; 

    function getBaseData() {
        return {
            driver: document.getElementById('driver_name').value.trim(),
            plate: document.getElementById('plate_num').value.trim()
        };
    }

    function openWhatsApp(text) {
        let url = "https://api.whatsapp.com/send?phone=" + MY_PHONE + "&text=" + encodeURIComponent(text);
        window.open(url, '_blank');
    }

    function sendOdometer() {
        let base = getBaseData();
        let km = document.getElementById('current_km').value.trim();
        if(!km || km === "0") { alert("❌ يرجى إدخال قراءة العداد الصحيحة!"); return; }
        
        let msg = "📟 *تقرير عداد الحركة اليومي (سيارة صالون) - 2600* 📟\\n\\n" +
                  "🚗 *رقم اللوحة:* " + base.plate + "\\n" +
                  "👤 *المستلم/السائق:* " + base.driver + "\\n" +
                  "🛣️ *قراءة العداد الحالية:* " + km + " كم/ميل\\n\\n" +
                  "⏳ *التوقيت:* " + new Date().toLocaleString('ar-EG');
        openWhatsApp(msg);
    }

    function sendFuel() {
        let base = getBaseData();
        let liters = document.getElementById('fuel_liters').value.trim();
        let bill = document.getElementById('bill_number').value.trim();
        let payType = document.getElementById('payment_type').value;
        let station = document.getElementById('station_name').value.trim() || "غير محددة";
        let km = document.getElementById('current_km').value.trim();

        if(!liters || !bill || !km || km === "0") {
            alert("❌ لاحتساب معدل الاستهلاك بدقة، يرجى ملء (الكمية، رقم الفاتورة، وقراءة العداد في قطاع 2) أولاً!");
            return;
        }

        let msg = "%E2%9B%BD *تقرير مراقبة استهلاك وقود السيارات - منظومة 2600* %E2%9B%BD\\n\\n" +
                  "🚗 *السيارة لوحة:* " + base.plate + "\\n" +
                  "👤 *السائق/المستخدم:* " + base.driver + "\\n" +
                  "🧾 *رقم الفاتورة:* " + bill + "\\n" +
                  "💳 *طبيعة التعبئة:* " + payType + "\\n" +
                  "📍 *المحطة:* " + station + "\\n" +
                  "📥 *الكمية المعبأة:* " + liters + " لتر\\n" +
                  "🛣️ *قراءة العداد عند التعبئة:* " + km + " كم/ميل\\n" +
                  "📊 *حالة الحركة:* تم التوثيق وسيتم مطابقتها مركزياً بالعداد السابق لإخراج معدل الاستهلاك الفعلي.\\n\\n" +
                  "⏳ *توقيت التوثيق:* " + new Date().toLocaleString('ar-EG');
        openWhatsApp(msg);
    }

    function sendFault(faultMsg, cat) {
        let base = getBaseData();
        let msg = "🚨 *بلاغ عطل سيارة صالون طارئ - منظومة 2600* 🚨\\n\\n" +
                  "🚗 *رقم اللوحة:* " + base.plate + "\\n" +
                  "👤 *المستخدم/السائق:* " + base.driver + "\\n" +
                  "🗂️ *التصنيف الفني للسيارات:* " + cat + "\\n" +
                  "🛠️ *تفاصيل العطل:* " + faultMsg + "\\n\\n" +
                  "⏳ *توقيت البلاغ:* " + new Date().toLocaleString('ar-EG');
        openWhatsApp(msg);
    }

    function sendFreeFault() {
        let base = getBaseData();
        let txt = document.getElementById('manual_fault').value.trim();
        if(!txt) { alert("يرجى كتابة نص الملاحظة أولاً!"); return; }
        
        let msg = "🚨 *بلاغ ملاحظات وأعطال حرة (سيارة) - 2600* 🚨\\n\\n" +
                  "🚗 *السيارة لوحة:* " + base.plate + "\\n" +
                  "👤 *المستلم:* " + base.driver + "\\n" +
                  "📝 *تفاصيل البلاغ اليدوي:* " + txt + "\\n\\n" +
                  "⏳ *توقيت البلاغ:* " + new Date().toLocaleString('ar-EG');
        openWhatsApp(msg);
        document.getElementById('manual_fault').value = "";
    }
</script>
</body>
</html>"""
        with open("Fakher_Car_Driver_2600.html", "w", encoding="utf-8") as f:
            f.write(html_content)

    def build_control_ui(self):
        label_title = tk.Label(self.root, text="غرفة إدارة حركة السيطرة المركزية\nمنظومة فاخر السيادية 2600", font=("Arial", 14, "bold"), bg="#0f172a", fg="#38bdf8", justify="center")
        label_title.pack(pady=25)
        
        label_status = tk.Label(self.root, text="حالة النظام وتوليد الملفات السريعة:\n\n✅ تم تفعيل قاعدة بيانات السيارات بنجاح.\n✅ تم إنشاء ملف بوابة سائقي السيارات بنجاح\nتحت اسم: Fakher_Car_Driver_2600.html", font=("Arial", 12, "bold"), bg="#0f172a", fg="#10b981", justify="center")
        label_status.pack(pady=15)
        
        label_inf = tk.Label(self.root, text="المشرف العام: المهندس جمال سويد", font=("Arial", 11, "bold"), bg="#0f172a", fg="#ffffff")
        label_inf.pack(side="bottom", pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherCarDriverWhatsApp2600(root)
    root.mainloop()