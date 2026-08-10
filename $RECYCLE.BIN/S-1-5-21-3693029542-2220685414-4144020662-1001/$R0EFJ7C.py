# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - وحدة السيارات الذكية (الإصدار الماسي المكتمل 100%)
المشرف العام وصاحب النظام: أنت يا غالي 👑
الإجراء: استعادة الكود الأصلي بكامل مفاتيحه مع إضافة حقل الرمز السري بجوار هوية التعريف.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
from datetime import datetime

# تثبيت المسارات المركزية والمحلية
DB_DIR = "C:/Fakher_System"
DB_PATH = os.path.join(DB_DIR, "Fakher_Central_Database_2600.db")

class CarGrandSystem2600:
    def __init__(self, root):
        self.root = root
        self.root.title("💎 منظومة فاخر 2600 - إدارة بيانات شاحنات وسيارات الصيانة الميدانية 💎")
        self.root.geometry("1550x920")
        self.root.state('zoomed')
        self.root.configure(bg="#0f172a") 
        
        self.fields = {}
        self.widgets_ordered = []
        
        self.init_database()
        self.build_original_ui()

    def init_database(self):
        """ تأسيس الخزنة المركزية بكافة الحقول والمفاتيح الأصلية دون أي نقصان """
        try:
            if not os.path.exists(DB_DIR):
                os.makedirs(DB_DIR, exist_ok=True)
                
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Car_Master (
                                admin_num TEXT PRIMARY KEY, 
                                plate_num TEXT, 
                                chassis_num TEXT,
                                car_model TEXT, 
                                manufacturer_en TEXT, 
                                car_class TEXT,
                                manufacturer_ar TEXT, 
                                car_class_ar TEXT, 
                                car_color TEXT, 
                                car_shape TEXT,
                                driver_job TEXT, 
                                driver_route TEXT, 
                                odometer_type TEXT,
                                driver_name TEXT, 
                                whatsapp_num TEXT, 
                                driver_password TEXT,
                                km_last_oil TEXT, 
                                km_last_oil_filter TEXT, 
                                km_last_air_filter TEXT,
                                km_last_plugs TEXT, 
                                km_last_gear_oil TEXT, 
                                km_last_coolant TEXT,
                                permit_start_year TEXT, 
                                permit_start_month TEXT, 
                                permit_start_day TEXT,
                                permit_end_year TEXT, 
                                permit_end_month TEXT, 
                                permit_end_day TEXT
                            )''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"تنبيه التأسيس: {e}")

    def build_original_ui(self):
        # 1. شريط التحكم العلوي الإستراتيجي للمستخدم الميداني
        top_bar = tk.Frame(self.root, bg="#1e293b", bd=1, relief="solid")
        top_bar.pack(fill="x", padx=15, pady=10)
        
        tk.Label(top_bar, text="🔍 ادخل الرقم الإداري لجلب البيانات:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").pack(side="right", padx=5, pady=15)
        self.search_entry = tk.Entry(top_bar, font=("Arial", 11), bg="#334155", fg="white", width=15)
        self.search_entry.pack(side="right", padx=5, pady=15)
        
        tk.Button(top_bar, text="⚙️ جلب بيانات السيارة", font=("Arial", 10, "bold"), bg="#38bdf8", fg="black", 
                  command=self.load_car_data_by_search, cursor="hand2").pack(side="right", padx=5, pady=10)

        tk.Button(top_bar, text="💾 ترحيل وحفظ البيانات الميدانية", font=("Arial", 12, "bold"), bg="#10b981", fg="white", 
                  command=self.save_car_data, width=28, cursor="hand2").pack(side="left", padx=10, pady=10)

        # 2. منطقة الحقول الرئيسية الموزعة
        main_frame = tk.Frame(self.root, bg="#0f172a")
        main_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # العمود الأيمن - حقول تعريف السيارة وفئاتها الإدارية (مع حقل الرمز السري الجديد المضاف إلى جوارها)
        right_panel = tk.LabelFrame(main_frame, text=" 🚗 أولاً: ملف هوية تعريف السيارة وفئاتها الإدارية ", font=("Arial", 13, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=5)
        
        self.add_smart_field(right_panel, "حقل الرقم الإداري للمركبة:", "admin_num", 0)
        self.add_smart_field(right_panel, "حقل رقم اللوحة المعدنية للشرطة:", "plate_num", 1)
        self.add_smart_field(right_panel, "رقم الشاصيه الفريد للسيارة:", "chassis_num", 2)
        
        # الحقل المطلوب بجوار هوية تعريف السيارة مباشرة
        self.add_smart_field(right_panel, "🔑 الرمز السري الخاص بالسائق:", "driver_password", 3)
        
        self.add_smart_field(right_panel, "حقل موديل السيارة / سنة الصنع:", "car_model", 4)
        self.add_smart_field(right_panel, "حقل الشركة المصنعة بالإنجليزية:", "manufacturer_en", 5)
        self.add_smart_field(right_panel, "حقل فئة السيارة الفني EN:", "car_class", 6)
        self.add_smart_field(right_panel, "حقل اسم الشركة المصنعة بالعربية:", "manufacturer_ar", 7)
        self.add_smart_field(right_panel, "حقل فئة السيارة باللغة العربية:", "car_class_ar", 8)
        self.add_smart_field(right_panel, "حقل لون السيارة الخارجي الثابت:", "car_color", 9)
        self.add_smart_field(right_panel, "حقل شكل السيارة (صالون، هيلوكس، إلخ):", "car_shape", 10)
        
        self.add_smart_combo(right_panel, "طبيعة عمل السائق والخيارات المنسدلة:", "driver_job", [
            "رئيس مجلس الادارة", "اعضاء مجلس الادارة", "مدير اداره", "نائب مدير", 
            "مندوب مبيعات جمله", "مندوب مبيعات تجزئه", "مندوب سوبرات", "مشرف ميداني", 
            "مسؤول خدمات", "سائق يتبع اعضاء مجلس الادارة", "سائق"
        ], 11)
        
        self.add_smart_combo(right_panel, "حقل خط سير السيارة (المحافظات اليمنية):", "driver_route", [
            "صنعاء", "عدن", "تعز", "الحديدة", "إب", "حضرموت", "ذمار", "عمران", 
            "صعدة", "حجة", "البيضاء", "مارب", "الجوف", "المهرة", "سقطرى", "أبين", "شبوة", "لحج"
        ], 12)
        
        self.add_smart_combo(right_panel, "حقل نوع العداد للمركبة (ميل / كم):", "odometer_type", ["كم (Kilometer)", "ميل (Mile)"], 13)

        # العمود الأيسر - حقول السائق والعدادات الفنية والتواريخ كاملة
        left_panel = tk.LabelFrame(main_frame, text=" 🔧 ثانياً: تحديث بيانات عدادات الصيانة الدورية الحالية ", font=("Arial", 13, "bold"), bg="#1e293b", fg="#a7f3d0", labelanchor="ne")
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        self.add_smart_field(left_panel, "حقل اسم السائق المعين بالكامل:", "driver_name", 0)
        self.add_smart_field(left_panel, "حقل رقم الواتساب المفعل للسائق (+):", "whatsapp_num", 1)
        
        self.add_smart_field(left_panel, "عداد الكيلومتر عند آخر تغيير زيت محرك:", "km_last_oil", 2)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير فلتر الزيت:", "km_last_oil_filter", 3)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير فلتر الهواء:", "km_last_air_filter", 4)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير البواجي (شمعات):", "km_last_plugs", 5)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير زيت الجيربوكس:", "km_last_gear_oil", 6)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير ماء الرديتر:", "km_last_coolant", 7)

        # صلاحية كرت تصريح السيارة الرسمي بكافة مفاتيحه وتفاصيله
        date_group = tk.LabelFrame(left_panel, text=" 📅 صلاحية كرت تصريح السيارة الرسمي ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#fbbf24")
        date_group.grid(row=8, column=0, columnspan=2, pady=15, padx=10, sticky="ew")

        # تاريخ البدء
        r1 = tk.Frame(date_group, bg="#1e293b")
        r1.pack(fill="x", pady=4, padx=15)
        tk.Label(r1, text="حقل تاريخ بدء وتجديد كرت السيارة الرسمي:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#cbd5e1", width=42, anchor="e").pack(side="right")
        
        self.fields["permit_start_year"] = ttk.Combobox(r1, values=[str(i) for i in range(2020, 2051)], width=8, font=("Arial", 10), state="readonly")
        self.fields["permit_start_year"].pack(side="left", padx=5)
        self.fields["permit_start_month"] = ttk.Combobox(r1, values=[str(i) for i in range(1, 13)], width=6, font=("Arial", 10), state="readonly")
        self.fields["permit_start_month"].pack(side="left", padx=5)
        self.fields["permit_start_day"] = ttk.Combobox(r1, values=[str(i) for i in range(1, 32)], width=6, font=("Arial", 10), state="readonly")
        self.fields["permit_start_day"].pack(side="left", padx=5)

        # تاريخ الانتهاء
        r2 = tk.Frame(date_group, bg="#1e293b")
        r2.pack(fill="x", pady=4, padx=15)
        tk.Label(r2, text="حقل تاريخ انتهاء تجديد الكرت الرسمي للسيارة:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#fca5a5", width=42, anchor="e").pack(side="right")
        
        self.fields["permit_end_year"] = ttk.Combobox(r2, values=[str(i) for i in range(2020, 2051)], width=8, font=("Arial", 10), state="readonly")
        self.fields["permit_end_year"].pack(side="left", padx=5)
        self.fields["permit_end_month"] = ttk.Combobox(r2, values=[str(i) for i in range(1, 13)], width=6, font=("Arial", 10), state="readonly")
        self.fields["permit_end_month"].pack(side="left", padx=5)
        self.fields["permit_end_day"] = ttk.Combobox(r2, values=[str(i) for i in range(1, 32)], width=6, font=("Arial", 10), state="readonly")
        self.fields["permit_end_day"].pack(side="left", padx=5)

        # تعيين التواريخ الافتراضية
        for k in ["permit_start_year", "permit_end_year"]: self.fields[k].set("2026")
        for k in ["permit_start_month", "permit_end_month", "permit_start_day", "permit_end_day"]: self.fields[k].set("1")

        self.setup_enter_navigation()

    def setup_enter_navigation(self):
        for idx, widget in enumerate(self.widgets_ordered):
            widget.bind("<Return>", lambda event, i=idx: self.focus_next_field(i))

    def focus_next_field(self, current_idx):
        if current_idx + 1 < len(self.widgets_ordered):
            next_w = self.widgets_ordered[current_idx + 1]
            next_w.focus_set()
            if isinstance(next_w, tk.Entry):
                next_w.selection_range(0, tk.END)
        return "break"

    def add_smart_field(self, parent, label_text, field_key, row_idx):
        tk.Label(parent, text=label_text, font=("Arial", 11, "bold"), bg="#1e293b", fg="#cbd5e1", anchor="e").grid(row=row_idx, column=1, sticky="e", padx=10, pady=6)
        entry = tk.Entry(parent, font=("Arial", 11), bg="#334155", fg="white", insertbackground="white", bd=2, relief="sunken", width=30)
        entry.grid(row=row_idx, column=0, sticky="w", padx=10, pady=6)
        self.fields[field_key] = entry
        self.widgets_ordered.append(entry)

    def add_smart_combo(self, parent, label_text, field_key, values, row_idx):
        tk.Label(parent, text=label_text, font=("Arial", 11, "bold"), bg="#1e293b", fg="#cbd5e1", anchor="e").grid(row=row_idx, column=1, sticky="e", padx=10, pady=6)
        combo = ttk.Combobox(parent, values=values, font=("Arial", 10), state="readonly", width=28)
        combo.grid(row=row_idx, column=0, sticky="w", padx=10, pady=6)
        if values: combo.set(values[0])
        self.fields[field_key] = combo
        self.widgets_ordered.append(combo)

    def load_car_data_by_search(self):
        """ جلب ملف البيانات بالكامل بالاعتماد على الرقم الإداري """
        target_admin = self.search_entry.get().strip()
        if not target_admin:
            messagebox.showwarning("تنبيه", "يرجى كتابة الرقم الإداري أولاً للبحث!")
            return
            
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Car_Master WHERE admin_num=?", (target_admin,))
            row = cursor.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل جلب البيانات: {e}")
            return
        
        if row:
            keys = [
                "admin_num", "plate_num", "chassis_num", "car_model", "manufacturer_en", "car_class",
                "manufacturer_ar", "car_class_ar", "car_color", "car_shape", "driver_job", "driver_route",
                "odometer_type", "driver_name", "whatsapp_num", "driver_password", "km_last_oil", "km_last_oil_filter",
                "km_last_air_filter", "km_last_plugs", "km_last_gear_oil", "km_last_coolant",
                "permit_start_year", "permit_start_month", "permit_start_day",
                "permit_end_year", "permit_end_month", "permit_end_day"
            ]
            
            for idx, key in enumerate(keys):
                val = str(row[idx]) if row[idx] is not None else ""
                widget = self.fields[key]
                if isinstance(widget, ttk.Combobox):
                    widget.set(val)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, val)
            messagebox.showinfo("نجاح", f"تم جلب ملف بيانات الشاحنة [{target_admin}] بنجاح!")
        else:
            messagebox.showwarning("غير موجود", "الرقم الإداري المدخل غير مسجل مسبقاً.")

    def save_car_data(self):
        """ حفظ أو تحديث كافة البيانات والمفاتيح في قاعدة البيانات المركزية """
        data = {k: v.get().strip() for k, v in self.fields.items()}
        
        if not data["admin_num"]:
            messagebox.showerror("خطأ مدخلات", "يجب كتابة الرقم الإداري للمركبة أولاً!")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO Car_Master (
                    admin_num, plate_num, chassis_num, car_model, manufacturer_en, car_class,
                    manufacturer_ar, car_class_ar, car_color, car_shape, driver_job, driver_route,
                    odometer_type, driver_name, whatsapp_num, driver_password, km_last_oil, km_last_oil_filter,
                    km_last_air_filter, km_last_plugs, km_last_gear_oil, km_last_coolant,
                    permit_start_year, permit_start_month, permit_start_day,
                    permit_end_year, permit_end_month, permit_end_day
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["admin_num"], data["plate_num"], data["chassis_num"], data["car_model"], data["manufacturer_en"], data["car_class"],
                data["manufacturer_ar"], data["car_class_ar"], data["car_color"], data["car_shape"],
                data["driver_job"], data["driver_route"], data["odometer_type"], data["driver_name"],
                data["whatsapp_num"], data["driver_password"], data["km_last_oil"], data["km_last_oil_filter"], data["km_last_air_filter"],
                data["km_last_plugs"], data["km_last_gear_oil"], data["km_last_coolant"],
                data["permit_start_year"], data["permit_start_month"], data["permit_start_day"],
                data["permit_end_year"], data["permit_end_month"], data["permit_end_day"]
            ))
            conn.commit()
            messagebox.showinfo("تم الحفظ بنجاح", f"🚀 تم تسجيل وحفظ بيانات المركبة رقم [{data['admin_num']}] بنجاح!")
        except 