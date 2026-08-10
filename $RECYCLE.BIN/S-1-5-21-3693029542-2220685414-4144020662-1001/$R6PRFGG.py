# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - وحدة السيارات الذكية (الإصدار الماسي المعمد 100%)
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم المعتمد برمجياً: CarGrandSystem2600
التعديل الإستراتيجي: توحيد مسار الخزنة مع كود الصيانة 100% في قرص C لإنهاء مشكلة عدم الحفظ
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
import urllib.request
import json
import threading
import os
from datetime import datetime

# توحيد المسار المركزي المشترك ليتطابق مع كود الصيانة تماماً
TARGET_DIR = "C:/Fakher_System"
DB_NAME = "Fakher_System_2026.db"
ADMIN_PASSWORD = "2600"

class CarGrandSystem2600:
    def __init__(self, root):
        self.root = root
        self.root.title("💎 منظومة فاخر 2600 - وحدة تعريف هوية السيارات والصيانة الذكية المتكاملة 💎")
        self.root.geometry("1550x920")
        self.root.state('zoomed')
        self.root.configure(bg="#0f172a") 
        
        self.fields = {}
        self.widgets_ordered = []
        
        self.resolve_db_path()
        self.init_database()
        self.build_creative_ui()

    def resolve_db_path(self):
        """تأمين إنشاء المجلد المركزي وتحديد المسار المشترك بدقة في قرص C"""
        if not os.path.exists(TARGET_DIR):
            try:
                os.makedirs(TARGET_DIR)
            except Exception as e:
                print(f"تنبيه إنشاء المجلد: {e}")
        self.db_path = os.path.join(TARGET_DIR, DB_NAME)

    def init_database(self):
        """ تأسيس الخزنة بنظام مرن يمنع القيود المعترضة أثناء الحفظ """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Car_Master (
                                admin_num TEXT PRIMARY KEY, 
                                plate_num TEXT, 
                                chassis_num TEXT,
                                car_model TEXT, manufacturer_en TEXT, car_class TEXT,
                                manufacturer_ar TEXT, car_class_ar TEXT, car_color TEXT, car_shape TEXT,
                                driver_job TEXT, driver_route TEXT, odometer_type TEXT,
                                driver_name TEXT, whatsapp_num TEXT,
                                km_last_oil TEXT, km_last_oil_filter TEXT, km_last_air_filter TEXT,
                                km_last_plugs TEXT, km_last_gear_oil TEXT, km_last_coolant TEXT,
                                permit_start_year TEXT, permit_start_month TEXT, permit_start_day TEXT,
                                permit_end_year TEXT, permit_end_month TEXT, permit_end_day TEXT
                            )''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"تنبيه التأسيس: {e}")

    def build_creative_ui(self):
        # 1. شريط التحكم العلوي الإستراتيجي
        top_bar = tk.Frame(self.root, bg="#1e293b", bd=1, relief="solid")
        top_bar.pack(fill="x", padx=15, pady=10)
        
        tk.Button(top_bar, text="✨ تعريف هوية سيارة جديدة", font=("Arial", 12, "bold"), bg="#0ea5e9", fg="white", 
                  command=self.clear_all_fields, width=22, cursor="hand2").pack(side="right", padx=10, pady=10)
        
        tk.Button(top_bar, text="🔍 استدعاء وتعديل هوية سيارة", font=("Arial", 12, "bold"), bg="#f59e0b", fg="black", 
                  command=self.search_and_load_car, width=25, cursor="hand2").pack(side="right", padx=10, pady=10)
        
        tk.Button(top_bar, text="💾 حفظ المعلومات في الخزنة", font=("Arial", 12, "bold"), bg="#10b981", fg="white", 
                  command=self.save_car_data, width=22, cursor="hand2").pack(side="right", padx=10, pady=10)

        # زر الطوارئ لتنظيف قاعدة البيانات من الرواسب الفارغة القديمة
        tk.Button(top_bar, text="🧼 إعادة تهيئة الخزنة وتصفير الرواسب", font=("Arial", 11, "bold"), bg="#ef4444", fg="white", 
                  command=self.danger_reset_database, width=25, cursor="hand2").pack(side="left", padx=10, pady=10)

        lbl_owner = tk.Label(top_bar, text="المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)", font=("Arial", 11, "bold", "italic"), bg="#1e293b", fg="#38bdf8")
        lbl_owner.pack(side="left", padx=15, pady=15)

        # 2. منطقة الحقول الرئيسية الموزعة
        main_frame = tk.Frame(self.root, bg="#0f172a")
        main_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # العمود الأيمن - الحقول الإدارية والتعريفية للسيارة
        right_panel = tk.LabelFrame(main_frame, text=" 🚗 أولاً: حقول تعريف السيارة وفئاتها الإدارية ", font=("Arial", 13, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=5)
        
        self.add_smart_field(right_panel, "حقل الرقم الإداري للمركبة (مطلوب):", "admin_num", 0)
        self.add_smart_field(right_panel, "حقل رقم اللوحة المعدنية للشرطة:", "plate_num", 1)
        
        # حقل رقم الشاصيه (VIN) باللون المميز
        tk.Label(right_panel, text="رقم الشاصيه الفريد (اكتبه واضغط Enter للسحب):", font=("Arial", 11, "bold"), bg="#1e293b", fg="#fbbf24", anchor="e").grid(row=2, column=1, sticky="e", padx=10, pady=6)
        chassis_entry = tk.Entry(right_panel, font=("Arial", 11, "bold"), bg="#1e1b4b", fg="#fcd34d", insertbackground="white", bd=2, relief="solid", width=30)
        chassis_entry.grid(row=2, column=0, sticky="w", padx=10, pady=6)
        chassis_entry.bind("<Return>", self.trigger_internet_vin_decode)
        self.fields["chassis_num"] = chassis_entry
        self.widgets_ordered.append(chassis_entry)

        self.add_smart_field(right_panel, "حقل موديل السيارة / سنة الصنع (آلي):", "car_model", 3)
        self.add_smart_field(right_panel, "حقل الشركة المصنعة بالإنجليزية (آلي):", "manufacturer_en", 4)
        
        # حقل فئة السيارة نصي مرن لاستقبال البيانات المسحوبة آلياً
        tk.Label(right_panel, text="حقل فئة السيارة الفني EN (آلي):", font=("Arial", 11, "bold"), bg="#1e293b", fg="#cbd5e1", anchor="e").grid(row=5, column=1, sticky="e", padx=10, pady=6)
        class_entry = tk.Entry(right_panel, font=("Arial", 11), bg="#334155", fg="white", width=30)
        class_entry.grid(row=5, column=0, sticky="w", padx=10, pady=6)
        self.fields["car_class"] = class_entry
        self.widgets_ordered.append(class_entry)

        self.add_smart_field(right_panel, "حقل اسم الشركة المصنعة بالعربية:", "manufacturer_ar", 6)
        self.add_smart_field(right_panel, "حقل فئة السيارة باللغة العربية:", "car_class_ar", 7)
        self.add_smart_field(right_panel, "حقل لون السيارة الخارجي الثابت:", "car_color", 8)
        self.add_smart_field(right_panel, "حقل شكل السيارة (صالون، هيلوكس، إلخ):", "car_shape", 9)
        
        self.add_smart_combo(right_panel, "طبيعة عمل السائق والخيارات المنسدلة:", "driver_job", [
            "رئيس مجلس الادارة", "اعضاء مجلس الادارة", "مدير اداره", "نائب مدير", 
            "مندوب مبيعات جمله", "مندوب مبيعات تجزئه", "مندوب سوبرات", "مشرف ميداني", 
            "مسؤول خدمات", "سائق يتبع اعضاء مجلس الادارة", "سائق"
        ], 10)
        
        self.add_smart_combo(right_panel, "حقل خط سير السيارة (المحافظات اليمنية):", "driver_route", [
            "صنعاء", "عدن", "تعز", "الحديدة", "إب", "حضرموت", "ذمار", "عمران", 
            "صعدة", "حجة", "البيضاء", "مارب", "الجوف", "المهرة", "سقطرى", "أبين", "شبوة", "لحج"
        ], 11)
        
        self.add_smart_combo(right_panel, "حقل نوع العداد للمركبة (ميل / كم):", "odometer_type", ["كم (Kilometer)", "ميل (Mile)"], 12)

        # العمود الأيسر - حقول السائق والعدادات الفنية والتواريخ
        left_panel = tk.LabelFrame(main_frame, text=" 🔧 ثانياً: بيانات السائق وعدادات الصيانة والتواريخ ", font=("Arial", 13, "bold"), bg="#1e293b", fg="#a7f3d0", labelanchor="ne")
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        self.add_smart_field(left_panel, "حقل اسم السائق المعين بالكامل:", "driver_name", 0)
        self.add_smart_field(left_panel, "حقل رقم الواتساب المفعل للسائق (+):", "whatsapp_num", 1)
        
        self.add_smart_field(left_panel, "عداد الكيلومتر عند آخر تغيير زيت محرك:", "km_last_oil", 2)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير فلتر الزيت:", "km_last_oil_filter", 3)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير فلتر الهواء:", "km_last_air_filter", 4)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير البواجي (شمعات):", "km_last_plugs", 5)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير زيت الجيربوكس:", "km_last_gear_oil", 6)
        self.add_smart_field(left_panel, "عداد الكيلومتر عند تغيير ماء الرديتر:", "km_last_coolant", 7)

        # صلاحية كرت تصريح السيارة الرسمي
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

        self.widgets_ordered.extend([
            self.fields["permit_start_year"], self.fields["permit_start_month"], self.fields["permit_start_day"],
            self.fields["permit_end_year"], self.fields["permit_end_month"], self.fields["permit_end_day"]
        ])

        self.setup_enter_navigation()
        self.auto_check_permit_alerts()

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

    def trigger_internet_vin_decode(self, event):
        vin = self.fields["chassis_num"].get().strip().upper()
        if not vin or len(vin) < 5:
            messagebox.showwarning("تنبيه الشاصيه", "⚠️ يرجى كتابة رقم شاصيه صحيح أولاً للسحب عبر الشبكة!")
            return
        
        self.fields["manufacturer_en"].delete(0, tk.END)
        self.fields["manufacturer_en"].insert(0, "...جاري الاتصال بالسيرفر العالمي...")
        
        threading.Thread(target=self.fetch_vin_data_from_internet, args=(vin,), daemon=True).start()

    def fetch_vin_data_from_internet(self, vin):
        try:
            url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                
            if "Results" in res_data and len(res_data["Results"]) > 0:
                data = res_data["Results"][0]
                
                make = data.get("Make", "").strip()
                model = data.get("Model", "").strip()
                year = data.get("ModelYear", "").strip()
                body_class = data.get("BodyClass", "").strip()

                self.fields["manufacturer_en"].delete(0, tk.END)
                if make: self.fields["manufacturer_en"].insert(0, make)
                
                self.fields["car_class"].delete(0, tk.END)
                if model: self.fields["car_class"].insert(0, model)
                
                self.fields["car_model"].delete(0, tk.END)
                if year: self.fields["car_model"].insert(0, year)
                
                self.fields["car_shape"].delete(0, tk.END)
                if body_class: self.fields["car_shape"].insert(0, body_class)

                messagebox.showinfo("نجاح السحب 🌐", f"🚀 تم سحب مواصفات السيارة بنجاح عبر الإنترنت من خوادم المصنع!\n\n🏢 الشركة: {make}\n🚗 الفئة: {model}\n📅 الموديل: {year}")
            else:
                self.fields["manufacturer_en"].delete(0, tk.END)
                messagebox.showwarning("الشبكة العالمية", "🛑 لم نتمكن من جلب تفاصيل دقيقة لهذا الرقم عبر الإنترنت.")
        except Exception as e:
            self.fields["manufacturer_en"].delete(0, tk.END)
            messagebox.showwarning("اتصال الإنترنت", f"⚠️ تعذر الاتصال بالسيرفر. يرجى التأكد من اتصال الكومبيوتر بالإنترنت.\nالتفاصيل: {e}")

    def check_cross_validation(self, admin_num, plate_num, chassis_num):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            if plate_num and plate_num != "":
                cursor.execute("SELECT admin_num FROM Car_Master WHERE plate_num=? AND admin_num != ?", (plate_num, admin_num))
                row = cursor.fetchone()
                if row:
                    return False, f"❌ تكرار لوحة: رقم اللوحة [{plate_num}] مسجل بالفعل لسيارة أخرى بالرقم الإداري [{row[0]}]!"

            if chassis_num and chassis_num != "":
                cursor.execute("SELECT admin_num FROM Car_Master WHERE chassis_num=? AND admin_num != ?", (chassis_num, admin_num))
                row = cursor.fetchone()
                if row:
                    return False, f"❌ تكرار شاصيه: رقم الشاصيه [{chassis_num}] مسجل لسيارة أخرى بالرقم الإداري [{row[0]}]!"

            return True, ""
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def save_car_data(self):
        admin_num = self.fields["admin_num"].get().strip()
        plate_num = self.fields["plate_num"].get().strip()
        chassis_num = self.fields["chassis_num"].get().strip()

        if not admin_num:
            messagebox.showwarning("بيانات ناقصة", "❌ يجب إدخال الرقم الإداري للمركبة أولاً لتحديد ملف الحفظ!")
            return

        is_valid, err_msg = self.check_cross_validation(admin_num, plate_num, chassis_num)
        if not is_valid:
            messagebox.showerror("تنبيه تكرار حقيقي", err_msg)
            return

        pwd = simpledialog.askstring("تحقق أمني 🔒", "أدخل الرقم السري لترحيل البيانات إلى الخزنة الفاخرة:", show="*")
        if pwd != ADMIN_PASSWORD:
            messagebox.showerror("صلاحية مرفوضة", "❌ الرقم السري خاطئ! تعذر الحفظ.")
            return

        data = {k: v.get().strip() for k, v in self.fields.items()}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO Car_Master (
                    admin_num, plate_num, chassis_num, car_model, manufacturer_en, car_class,
                    manufacturer_ar, car_class_ar, car_color, car_shape, driver_job, driver_route,
                    odometer_type, driver_name, whatsapp_num, km_last_oil, km_last_oil_filter,
                    km_last_air_filter, km_last_plugs, km_last_gear_oil, km_last_coolant,
                    permit_start_year, permit_start_month, permit_start_day,
                    permit_end_year, permit_end_month, permit_end_day
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                admin_num, plate_num, chassis_num, data["car_model"], data["manufacturer_en"], data["car_class"],
                data["manufacturer_ar"], data["car_class_ar"], data["car_color"], data["car_shape"],
                data["driver_job"], data["driver_route"], data["odometer_type"], data["driver_name"],
                data["whatsapp_num"], data["km_last_oil"], data["km_last_oil_filter"], data["km_last_air_filter"],
                data["km_last_plugs"], data["km_last_gear_oil"], data["km_last_coolant"],
                data["permit_start_year"], data["permit_start_month"], data["permit_start_day"],
                data["permit_end_year"], data["permit_end_month"], data["permit_end_day"]
            ))
            conn.commit()
            messagebox.showinfo("تم التوثيق 🔒", f"🚀 تم حفظ وتأمين بيانات السيارة رقم [{admin_num}] في الخزنة الموحدة بنجاح!")
            self.clear_all_fields()
        except Exception as e:
            messagebox.showerror("خطأ خزنة", f"تعذر الحفظ: {e}")
        finally:
            conn.close()

    def search_and_load_car(self):
        q = simpledialog.askstring("البحث الذكي 🔍", "أدخل الرقم الإداري أو رقم اللوحة للسيارة:")
        if not q: return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Car_Master WHERE admin_num=? OR plate_num=?", (q.strip(), q.strip()))
            row = cursor.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror("خطأ خزنة", f"فشل جلب البيانات: {e}")
            return
        
        if row:
            self.fields["admin_num"].configure(state="normal")
            self.clear_all_fields()

            keys = [
                "admin_num", "plate_num", "chassis_num", "car_model", "manufacturer_en", "car_class",
                "manufacturer_ar", "car_class_ar", "car_color", "car_shape", "driver_job", "driver_route",
                "odometer_type", "driver_name", "whatsapp_num", "km_last_oil", "km_last_oil_filter",
                "km_last_air_filter", "km_last_plugs", "km_last_gear_oil", "km_last_coolant",
                "permit_start_year", "permit_start_month", "permit_start_day",
                "permit_end_year", "permit_end_month", "permit_end_day"
            ]
            
            for idx, key in enumerate(keys):
                val = str(row[idx]) if row[idx] is not None else ""
                if isinstance(self.fields[key], ttk.Combobox):
                    self.fields[key].set(val)
                else:
                    self.fields[key].insert(0, val)
            
            self.fields["admin_num"].configure(state="disabled")
            messagebox.showinfo("نجاح الاستدعاء 📡", "✅ تم استدعاء ملف السيارة وإدراج بياناتها للتعديل الحين.")
        else:
            messagebox.showerror("خطأ في البحث", "❌ لم نجد أي مركبة تطابق المدخلات في الخزنة الموحدة.")

    def clear_all_fields(self):
        for key, widget in self.fields.items():
            if isinstance(widget, tk.Entry):
                widget.configure(state="normal")
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set("")
        self.fields["admin_num"].configure(state="normal")
        self.fields["admin_num"].focus_set()

    def danger_reset_database(self):
        pwd = simpledialog.askstring("تصفير ⚠️", "أدخل الرقم السري لتصفير وتنظيف رواسب الجدول القديم:", show="*")
        if pwd == ADMIN_PASSWORD:
            if messagebox.askyesno("تأكيد حاسم", "هل تريد تنظيف وإعادة بناء جدول السيارات لمسح أي تداخلات قديمة تماماً؟"):
                try:
                    conn = sqlite3.connect(self.db_path)
                    conn.cursor().execute("DROP TABLE IF EXISTS Car_Master")
                    conn.commit()
                    conn.close()
                    self.init_database()
                    self.clear_all_fields()
                    messagebox.showinfo("نجاح 🧼", "تم تصفير الرواسب وإعادة تهيئة نظام الملفات الجديد بنجاح.")
                except Exception as e:
                    messagebox.showerror("خطأ", str(e))

    def auto_check_permit_alerts(self):
        today = datetime.now()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT admin_num, plate_num, driver_name, permit_end_year, permit_end_month, permit_end_day FROM Car_Master")
            rows = cursor.fetchall()
            conn.close()
        except Exception: rows = []
        
        alerts = []
        for row in rows:
            a_num, plate, driver, e_year, e_month, e_day = row
            if e_year and e_month and e_day:
                try:
                    end_date = datetime(int(e_year), int(e_month), int(e_day))
                    delta_days = (end_date - today).days
                    if 0 <= delta_days <= 7:
                        alerts.append(f"⚠️ السيارة إداري [{a_num}] لوحة ({plate}) - متبقي: {delta_days} أيام!")
                except ValueError: pass
        if alerts:
            messagebox.showwarning("⚠️ إنذار انتهاء التجديد", "\n".join(alerts))

if __name__ == "__main__":
    root = tk.Tk()
    app = CarGrandSystem2600(root)
    root.mainloop()