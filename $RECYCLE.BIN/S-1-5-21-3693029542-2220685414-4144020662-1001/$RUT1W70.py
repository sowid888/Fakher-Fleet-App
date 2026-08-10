# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - واجهة هاتف سائق الشاحنة الذكية للواتساب (الإصدار السيادي المطور كلياً)
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد: Fakher_Driver_WhatsApp_2600.py

التطوير الإستراتيجي الشامل:
1. ثبات هوية السائق ورقم اللوحة (تُدخل مرة واحدة وتظل ثابتة لمنع ضياع الوقت).
2. تقسيم شريط البيانات العلوي إلى 3 قطاعات مستقلة تماماً بـ 3 مفاتيح إرسال منفصلة.
3. مراعاة آلية تعبئة الوقود (محطات متفق معها بالآجل / أو كاش بالخطوط الطويلة والمحافظات مسترد عند الوصول).
4. الإبقاء على قائمة الأعطال والإنذارات بالأسفل كما هي دون أي مسح.
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

class FakherDriverWhatsApp2600:
    def __init__(self, root):
        self.root = root
        self.root.title("📱 منظومة فاخر 2600 - بوابة السائق الذكية ومراقبة الوقود والعداد 📱")
        self.root.geometry("1350x900")
        
        self.bg_dark = "#0f172a"
        self.bg_frame = "#1e293b"
        self.fg_white = "#ffffff"
        
        self.root.configure(bg=self.bg_dark)
        
        self.init_driver_database()
        self.build_ui_layout()
        self.load_active_alerts()

    def init_driver_database(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # جدول حركات العداد الحركية المستقلة
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS truck_odometer_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plate_num TEXT,
                    driver_name TEXT,
                    km_reading REAL,
                    date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # جدول وقود الديزل المطور لحساب التكلفة والنوع (كاش مسترد / اتفاق شركة بالآجل)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS truck_diesel (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    truck_id TEXT,
                    driver_name TEXT,
                    liters REAL,
                    bill_number TEXT,
                    payment_type TEXT,
                    station_name TEXT,
                    date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # جدول بلاغات الأعطال
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Driver_Fault_Logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plate_num TEXT,
                    driver_name TEXT,
                    fault_category TEXT,
                    fault_detail TEXT,
                    log_date TEXT
                )
            """)
            
            # جدول التنبيهات المركزية للإدارة
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Driver_Central_Alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_text TEXT,
                    is_done INTEGER DEFAULT 0
                )
            """)
            
            # إدخال تنبيهات الأمن والسلامة الافتراضية إذا كان الجدول فارغاً
            cursor.execute("SELECT COUNT(*) FROM Driver_Central_Alerts WHERE is_done = 0")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO Driver_Central_Alerts (alert_text, is_done) VALUES ('تذكير أمن وسلامة الشاحنات: يرجى فحص وزن الإطارات الشامل وضغط الهواء كل يومين.', 0)")
                cursor.execute("INSERT INTO Driver_Central_Alerts (alert_text, is_done) VALUES ('تنبيه الصيانة الدوري: موعد غسيل وتنظيف صندوق الشاحنة نهاية الأسبوع (يوم مهلة للموزع).', 0)")
                
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database Init Error: {e}")

    def build_ui_layout(self):
        # 1. شريط الترويسة العلوي الملكي
        header = tk.Frame(self.root, bg="#1e1b4b", pady=12)
        header.pack(fill="x", padx=15, pady=8)
        tk.Label(header, text="📱 بـوابـة سـائـق الشـاحـنـة الـرقـمـيـة المـوحـدة 2600 📱", font=("Arial", 16, "bold"), bg="#1e1b4b", fg="#10b981", anchor="center").pack(fill="x")

        # -------------------------------------------------------------------------
        # [القطاع الأول]: قطاع هوية الشاحنة الثابتة (تُدخل مرة واحدة وتظل مستقرة)
        # -------------------------------------------------------------------------
        identity_frame = tk.LabelFrame(self.root, text=" 👤 [ 1. هوية الشاحنة والسائق الثابتة ] ", font=("Arial", 11, "bold"), bg=self.bg_frame, fg="#38bdf8", labelanchor="ne")
        identity_frame.pack(fill="x", padx=15, pady=5)
        
        # حقل اسم السائق
        self.txt_driver_name = tk.Entry(identity_frame, font=("Arial", 13, "bold"), width=25, justify="center")
        self.txt_driver_name.pack(side="right", padx=15, pady=8)
        self.txt_driver_name.insert(0, "عبده محمد الجوزي")
        tk.Label(identity_frame, text="اسم السائق:", font=("Arial", 12, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right", padx=2)

        # حقل رقم اللوحة المعدنية للشاحنة
        self.txt_plate = tk.Entry(identity_frame, font=("Arial", 13, "bold"), width=15, justify="center")
        self.txt_plate.pack(side="right", padx=15, pady=8)
        self.txt_plate.insert(0, "ط ص 100")
        tk.Label(identity_frame, text="رقم اللوحة المعدنية:", font=("Arial", 12, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right", padx=2)

        # حقل رقم الواتساب المستلم
        self.txt_whatsapp = tk.Entry(identity_frame, font=("Arial", 13, "bold"), width=15, justify="center")
        self.txt_whatsapp.pack(side="left", padx=15, pady=8)
        tk.Label(identity_frame, text="رقم الواتساب المستلم:", font=("Arial", 12, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="left", padx=2)

        # -------------------------------------------------------------------------
        # [القطاع الثاني]: قطاع قراءات العداد الحركية + مفتاح إرسال مستقل
        # -------------------------------------------------------------------------
        odometer_frame = tk.LabelFrame(self.root, text=" 📟 [ 2. قطاع قراءات العداد الحركية اليومية ] ", font=("Arial", 11, "bold"), bg=self.bg_frame, fg="#f43f5e", labelanchor="ne")
        odometer_frame.pack(fill="x", padx=15, pady=5)

        # مفتاح إرسال العداد المستقل جهة اليسار
        btn_send_km = tk.Button(odometer_frame, text="🚀 إرسال قراءة العداد الحالية فقط", font=("Arial", 11, "bold"), bg="#e11d48", fg="white", padx=15, command=self.send_only_odometer)
        btn_send_km.pack(side="left", padx=15, pady=8)

        # حقل قراءة العداد
        self.txt_current_km = tk.Entry(odometer_frame, font=("Arial", 13, "bold"), width=20, justify="center", bg="#334155", fg="white", insertbackground="white")
        self.txt_current_km.pack(side="right", padx=15, pady=8)
        self.txt_current_km.insert(0, "0")
        tk.Label(odometer_frame, text="قراءة العداد الحالية (كم / ميل):", font=("Arial", 12, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right", padx=5)

        # -------------------------------------------------------------------------
        # [القطاع الثالث]: قطاع تعبئة وقود الديزل المطور (مراعاة الكاش والآجل) + مفتاح إرسال مستقل
        # -------------------------------------------------------------------------
        fuel_frame = tk.LabelFrame(self.root, text=" ⛽ [ 3. قطاع مراقبة وقود الديزل ومنع الهدر وحساب السندات ] ", font=("Arial", 11, "bold"), bg=self.bg_frame, fg="#eab308", labelanchor="ne")
        fuel_frame.pack(fill="x", padx=15, pady=5)

        # مفتاح إرسال وقود الديزل المستقل جهة اليسار
        btn_send_fuel = tk.Button(fuel_frame, text="⛽ إرسال بيانات وقود الديزل فقط", font=("Arial", 11, "bold"), bg="#ca8a04", fg="black", padx=15, command=self.send_only_fuel)
        btn_send_fuel.pack(side="left", padx=15, pady=8)

        # حقل اسم المحطة / الموقع
        self.txt_fuel_station = tk.Entry(fuel_frame, font=("Arial", 12, "bold"), width=15, justify="center", bg="#334155", fg="white")
        self.txt_fuel_station.pack(side="right", padx=10, pady=8)
        tk.Label(fuel_frame, text="المحطة:", font=("Arial", 11, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right")

        # قائمة منسدلة لنوع التعبئة (اتفاق شركة بالآجل / كاش بالخطوط الطويلة مسترد)
        self.combo_payment_type = ttk.Combobox(fuel_frame, values=["اتفاق شركة (بالآجل)", "كاش (مسترد عند الوصول)"], font=("Arial", 11, "bold"), state="readonly", width=22, justify="center")
        self.combo_payment_type.pack(side="right", padx=10, pady=8)
        self.combo_payment_type.set("اتفاق شركة (بالآجل)")
        tk.Label(fuel_frame, text="نوع التعبئة:", font=("Arial", 11, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right")

        # حقل رقم الفاتورة / السند المالي
        self.txt_bill_number = tk.Entry(fuel_frame, font=("Arial", 12, "bold"), width=12, justify="center", bg="#334155", fg="white")
        self.txt_bill_number.pack(side="right", padx=10, pady=8)
        tk.Label(fuel_frame, text="رقم الفاتورة:", font=("Arial", 11, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right")

        # حقل كمية الديزل باللتر
        self.txt_fuel_liters = tk.Entry(fuel_frame, font=("Arial", 12, "bold"), width=10, justify="center", bg="#334155", fg="white")
        self.txt_fuel_liters.pack(side="right", padx=10, pady=8)
        tk.Label(fuel_frame, text="الكمية (لتر):", font=("Arial", 11, "bold"), bg=self.bg_frame, fg=self.fg_white).pack(side="right")

        # -------------------------------------------------------------------------
        # [القطاع الرابع]: حاوية تصنيفات الأعطال المركزية والأعمال المطلوبة بالأسفل كما هي
        # -------------------------------------------------------------------------
        self.fault_frame = tk.LabelFrame(self.root, text=" 🛠️ [ قائمة تسجيل أعطال الشاحنة المعتمدة ] ", font=("Arial", 13, "bold"), bg=self.bg_dark, fg="#38bdf8", labelanchor="ne", padx=15, pady=5)
        self.fault_frame.pack(fill="both", expand=True, padx=15, pady=5)

        nav_bar = tk.Frame(self.fault_frame, bg=self.bg_frame, pady=6)
        nav_bar.pack(fill="x", pady=5)

        # أزرار التنقل بين تصنيفات الأعطال الأصلية
        tk.Button(nav_bar, text="⚙️ أعطال ميكانيكية", font=("Arial", 12, "bold"), bg="#b91c1c", fg="white", padx=12, command=lambda: self.switch_fault_view("mechanical")).pack(side="right", padx=8)
        tk.Button(nav_bar, text="⚡ أعطال كهربائية", font=("Arial", 12, "bold"), bg="#eab308", fg="black", padx=12, command=lambda: self.switch_fault_view("electrical")).pack(side="right", padx=8)
        tk.Button(nav_bar, text="🛑 أعطال البريك", font=("Arial", 12, "bold"), bg="#2563eb", fg="white", padx=12, command=lambda: self.switch_fault_view("brakes")).pack(side="right", padx=8)
        tk.Button(nav_bar, text="❄️ أعطال الثلاجة", font=("Arial", 12, "bold"), bg="#0d9488", fg="white", padx=12, command=lambda: self.switch_fault_view("fridge")).pack(side="right", padx=8)
        tk.Button(nav_bar, text="🎙️ أعطال غير مسجلة", font=("Arial", 12, "bold"), bg="#7c3aed", fg="white", padx=12, command=lambda: self.switch_fault_view("unregistered")).pack(side="right", padx=8)

        # حاوية عرض أسطر الأعطال الفورية والمتحركة
        self.view_container = tk.Frame(self.fault_frame, bg=self.bg_dark, pady=5)
        self.view_container.pack(fill="both", expand=True, pady=5)
        
        # صندوق التنبيهات المركزي للأمن والسلامة في الأسفل
        self.alerts_frame = tk.LabelFrame(self.root, text=" 🔔 [ صندوق التنبيهات المركزي وإشعارات أمن الشاحنات ] ", font=("Arial", 13, "bold"), bg=self.bg_dark, fg="#f43f5e", labelanchor="ne", padx=15, pady=5)
        self.alerts_frame.pack(fill="x", padx=15, pady=10)

        self.alerts_container = tk.Frame(self.alerts_frame, bg=self.bg_dark)
        self.alerts_container.pack(fill="x", expand=True)

        # العرض الأولي لأعطال الميكانيك
        self.switch_fault_view("mechanical")

    def switch_fault_view(self, category):
        for widget in self.view_container.winfo_children():
            widget.destroy()

        data = {
            "mechanical": ["لايوجد عزم", "استهلاك مرتفع للديزل", "تاخير في التشغيل", "صوت في المحرك غريب", "ارتفاع حراره المحرك", "تهريب ماء من التانكي", "تهريب زيت من الاقزوز", "تهريب زيت من تحت المحرك", "تهريب ديزل من تحت المحرك", "تهريب زيت السكان الدركسون"],
            "electrical": ["الشاحنه لا تعمل بسبب البطاريات ضعيفه تمامنا", "الشاحنه احيانا البطاريات ضعيفه اذا كنت في الصباح فقط", "نور الامامي جهة السائق معطل", "نور الامامي جهة الراكب معطل", "نور الاسطبات الخلفية جهة السائق معطله", "نور الاسطبات الخلفية جهة الراكب معطل", "نور إشارة الانعطاف خلف السائق معطله", "نور إشارة الانعطاف خلف الراكب معطله", "بيت شاحن الجوال معطل", "انارة الثلاجة الداخلية معطله", "الهون كلاكس طريقة معطل"],
            "brakes": ["البريك يصطر صوت", "البريك ضعيف", "تهريب سم بريك داخل الكبينه من علبه فوق", "تهريب سم بريك من قدام جهة الراكب او السائق", "تهريب سم بريك من الخلف من جهة الراكب او السائق", "تهريب زيت الدفريشن الجرويل"],
            "fridge": ["تهريب ماء من السقف", "تهريب ماء من الجوانب", "تهريب ماء من الباب الجانبي", "تهريب ماء من الابواب الخلفيه", "عند المطبات الثلاجه تصدر صوت", "تلفيه في عمود اقفال ابواب الثلاجه", "ثلاثيه في مفصلات ابواب الثلاجه", "تلفيه اقفال ابواب الثلاجه"]
        }

        if category in data:
            self.view_container.columnconfigure(0, weight=1)
            self.view_container.columnconfigure(1, weight=3)

            for idx, fault_text in enumerate(data[category]):
                lbl = tk.Label(self.view_container, text=f"• {fault_text}", font=("Arial", 13, "bold"), bg=self.bg_dark, fg="#f1f5f9", anchor="e")
                lbl.grid(row=idx, column=1, sticky="e", padx=20, pady=4)

                btn_send = tk.Button(self.view_container, text="✉️ إرسال بلاغ العطل للواتساب", font=("Arial", 11, "bold"), bg="#16a34a", fg="white", padx=12,
                                     command=lambda f=fault_text, c=category: self.send_fault_only_payload(f, c))
                btn_send.grid(row=idx, column=0, sticky="w", padx=20, pady=4)

        elif category == "unregistered":
            unreg_frame = tk.Frame(self.view_container, bg=self.bg_frame, padx=15, pady=10)
            unreg_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(unreg_frame, text="✍️ ادخل تفاصيل المشكلة الحرة هنا المكونة من ثلاثة أسطر:", font=("Arial", 12, "bold"), bg=self.bg_frame, fg="#cbd5e1", anchor="e").pack(fill="x", pady=4)
            self.txt_manual_fault = tk.Text(unreg_frame, height=3, font=("Arial", 12, "bold"), bg=self.bg_dark, fg="white", insertbackground="white")
            self.txt_manual_fault.pack(fill="x", pady=4)

            tk.Button(unreg_frame, text="🚀 إرسال البلاغ اليدوي عبر الواتساب وتوثيقه بالخزنة", font=("Arial", 12, "bold"), bg="#7c3aed", fg="white", pady=5,
                      command=self.send_unregistered_fault_payload).pack(pady=10)

    # 1. تنفيذ زر قراءة العداد المستقل والسيادي
    def send_only_odometer(self):
        driver = self.txt_driver_name.get().strip()
        plate = self.txt_plate.get().strip()
        phone = self.txt_whatsapp.get().strip()
        current_km = self.txt_current_km.get().strip()

        if not phone or not current_km or current_km == "0":
            messagebox.showwarning("بيانات غير مكتملة", "❌ يرجى كتابة رقم الواتساب وقراءة العداد الفعلية!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO truck_odometer_logs (plate_num, driver_name, km_reading)
                VALUES (?, ?, ?)
            """, (plate, driver, float(current_km)))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Odometer Save Error: {e}")

        # صياغة رسالة العداد الموجهة لغرفة العمليات
        msg = (
            f"📟 *تقرير قراءة العداد الحركي - منظومة 2600* 📟\n\n"
            f"🚚 *رقم اللوحة المعدنية:* {plate}\n"
            f"👤 *السائق الحركي:* {driver}\n"
            f"🛣️ *قراءة العداد الحالية:* {current_km} كم/ميل\n\n"
            f"⏳ *توقيت البلاغ الآمن:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.fire_whatsapp_gateway(phone, msg)

    # 2. تنفيذ زر وقود الديزل المستقل (معالجة فواتير المحطات بالآجل وكاش الخطوط الطويلة)
    def send_only_fuel(self):
        driver = self.txt_driver_name.get().strip()
        plate = self.txt_plate.get().strip()
        phone = self.txt_whatsapp.get().strip()
        liters = self.txt_fuel_liters.get().strip()
        bill_num = self.txt_bill_number.get().strip()
        pay_type = self.combo_payment_type.get()
        station = self.txt_fuel_station.get().strip()

        if not phone or not liters or not bill_num:
            messagebox.showwarning("بيانات الوقود مفقودة", "❌ يرجى إدخال رقم الواتساب، كمية اللترات، ورقم الفاتورة لتوثيق السند!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO truck_diesel (truck_id, driver_name, liters, bill_number, payment_type, station_name)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (plate, driver, float(liters), bill_num, pay_type, station if station else "غير محددة"))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Diesel Save Error: {e}")

        # بناء رسالة الوقود الذكية لغرفة الحسابات والموزع
        msg = (
            f"⛽ *بلاغ تعبئة وقود الديزل - منظومة فاخر 2600* ⛽\n\n"
            f"🚚 *الشاحنة لوحة:* {plate}\n"
            f"👤 *السائق:* {driver}\n"
            f"🧾 *رقم الفاتورة / السند:* {bill_num}\n"
            f"💳 *طبيعة ونوع التعبئة:* {pay_type}\n"
            f"▪️ *الكمية المعبأة:* {liters} لتر\n"
            f"📍 *المحطة / الموقع:* {station if station else 'غير محددة'}\n\n"
            f"⚠️ *ملاحظة:* "
        )
        if "كاش" in pay_type:
            msg += "هذه الفاتورة دُفعت كاش في الخطوط الطويلة/المحافظات وهي مستردة للمحاسبة فور الوصول."
        else:
            msg += "تعبئة بالآجل بموجب الفاتورة الرسمية المتفق عليها مسبقاً مع الشركة."

        msg += f"\n\n⏳ *توقيت التوثيق المالي:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        self.fire_whatsapp_gateway(phone, msg)
        
        # تصفير حقول الوقود فوراً لراحة السائق
        self.txt_fuel_liters.delete(0, tk.END)
        self.txt_bill_number.delete(0, tk.END)
        self.txt_fuel_station.delete(0, tk.END)

    # 3. إرسال الأعطال والمسجلة
    def send_fault_only_payload(self, fault_msg, category):
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
                INSERT INTO Driver_Fault_Logs (plate_num, driver_name, fault_category, fault_detail, log_date)
                VALUES (?, ?, ?, ?, ?)
            """, (plate, driver, category, fault_msg, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database Save Error: {e}")

        msg = (
            f"🚨 *بلاغ عطل شاحنة طارئ - منظومة 2600* 🚨\n\n"
            f"🚚 *رقم اللوحة:* {plate}\n"
            f"👤 *السائق:* {driver}\n"
            f"🗂️ *التصنيف الفني:* {category}\n"
            f"🛠️ *تفاصيل العطل المختار:* {fault_msg}\n\n"
            f"⏳ *توقيت البلاغ الفني:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.fire_whatsapp_gateway(phone, msg)

    # 4. إرسال بلاغات الأعطال غير المسجلة (اليدوية)
    def send_unregistered_fault_payload(self):
        manual_txt = self.txt_manual_fault.get("1.0", tk.END).strip()
        driver = self.txt_driver_name.get().strip()
        plate = self.txt_plate.get().strip()
        phone = self.txt_whatsapp.get().strip()

        if not phone or not manual_txt: 
            messagebox.showwarning("بيانات ناقصة", "يرجى كتابة رقم الهاتف ونص البلاغ اليدوي أولاً!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Driver_Fault_Logs (plate_num, driver_name, fault_category, fault_detail, log_date)
                VALUES (?, ?, ?, ?, ?)
            """, (plate, driver, "unregistered", manual_txt, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database Save Error: {e}")

        msg = (
            f"🚨 *بلاغ أعطال وملاحظات حرة - منظومة 2600* 🚨\n\n"
            f"🚚 *الشاحنة لوحة:* {plate}\n"
            f"👤 *السائق:* {driver}\n"
            f"📝 *تفاصيل البلاغ اليدوي:* {manual_txt}\n\n"
            f"⏳ *توقيت البلاغ:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.fire_whatsapp_gateway(phone, msg)
        self.txt_manual_fault.delete("1.0", tk.END)

    def fire_whatsapp_gateway(self, phone, message_body):
        """ بوابة الربط والفتح التلقائي للواتساب """
        encoded_msg = urllib.parse.quote(message_body)
        webbrowser.open(f"https://api.whatsapp.com/send?phone={phone}&text={encoded_msg}")

    def load_active_alerts(self):
        for widget in self.alerts_container.winfo_children():
            widget.destroy()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, alert_text FROM Driver_Central_Alerts WHERE is_done = 0")
            rows = cursor.fetchall()
            conn.close()
        except:
            rows = []

        self.alerts_container.columnconfigure(0, weight=1)
        self.alerts_container.columnconfigure(1, weight=4)

        if not rows:
            lbl_empty = tk.Label(self.alerts_container, text="✅ جميع الأعمال والتنبيهات معمدة ومنفذة.", font=("Arial", 12, "bold"), bg=self.bg_dark, fg="#10b981", anchor="e")
            lbl_empty.pack(pady=8, fill="x", padx=20)
            return

        for idx, (alert_id, text_msg) in enumerate(rows):
            lbl_msg = tk.Label(self.alerts_container, text=f"🔔 {text_msg}", font=("Arial", 12, "bold"), bg=self.bg_dark, fg="#fecdd3", anchor="e", justify="right")
            lbl_msg.grid(row=idx, column=1, sticky="e", padx=15, pady=6)

            btn_confirm = tk.Button(self.alerts_container, text="✅ تم تنفيذ المطلوب", font=("Arial", 11, "bold"), bg="#0269a1", fg="white", padx=10,
                                    command=lambda aid=alert_id: self.mark_alert_as_done_confirm(aid))
            btn_confirm.grid(row=idx, column=0, sticky="w", padx=15, pady=6)

    def mark_alert_as_done_confirm(self, alert_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("UPDATE Driver_Central_Alerts SET is_done = 1 WHERE id = ?", (alert_id,))
            conn.commit()
            conn.close()
        except:
            pass

        messagebox.showinfo("تأكيد سيادي", "🚀 تم تسجيل إنجاز التنبيه في المنظومة بنجاح.")
        self.load_active_alerts()

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherDriverWhatsApp2600(root)
    root.mainloop()