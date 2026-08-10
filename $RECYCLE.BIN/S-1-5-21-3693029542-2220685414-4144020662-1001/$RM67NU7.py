# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - واجهة هاتف سائق السيارة الذكية وحساب استهلاك الوقود (الإصدار السيادي الشامل)
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد: Fakher_Car_Driver_WhatsApp_2600.py
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import webbrowser  
import urllib.parse  

DB_PATH = "Fakher_System_2026.db"

class FakherCarDriverWhatsApp2600:
    def __init__(self, root):
        self.root = root
        self.root.title("📱 منظومة فاخر 2600 - بوابة سائق السيارة ومراقبة الاستهلاك الفعلي 📱")
        self.root.geometry("1350x900")
        
        self.bg_dark = "#0f172a"
        self.bg_frame = "#1e293b"
        self.fg_white = "#ffffff"
        
        self.root.configure(bg=self.bg_dark)
        
        self.init_car_database()
        self.build_ui_layout()
        self.load_active_car_alerts()

    def init_car_database(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # جدول حركات العداد للسيارات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS car_odometer_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plate_num TEXT,
                    driver_name TEXT,
                    km_reading REAL,
                    date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # جدول وقود السيارات المطور مع رقم الفاتورة والنوع
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
            
            # جدول بلاغات أعطال السيارات
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
            
            # جدول التنبيهات المركزية للسيارات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Car_Central_Alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_text TEXT,
                    is_done INTEGER DEFAULT 0
                )
            """)
            
            cursor.execute("SELECT COUNT(*) FROM Car_Central_Alerts WHERE is_done = 0")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO Car_Central_Alerts (alert_text, is_done) VALUES ('تنبيه أمن وسلامة السيارات: فحص مستوى زيت المحرك والماء الاحتياطي قبل تشغيل السيارة صباحاً.', 0)")
                cursor.execute("INSERT INTO Car_Central_Alerts (alert_text, is_done) VALUES ('تذكير النظافة الدوري: يرجى تنظيف وتطهير مقصورة السيارة الصالون نهاية كل أسبوع.', 0)")
                
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Car Database Init Error: {e}")

    def build_ui_layout(self):
        header = tk.Frame(self.root, bg="#1e1b4b", pady=12)
        header.pack(fill="x", padx=15, pady=8)
        tk.Label(header, text="📱 بـوابـة سـائـق السـيـارات الـصـالـون والـفـرعـيـة 2600 📱", font=("Arial", 16, "bold"), bg="#1e1b4b", fg="#38bdf8", anchor="center").pack(fill="x")

        # [القطاع الأول]: قطاع هوية السيارة الثابتة
        identity_frame = tk.LabelFrame(self.root, text=" 👤 [ 1. هوية السيارة والسائق الثابتة ] ", font=("Arial", 11, "bold"), bg=self.bg_frame, fg="#38bdf8", labelanchor="ne")
        identity_frame.pack(fill="x", padx=15, pady=5)
        
        self.txt_driver_name = tk.Entry(identity_frame, font=("Arial", 13, "bold"), width=25, justify="center")
        self.txt_driver_name.pack(side="right", padx=15, pady=8)
        self.txt_driver_name.insert(0, "محمد علي الناشري")
        tk.Label(identity_frame, text="اسم المستخدم/السائق:", font=("Arial", 12, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right", padx=2)

        self.txt_plate = tk.Entry(identity_frame, font=("Arial", 13, "bold"), width=15, justify="center")
        self.txt_plate.pack(side="right", padx=15, pady=8)
        self.txt_plate.insert(0, "أ ب 200")
        tk.Label(identity_frame, text="رقم اللوحة المعدنية:", font=("Arial", 12, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right", padx=2)

        self.txt_whatsapp = tk.Entry(identity_frame, font=("Arial", 13, "bold"), width=15, justify="center")
        self.txt_whatsapp.pack(side="left", padx=15, pady=8)
        tk.Label(identity_frame, text="رقم الواتساب المستلم:", font=("Arial", 12, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="left", padx=2)

        # [القطاع الثاني]: قطاع قراءات العداد الحركية اليومية
        odometer_frame = tk.LabelFrame(self.root, text=" 📟 [ 2. قطاع قراءات العداد الحركية اليومية للسيارة ] ", font=("Arial", 11, "bold"), bg=self.bg_frame, fg="#f43f5e", labelanchor="ne")
        odometer_frame.pack(fill="x", padx=15, pady=5)

        btn_send_km = tk.Button(odometer_frame, text="🚀 إرسال قراءة العداد الحالية فقط", font=("Arial", 11, "bold"), bg="#e11d48", fg="white", padx=15, command=self.send_only_car_odometer)
        btn_send_km.pack(side="left", padx=15, pady=8)

        self.txt_current_km = tk.Entry(odometer_frame, font=("Arial", 13, "bold"), width=20, justify="center", bg="#334155", fg="white", insertbackground="white")
        self.txt_current_km.pack(side="right", padx=15, pady=8)
        self.txt_current_km.insert(0, "0")
        tk.Label(odometer_frame, text="قراءة العداد الحالية (كم / ميل):", font=("Arial", 12, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right", padx=5)

        # [القطاع الثالث]: قطاع تزويد وقود السيارة المطور والخوارزمية الذكية
        fuel_frame = tk.LabelFrame(self.root, text=" ⛽ [ 3. قطاع مراقبة تزويد وقود السيارة واحتساب معدل الاستهلاك الفعلي ] ", font=("Arial", 11, "bold"), bg=self.bg_frame, fg="#eab308", labelanchor="ne")
        fuel_frame.pack(fill="x", padx=15, pady=5)

        btn_send_fuel = tk.Button(fuel_frame, text="⛽ إرسال وقود السيارة وحساب الاستهلاك", font=("Arial", 11, "bold"), bg="#ca8a04", fg="black", padx=15, command=self.send_car_fuel_and_calculate_consumption)
        btn_send_fuel.pack(side="left", padx=15, pady=8)

        self.txt_fuel_station = tk.Entry(fuel_frame, font=("Arial", 12, "bold"), width=15, justify="center", bg="#334155", fg="white")
        self.txt_fuel_station.pack(side="right", padx=10, pady=8)
        tk.Label(fuel_frame, text="المحطة:", font=("Arial", 11, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right")

        self.combo_payment_type = ttk.Combobox(fuel_frame, values=["اتفاق شركة (بالآجل)", "كاش (مسترد عند الوصول)"], font=("Arial", 11, "bold"), state="readonly", width=22, justify="center")
        self.combo_payment_type.pack(side="right", padx=10, pady=8)
        self.combo_payment_type.set("اتفاق شركة (بالآجل)")
        tk.Label(fuel_frame, text="نوع التعبئة:", font=("Arial", 11, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right")

        self.txt_bill_number = tk.Entry(fuel_frame, font=("Arial", 12, "bold"), width=12, justify="center", bg="#334155", fg="white")
        self.txt_bill_number.pack(side="right", padx=10, pady=8)
        tk.Label(fuel_frame, text="رقم الفاتورة:", font=("Arial", 11, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right")

        self.txt_fuel_liters = tk.Entry(fuel_frame, font=("Arial", 12, "bold"), width=10, justify="center", bg="#334155", fg="white")
        self.txt_fuel_liters.pack(side="right", padx=10, pady=8)
        tk.Label(fuel_frame, text="الكمية (لتر):", font=("Arial", 11, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right")

        # [القطاع الرابع]: تصنيفات الأعطال المركزية للسيارات بالأسفل
        self.fault_frame = tk.LabelFrame(self.root, text=" 🛠️ [ قائمة تسجيل أعطال السيارة المعتمدة ] ", font=("Arial", 13, "bold"), bg=self.bg_dark, fg="#38bdf8", labelanchor="ne", padx=15, pady=5)
        self.fault_frame.pack(fill="both", expand=True, padx=15, pady=5)

        nav_bar = tk.Frame(self.fault_frame, bg=self.bg_frame, pady=6)
        nav_bar.pack(fill="x", pady=5)

        tk.Button(nav_bar, text="⚙️ أعطال ميكانيكية", font=("Arial", 12, "bold"), bg="#b91c1c", fg="white", padx=12, command=lambda: self.switch_car_fault_view("mechanical")).pack(side="right", padx=8)
        tk.Button(nav_bar, text="⚡ أعطال كهربائية", font=("Arial", 12, "bold"), bg="#eab308", fg="black", padx=12, command=lambda: self.switch_car_fault_view("electrical")).pack(side="right", padx=8)
        tk.Button(nav_bar, text="🛑 أعطال البريك", font=("Arial", 12, "bold"), bg="#2563eb", fg="white", padx=12, command=lambda: self.switch_car_fault_view("brakes")).pack(side="right", padx=8)
        tk.Button(nav_bar, text="🎙️ ملاحظات وأعطال حرة", font=("Arial", 12, "bold"), bg="#7c3aed", fg="white", padx=12, command=lambda: self.switch_car_fault_view("unregistered")).pack(side="right", padx=8)

        self.view_container = tk.Frame(self.fault_frame, bg=self.bg_dark, pady=5)
        self.view_container.pack(fill="both", expand=True, pady=5)
        
        self.alerts_frame = tk.LabelFrame(self.root, text=" 🔔 [ صندوق التنبيهات وإشعارات صيانة وأمن السيارات ] ", font=("Arial", 13, "bold"), bg=self.bg_dark, fg="#f43f5e", labelanchor="ne", padx=15, pady=5)
        self.alerts_frame.pack(fill="x", padx=15, pady=10)

        self.alerts_container = tk.Frame(self.alerts_frame, bg=self.bg_dark)
        self.alerts_container.pack(fill="x", expand=True)

        self.switch_car_fault_view("mechanical")

    def switch_car_fault_view(self, category):
        for widget in self.view_container.winfo_children():
            widget.destroy()

        data = {
            "mechanical": ["حرارة المحرك مرتفعة", "صوت غريب أسفل السيارة", "نقص مستمر في زيت المحرك", "تهريب ماء الرديتر", "تفتفة وتقطيع أثناء المشي", "ضعف في سحب وعزم السيارة", "صوت في ناقل الحركة (الغير)"],
            "electrical": ["البطارية ضعيفة والسيارة لا تعمل صباحاً", "مكيف السيارة لا يبرد", "الانارة الأمامية عاطلة", "الانارة الخلفية وإشارات الانعطاف عاطلة", "مشكلة في لوحة العدادات والتابلوه", "بيت شاحن الولاعة عاطل", "الزجاج الكهربائي لا يعمل"],
            "brakes": ["صوت صفير عند الضغط على البريك", "البريك ضعيف ويحتاج مسافة طويلة وقف", "رعشة في المقود عند الضغط على البريك", "نقص في زيت الفرامل (الباكم)", "فرامل اليد (الهاند بريك) لا تعمل"]
        }

        if category in data:
            self.view_container.columnconfigure(0, weight=1)
            self.view_container.columnconfigure(1, weight=3)

            for idx, fault_text in enumerate(data[category]):
                lbl = tk.Label(self.view_container, text=f"• {fault_text}", font=("Arial", 13, "bold"), bg=self.bg_dark, fg="#f1f5f9", anchor="e")
                lbl.grid(row=idx, column=1, sticky="e", padx=20, pady=5)

                btn_send = tk.Button(self.view_container, text="✉️ إرسال بلاغ العطل للواتساب", font=("Arial", 11, "bold"), bg="#16a34a", fg="white", padx=12,
                                     command=lambda f=fault_text, c=category: self.send_car_fault_only_payload(f, c))
                btn_send.grid(row=idx, column=0, sticky="w", padx=20, pady=5)

        elif category == "unregistered":
            unreg_frame = tk.Frame(self.view_container, bg=self.bg_frame, padx=15, pady=10)
            unreg_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(unreg_frame, text="✍️ ادخل أي ملاحظات حرة أو أعطال غير مسجلة خاصة بالسيارة:", font=("Arial", 12, "bold"), bg=self.bg_frame, fg="#cbd5e1", anchor="e").pack(fill="x", pady=4)
            self.txt_manual_fault = tk.Text(unreg_frame, height=3, font=("Arial", 12, "bold"), bg=self.bg_dark, fg="white", insertbackground="white")
            self.txt_manual_fault.pack(fill="x", pady=4)

            tk.Button(unreg_frame, text="🚀 إرسال البلاغ الحر للسيارة عبر الواتساب وتوثيقه", font=("Arial", 12, "bold"), bg="#7c3aed", fg="white", pady=5,
                      command=self.send_car_unregistered_fault_payload).pack(pady=10)

    def send_only_car_odometer(self):
        driver = self.txt_driver_name.get().strip()
        plate = self.txt_plate.get().strip()
        phone = self.txt_whatsapp.get().strip()
        current_km = self.txt_current_km.get().strip()

        if not phone or not current_km or current_km == "0":
            messagebox.showwarning("بيانات ناقصة", "❌ يرجى إدخال رقم الواتساب وقراءة العداد الصحيحة!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO car_odometer_logs (plate_num, driver_name, km_reading)
                VALUES (?, ?, ?)
            """, (plate, driver, float(current_km)))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Car Odometer Save Error: {e}")

        msg = (
            f"📟 *تقرير عداد الحركة اليومي (سيارة صالون) - 2600* 📟\n\n"
            f"🚗 *رقم اللوحة المعدنية:* {plate}\n"
            f"👤 *المستلم/السائق:* {driver}\n"
            f"🛣️ *قراءة العداد الحالية:* {current_km} كم/ميل\n\n"
            f"⏳ *التوقيت:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.fire_whatsapp_gateway(phone, msg)

    def send_car_fuel_and_calculate_consumption(self):
        driver = self.txt_driver_name.get().strip()
        plate = self.txt_plate.get().strip()
        phone = self.txt_whatsapp.get().strip()
        liters_str = self.txt_fuel_liters.get().strip()
        bill_num = self.txt_bill_number.get().strip()
        pay_type = self.combo_payment_type.get()
        station = self.txt_fuel_station.get().strip()
        current_km_str = self.txt_current_km.get().strip()

        if not phone or not liters_str or not bill_num or current_km_str == "0":
            messagebox.showwarning("بيانات ناقصة", "❌ لاحتساب معدل استهلاك الوقود بدقة، يرجى ملء (الكمية، رقم الفاتورة، وقراءة العداد الحالية في القطاع رقم 2) أولاً!")
            return

        try:
            current_km = float(current_km_str)
            liters = float(liters_str)
        except ValueError:
            messagebox.showerror("خطأ في البيانات", "❌ العداد وكمية اللترات يجب أن تكون أرقاماً!")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT km_reading FROM car_odometer_logs 
            WHERE plate_num = ? 
            ORDER BY date_recorded DESC LIMIT 1
        """, (plate,))
        
        row = cursor.fetchone()
        
        if not row:
            distance_traveled = 0
            consumption_rate = 0
            is_high_consumption = False
        else:
            previous_km = float(row[0])
            distance_traveled = current_km - previous_km
            
            if distance_traveled < 0:
                conn.close()
                messagebox.showerror("خطأ في العداد", "⚠️ تنبيه سيادي: قراءة العداد الحالية أقل من القراءة السابقة المخزنة!")
                return
            
            if distance_traveled > 0:
                consumption_rate = round(distance_traveled / liters, 2)
            else:
                consumption_rate = 0

            is_high_consumption = True if (0 < consumption_rate < 8.0) else False

        cursor.execute("""
            INSERT INTO car_fuel_logs (plate_num, driver_name, liters, bill_number, payment_type, station_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (plate, driver, liters, bill_num, pay_type, station if station else "غير محددة"))
        
        cursor.execute("""
            INSERT INTO car_odometer_logs (plate_num, driver_name, km_reading)
            VALUES (?, ?, ?)
        """, (plate, driver, current_km))
        
        conn.commit()
        conn.close()

        msg = (
            f"⛽ *تقرير مراقبة استهلاك وقود السيارات - منظومة 2600* ⛽\n\n"
            f"🚗 *السيارة لوحة:* {plate}\n"
            f"👤 *السائق/المستخدم:* {driver}\n"
            f"🧾 *رقم الفاتورة:* {bill_num}\n"
            f"💳 *طبيعة التعبئة:* {pay_type}\n"
            f"📍 *المحطة:* {station if station else 'غير محددة'}\n"
            f"📥 *الكمية المعبأة:* {liters} لتر\n"
            f"🛣 *المسافة المقطوعة بالحركة:* {distance_traveled} كم\n"
            f"📊 *معدل الاستهلاك الفعلي:* {consumption_rate} كم/لتر\n"
        )

        if distance_traveled == 0:
            msg += "📝 *حالة الحركة:* تعبئة تأسيسية أولى (سيتم حساب الاستهلاك المقارن بدءاً من الحركة القادمة).\n"
        elif is_high_consumption:
            msg += "🚨 *تنبيه الرقابة:* استهلاك مرتفع جداً وغير طبيعي للوقود! يرجى الفحص الفني للسيارة.\n"
        else:
            msg += "✅ *حالة الحركة:* معدل استهلاك الوقود طبيعي وفي النطاق الآمن للسيارات.\n"

        if "كاش" in pay_type:
            msg += "⚠️ *ملاحظة مالية:* الفاتورة مدفوعة نقداً بالخطوط ومستردة للسائق."
        else:
            msg += "💼 *ملاحظة مالية:* تعبئة بالآجل على حساب الشركة المتفق عليه مسبقاً."

        msg += f"\n\n⏳ *توقيت التوثيق المركزي:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        self.fire_whatsapp_gateway(phone, msg)
        
        self.txt_fuel_liters.delete(0, tk.END)
        self.txt_bill_number.delete(0, tk.END)
        self.txt_fuel_station.delete(0, tk.END)

    def send_car_fault_only_payload(self, fault_msg, category):
        driver = self.txt_driver_name.get().strip()
        plate = self.txt_plate.get().strip()
        phone = self.txt_whatsapp.get().strip()

        if not phone:
            messagebox.showwarning("رقم مفقود", "يرجى كتابة رقم هاتف الواتساب أولاً!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Car_Fault_Logs (plate_num, driver_name, fault_category, fault_detail, log_date)
                VALUES (?, ?, ?, ?, ?)
            """, (plate, driver, category, fault_msg, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Car Fault Save Error: {e}")

        msg = (
            f"🚨 *بلاغ عطل سيارة طارئ - منظومة 2600* 🚨\n\n"
            f"🚗 *رقم اللوحة:* {plate}\n"
            f"👤 *المستخدم/السائق:* {driver}\n"
            f"🗂️ *التصنيف الفني للسيارات:* {category}\n"
            f"🛠️ *تفاصيل العطل:* {fault_msg}\n\n"
            f"⏳ *توقيت البلاغ الفني:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.fire_whatsapp_gateway(phone, msg)

    def send_car_unregistered_fault_payload(self):
        manual_txt = self.txt_manual_fault.get("1.0", tk.END).strip()
        driver = self.txt_driver_name.get().strip()
        plate = self.txt_plate.get().strip()
        phone = self.txt_whatsapp.get().strip()

        if not phone or not manual_txt: 
            messagebox.showwarning("بيانات ناقصة", "يرجى كتابة رقم الهاتف ونص الملاحظة للسيارة أولاً!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Car_Fault_Logs (plate_num, driver_name, fault_category, fault_detail, log_date)
                VALUES (?, ?, ?, ?, ?)
            """, (plate, driver, "unregistered", manual_txt, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Car Manual Save Error: {e}")

        msg = (
            f"🚨 *بلاغ ملاحظات وأعطال حرة (سيارة) - 2600* 🚨\n\n"
            f"🚗 *السيارة لوحة:* {plate}\n"
            f"👤 *المستلم:* {driver}\n"
            f"📝 *تفاصيل البلاغ اليدوي:* {manual_txt}\n\n"
            f"⏳ *توقيت البلاغ:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.fire_whatsapp_gateway(phone, msg)
        self.txt_manual_fault.delete("1.0", tk.END)

    def fire_whatsapp_gateway(self, phone, message_body):
        encoded_msg = urllib.parse.quote(message_body)
        webbrowser.open(f"https://api.whatsapp.com/send?phone={phone}&text={encoded_msg}")

    def load_active_car_alerts(self):
        for widget in self.alerts_container.winfo_children():
            widget.destroy()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, alert_text FROM Car_Central_Alerts WHERE is_done = 0")
            rows = cursor.fetchall()
            conn.close()
        except:
            rows = []

        self.alerts_container.columnconfigure(0, weight=1)
        self.alerts_container.columnconfigure(1, weight=4)

        if not rows:
            lbl_empty = tk.Label(self.alerts_container, text="✅ جميع التنبيهات والأعمال للسيارات منفذة ومعمدة.", font=("Arial", 12, "bold"), bg=self.bg_dark, fg="#10b981", anchor="e")
            lbl_empty.pack(pady=8, fill="x", padx=20)
            return

        for idx, (alert_id, text_msg) in enumerate(rows):
            lbl_msg = tk.Label(self.alerts_container, text=f"🔔 {text_msg}", font=("Arial", 12, "bold"), bg=self.bg_dark, fg="#fecdd3", anchor="e", justify="right")
            lbl_msg.grid(row=idx, column=1, sticky="e", padx=15, pady=6)

            btn_confirm = tk.Button(self.alerts_container, text="✅ تم تنفيذ المطلوب للسيارة", font=("Arial", 11, "bold"), bg="#0269a1", fg="white", padx=10,
                                    command=lambda aid=alert_id: self.mark_car_alert_done_confirm(aid))
            btn_confirm.grid(row=idx, column=0, sticky="w", padx=15, pady=6)

    def mark_car_alert_done_confirm(self, alert_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("UPDATE Car_Central_Alerts SET is_done = 1 WHERE id = ?", (alert_id,))
            conn.commit()
            conn.close()
        except:
            pass

        messagebox.showinfo("تأكيد سيادي", "🚀 تم تسجيل إنجاز العمل الخاص بالسيارة بنجاح.")
        self.load_active_car_alerts()

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherCarDriverWhatsApp2600(root)
    root.mainloop()