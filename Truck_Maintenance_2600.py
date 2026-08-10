# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - سجل الصيانة الفني
الإصدار 2.0 - محسن بالكامل
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
import sqlite3
from datetime import datetime
import os
import webbrowser
import urllib.parse
import tempfile
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Fakher_System_2026.db")


class TruckMaintenanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("منظومة فاخر 2600 - سجل الصيانة v2.0")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0f172a")

        self.is_truck_loaded = False
        self.loaded_plate = ""
        self.loaded_driver = ""
        self.loaded_whatsapp = ""
        self.loaded_admin = ""
        self.dyn_widgets = {}
        self.current_report_html = ""

        self.init_db()
        self.build_ui()
        self.root.after(1000, self.check_data)

    def init_db(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Truck_Maintenance_Logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plate_num TEXT,
                    admin_num TEXT,
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
            conn.commit()
            conn.close()
        except Exception as e:
            print("init_db error: " + str(e))

    def check_data(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Car_Master'")
            table_exists = cursor.fetchone()

            if not table_exists:
                msg = (
                    "لم يتم العثور على جدول السيارات!\n\n"
                    "الحلول:\n"
                    "1. شغل ملف Truck_Identity_2600.py أولاً\n"
                    "2. تأكد أن الملفين في نفس المجلد\n"
                    "3. اضغط نعم لإنشاء بيانات تجريبية"
                )
                if messagebox.askyesno("تنبيه", msg):
                    self.create_sample_data()
                conn.close()
                return

            cursor.execute("SELECT COUNT(*) FROM Car_Master")
            count = cursor.fetchone()[0]
            conn.close()

            if count == 0:
                self.status_bar.config(text="جاهز - لا توجد شاحنات")
            else:
                self.status_bar.config(text="جاهز - شاحنات: " + str(count))

        except Exception as e:
            self.status_bar.config(text="خطأ: " + str(e))

    def create_sample_data(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Car_Master (
                    admin_num TEXT PRIMARY KEY, plate_num TEXT, chassis_num TEXT,
                    car_model TEXT, manufacturer_en TEXT, car_class TEXT,
                    manufacturer_ar TEXT, car_class_ar TEXT, car_color TEXT, car_shape TEXT,
                    driver_job TEXT, driver_route TEXT, odometer_type TEXT,
                    driver_name TEXT, whatsapp_num TEXT,
                    km_last_oil TEXT, km_last_oil_filter TEXT, km_last_air_filter TEXT,
                    km_last_plugs TEXT, km_last_gear_oil TEXT, km_last_coolant TEXT,
                    permit_start_year TEXT, permit_start_month TEXT, permit_start_day TEXT,
                    permit_end_year TEXT, permit_end_month TEXT, permit_end_day TEXT
                )
            """)
            sample = [
                ("TRK-100-2600", "أ ب ج 2600", "WDB9634232L123456", "2022", "Mercedes", "Actros",
                 "مرسيدس", "أكتروس", "أبيض", "شاحنة ثقيل", "سائق", "صنعاء", "كم",
                 "محمد علي الناشري", "+966501234567", "", "", "", "", "", "",
                 "2024", "1", "1", "2025", "1", "1"),
                ("TRK-100-8801", "د هـ و 8801", "YV2AHA0A1LB123456", "2021", "Volvo", "FH16",
                 "فولفو", "FH16", "أزرق", "شاحنة ثقيل", "سائق", "عدن", "كم",
                 "أحمد سالم البريدي", "+966509876543", "", "", "", "", "", "",
                 "2024", "6", "1", "2025", "6", "1"),
            ]
            cursor.executemany(
                "INSERT OR REPLACE INTO Car_Master VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                sample
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("تم", "تم إنشاء بيانات تجريبية!")
            self.status_bar.config(text="جاهز - بيانات تجريبية")
        except Exception as e:
            messagebox.showerror("خطأ", "فشل: " + str(e))

    def build_ui(self):
        header = tk.Frame(self.root, bg="#1e1b4b", pady=10)
        header.pack(fill="x", padx=10, pady=5)
        tk.Label(header, text="⚙️ منظومة فاخر 2600 - سجل الصيانة v2.0", 
                 font=("Arial", 20, "bold"), bg="#1e1b4b", fg="#38bdf8").pack()

        self.status_bar = tk.Label(self.root, text="جاري التحميل...", 
                                   font=("Arial", 10), bg="#0f172a", fg="#94a3b8", anchor="e")
        self.status_bar.pack(fill="x", padx=10, pady=2)

        search_frame = tk.LabelFrame(self.root, text=" البحث عن الشاحنة ",
                                     font=("Arial", 12, "bold"), bg="#1e293b",
                                     fg="#38bdf8", labelanchor="ne", padx=15, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="أدخل (اسم السائق / رقم اللوحة / الرقم الإداري / الواتساب / الشاصيه):",
                 font=("Arial", 11, "bold"), bg="#1e293b", fg="white").pack(side="right", padx=5)

        self.txt_search = tk.Entry(search_frame, font=("Arial", 14, "bold"), width=40,
                                   justify="center", bg="#334155", fg="white",
                                   insertbackground="white")
        self.txt_search.pack(side="right", padx=10)
        self.txt_search.bind("<Return>", lambda e: self.search())
        self.txt_search.focus_set()

        tk.Button(search_frame, text="🔍 بحث", font=("Arial", 12, "bold"),
                  bg="#2563eb", fg="white", padx=20, command=self.search).pack(side="right", padx=5)

        tk.Button(search_frame, text="📋 عرض كل الشاحنات", font=("Arial", 11, "bold"),
                  bg="#7c3aed", fg="white", command=self.show_all).pack(side="left", padx=5)

        main_frame = tk.Frame(self.root, bg="#0f172a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.right_panel = tk.LabelFrame(main_frame, text=" هوية الشاحنة ",
                                         font=("Arial", 13, "bold"), bg="#1e293b",
                                         fg="#facc15", labelanchor="ne",
                                         padx=15, pady=15, width=400)
        self.right_panel.pack(side="right", fill="y", padx=5, pady=5)
        self.right_panel.pack_propagate(False)

        identity_data = [
            ("الرقم الإداري:", "val_admin"),
            ("رقم اللوحة:", "val_plate"),
            ("اسم السائق:", "val_driver"),
            ("واتساب:", "val_whatsapp"),
            ("نوع الشاحنة:", "val_type"),
            ("الموديل:", "val_model"),
            ("اللون:", "val_color"),
            ("خط السير:", "val_route"),
        ]

        for label_text, attr_name in identity_data:
            frame = tk.Frame(self.right_panel, bg="#1e293b")
            frame.pack(fill="x", pady=4)
            tk.Label(frame, text=label_text, font=("Arial", 11, "bold"),
                     bg="#1e293b", fg="#94a3b8").pack(anchor="e")
            lbl = tk.Label(frame, text="بانتظار الاستدعاء...", font=("Arial", 12, "bold"),
                           bg="#1e293b", fg="#38bdf8", wraplength=360)
            lbl.pack(anchor="e", pady=1)
            setattr(self, attr_name, lbl)

        report_frame = tk.LabelFrame(self.right_panel, text=" التقارير والمشاركة ",
                                     font=("Arial", 11, "bold"), bg="#1e293b",
                                     fg="#67e8f9", labelanchor="ne", padx=10, pady=10)
        report_frame.pack(fill="x", pady=10)

        tk.Button(report_frame, text="📋 أرشيف الصيانة", font=("Arial", 10, "bold"),
                  bg="#7c3aed", fg="white", command=self.show_archive).pack(fill="x", pady=2)
        tk.Button(report_frame, text="👁️ معاينة + تعديل التقرير", font=("Arial", 10, "bold"),
                  bg="#0ea5e9", fg="white", command=self.preview_report).pack(fill="x", pady=2)
        tk.Button(report_frame, text="🖨️ طباعة التقرير", font=("Arial", 10, "bold"),
                  bg="#db2777", fg="white", command=self.print_report).pack(fill="x", pady=2)
        tk.Button(report_frame, text="📊 تقرير شامل (كل العمليات)", font=("Arial", 10, "bold"),
                  bg="#f59e0b", fg="black", command=self.full_report).pack(fill="x", pady=2)
        tk.Button(report_frame, text="💾 حفظ التقرير كملف", font=("Arial", 10, "bold"),
                  bg="#6366f1", fg="white", command=self.save_report_file).pack(fill="x", pady=2)
        tk.Button(report_frame, text="📤 إرسال واتساب (نص)", font=("Arial", 10, "bold"),
                  bg="#16a34a", fg="white", command=self.send_whatsapp).pack(fill="x", pady=2)
        tk.Button(report_frame, text="📎 إرسال ملف واتساب", font=("Arial", 10, "bold"),
                  bg="#8b5cf6", fg="white", command=self.send_file_whatsapp).pack(fill="x", pady=2)
        tk.Button(report_frame, text="📧 إرسال بريد إلكتروني", font=("Arial", 10, "bold"),
                  bg="#ec4899", fg="white", command=self.send_email).pack(fill="x", pady=2)

        self.left_panel = tk.LabelFrame(main_frame, text=" بيانات الصيانة ",
                                        font=("Arial", 13, "bold"), bg="#1e293b",
                                        fg="white", labelanchor="ne", padx=15, pady=15)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        fixed_frame = tk.Frame(self.left_panel, bg="#1e293b")
        fixed_frame.pack(fill="x", pady=5)

        tk.Label(fixed_frame, text="عداد الكيلومتر:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").pack(side="right", padx=5)
        self.txt_km = tk.Entry(fixed_frame, font=("Arial", 13, "bold"), width=15, justify="center")
        self.txt_km.pack(side="right", padx=10)

        tk.Label(fixed_frame, text="اسم الورشة:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").pack(side="right", padx=5)
        self.txt_workshop = tk.Entry(fixed_frame, font=("Arial", 13, "bold"), width=25, justify="center")
        self.txt_workshop.pack(side="right", padx=10)

        type_frame = tk.Frame(self.left_panel, bg="#1e293b")
        type_frame.pack(fill="x", pady=10)
        tk.Label(type_frame, text="نوع الاستبدال:", font=("Arial", 12, "bold"),
                 bg="#1e293b", fg="#67e8f9").pack(side="right", padx=5)

        self.combo_main_type = ttk.Combobox(type_frame, state="readonly", width=30,
                                            font=("Arial", 12, "bold"),
                                            values=["استبدال قطع في المحرك",
                                                    "استبدال قطع في البودي",
                                                    "استبدال قطع كهربائية",
                                                    "استبدال قطع أخرى",
                                                    "إطارات",
                                                    "بطاريات"])
        self.combo_main_type.pack(side="right", padx=10)
        self.combo_main_type.bind("<<ComboboxSelected>>", self.handle_type)

        self.dynamic_panel = tk.Frame(self.left_panel, bg="#1e293b", bd=2,
                                      relief="groove", pady=10, padx=10)
        self.dynamic_panel.pack(fill="x", pady=10)

        tk.Label(self.dynamic_panel,
                 text="اختر نوع الاستبدال لإظهار الحقول الإضافية",
                 font=("Arial", 11, "italic"), bg="#1e293b", fg="#94a3b8").pack(pady=10)

        tk.Label(self.left_panel, text="وصف تفصيلي للأعطال:",
                 font=("Arial", 11, "bold"), bg="#1e293b", fg="white").pack(anchor="e", pady=5)
        self.txt_fault_details = tk.Text(self.left_panel, height=6, font=("Arial", 12),
                                         bg="#0f172a", fg="white", insertbackground="white")
        self.txt_fault_details.pack(fill="x", pady=5)

        tk.Button(self.left_panel, text="🔒 حفظ السجل (الرقم السري: 2600)",
                  font=("Arial", 13, "bold"), bg="#16a34a", fg="white",
                  pady=10, command=self.save).pack(fill="x", pady=15)

    def handle_type(self, event=None):
        for widget in self.dynamic_panel.winfo_children():
            widget.destroy()
        self.dyn_widgets = {}

        selected = self.combo_main_type.get()
        if not selected:
            return

        grid = tk.Frame(self.dynamic_panel, bg="#1e293b")
        grid.pack(fill="x")

        if selected == "بطاريات":
            self._battery_fields(grid)
        elif selected == "إطارات":
            self._tire_fields(grid)
        else:
            tk.Label(grid, text="استخدم صندوق الوصف أدناه لتفاصيل القطع الميكانيكية",
                     font=("Arial", 11, "bold"), bg="#1e293b", fg="#a7f3d0").pack(pady=15)

    def _battery_fields(self, parent):
        tk.Label(parent, text="نوع البطارية:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").grid(row=0, column=3, padx=10, pady=8, sticky="e")
        c1 = ttk.Combobox(parent, values=["بطارية إلكترونية", "بطارية أسيد سائل"],
                          font=("Arial", 11, "bold"), state="readonly", width=18, justify="center")
        c1.grid(row=0, column=2, padx=10, pady=8)
        self.dyn_widgets["sub_type"] = c1

        tk.Label(parent, text="سعة البطارية:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").grid(row=0, column=1, padx=10, pady=8, sticky="e")
        c2 = ttk.Combobox(parent, values=["45 أمبير", "50 أمبير", "55 أمبير", "60 أمبير", 
                                          "65 أمبير", "70 أمبير", "80 أمبير", "90 أمبير",
                                          "100 أمبير", "110 أمبير", "120 أمبير"],
                          font=("Arial", 11, "bold"), state="readonly", width=15, justify="center")
        c2.grid(row=0, column=0, padx=10, pady=8)
        self.dyn_widgets["capacity"] = c2

        tk.Label(parent, text="اسم/ماركة البطارية:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").grid(row=1, column=3, padx=10, pady=8, sticky="e")
        e1 = tk.Entry(parent, font=("Arial", 11, "bold"), width=20, justify="center")
        e1.grid(row=1, column=2, padx=10, pady=8)
        self.dyn_widgets["item_name"] = e1

        tk.Label(parent, text="المورد/البنشر:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").grid(row=1, column=1, padx=10, pady=8, sticky="e")
        c3 = ttk.Combobox(parent, values=["محل بنشر", "محل بطاريات", "الوكيل"],
                          font=("Arial", 11, "bold"), state="readonly", width=18, justify="center")
        c3.grid(row=1, column=0, padx=10, pady=8)
        self.dyn_widgets["supplier_name"] = c3

        tk.Label(parent, text="تاريخ الإنتاج:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").grid(row=2, column=3, padx=10, pady=8, sticky="e")
        e2 = tk.Entry(parent, font=("Arial", 11, "bold"), width=20, justify="center")
        e2.grid(row=2, column=2, padx=10, pady=8)
        e2.insert(0, "MM/YYYY")
        self.dyn_widgets["prod_date"] = e2

    def _tire_fields(self, parent):
        tk.Label(parent, text="اسم/ماركة الإطار:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").grid(row=0, column=3, padx=10, pady=8, sticky="e")
        e1 = tk.Entry(parent, font=("Arial", 11, "bold"), width=20, justify="center")
        e1.grid(row=0, column=2, padx=10, pady=8)
        self.dyn_widgets["item_name"] = e1

        tk.Label(parent, text="تاريخ الإنتاج:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").grid(row=0, column=1, padx=10, pady=8, sticky="e")
        e2 = tk.Entry(parent, font=("Arial", 11, "bold"), width=15, justify="center")
        e2.grid(row=0, column=0, padx=10, pady=8)
        e2.insert(0, "Week/Year")
        self.dyn_widgets["prod_date"] = e2

        tk.Label(parent, text="نوع/مقاس الإطار:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").grid(row=1, column=3, padx=10, pady=8, sticky="e")
        e3 = tk.Entry(parent, font=("Arial", 11, "bold"), width=20, justify="center")
        e3.grid(row=1, column=2, padx=10, pady=8)
        self.dyn_widgets["sub_type"] = e3

        tk.Label(parent, text="المورد/البنشر:", font=("Arial", 11, "bold"),
                 bg="#1e293b", fg="white").grid(row=1, column=1, padx=10, pady=8, sticky="e")
        c1 = ttk.Combobox(parent, values=["محل بنشر", "محل إطارات", "الوكيل"],
                          font=("Arial", 11, "bold"), state="readonly", width=18, justify="center")
        c1.grid(row=1, column=0, padx=10, pady=8)
        self.dyn_widgets["supplier_name"] = c1

    def search(self):
        query = self.txt_search.get().strip()
        if not query:
            messagebox.showwarning("تنبيه", "أدخل نص للبحث!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Car_Master'")
            if not cursor.fetchone():
                conn.close()
                messagebox.showerror("خطأ", "جدول السيارات غير موجود!")
                return

            cursor.execute("""
                SELECT admin_num, plate_num, driver_name, whatsapp_num, car_shape, car_model, car_color, driver_route
                FROM Car_Master
                WHERE admin_num LIKE ? OR plate_num LIKE ? OR driver_name LIKE ? 
                   OR whatsapp_num LIKE ? OR chassis_num LIKE ?
            """, ("%" + query + "%", "%" + query + "%", "%" + query + "%", "%" + query + "%", "%" + query + "%"))
            results = cursor.fetchall()

            if not results:
                query_no_space = query.replace(" ", "")
                cursor.execute("""
                    SELECT admin_num, plate_num, driver_name, whatsapp_num, car_shape, car_model, car_color, driver_route
                    FROM Car_Master
                    WHERE REPLACE(plate_num, ' ', '') LIKE ?
                """, ("%" + query_no_space + "%",))
                results = cursor.fetchall()

            conn.close()

            if not results:
                messagebox.showerror("غير موجود",
                    "لا توجد شاحنة مطابقة!\n\n"
                    "يمكنك البحث بـ:\n"
                    "• اسم السائق\n"
                    "• رقم اللوحة\n"
                    "• الرقم الإداري\n"
                    "• الواتساب\n"
                    "• الشاصيه")
                return

            if len(results) == 1:
                self.load_truck(results[0])
            else:
                self.show_selection(results)

        except Exception as e:
            messagebox.showerror("خطأ", "فشل في البحث: " + str(e))

    def show_selection(self, results):
        dialog = tk.Toplevel(self.root)
        dialog.title(str(len(results)) + " نتيجة")
        dialog.geometry("700x400")
        dialog.configure(bg="#0f172a")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="تم العثور على " + str(len(results)) + " شاحنة - اختر واحدة:",
                 font=("Arial", 14, "bold"), bg="#0f172a", fg="#38bdf8").pack(pady=10)

        columns = ("#", "الرقم الإداري", "اللوحة", "السائق")
        tree = ttk.Treeview(dialog, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        for i, row in enumerate(results, 1):
            tree.insert("", "end", values=(i, row[0], row[1], row[2]))

        def on_select():
            selected = tree.selection()
            if selected:
                idx = tree.index(selected[0])
                self.load_truck(results[idx])
                dialog.destroy()

        tk.Button(dialog, text="اختيار", font=("Arial", 12, "bold"),
                  bg="#2563eb", fg="white", command=on_select).pack(pady=10)
        tree.bind("<Double-1>", lambda e: on_select())

    def load_truck(self, row):
        admin_num, plate, driver, whatsapp, truck_type, model, color, route = row

        self.val_admin.config(text=admin_num or "غير مسجل")
        self.val_plate.config(text=plate or "غير مسجل")
        self.val_driver.config(text=driver or "غير مسجل")
        self.val_whatsapp.config(text=whatsapp or "غير مسجل")
        self.val_type.config(text=truck_type or "غير مسجل")
        self.val_model.config(text=model or "غير مسجل")
        self.val_color.config(text=color or "غير مسجل")
        self.val_route.config(text=route or "غير مسجل")

        self.loaded_admin = admin_num or ""
        self.loaded_plate = plate or ""
        self.loaded_driver = driver or ""
        self.loaded_whatsapp = whatsapp or ""
        self.is_truck_loaded = True

        self.root.title("فاخر 2600 | " + str(plate) + " | " + str(driver))
        self.status_bar.config(text="تم الاستدعاء: " + str(plate))

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Truck_Maintenance_Logs WHERE plate_num = ?", (plate,))
            count = cursor.fetchone()[0]
            conn.close()
        except:
            count = 0

        messagebox.showinfo("تم الاستدعاء",
            "اللوحة: " + str(plate) + "\n"
            "السائق: " + str(driver) + "\n"
            "سجلات الصيانة: " + str(count))

    def show_all(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Car_Master'")
            if not cursor.fetchone():
                conn.close()
                messagebox.showerror("خطأ", "جدول السيارات غير موجود!")
                return
                
            cursor.execute("""
                SELECT admin_num, plate_num, driver_name, whatsapp_num, car_shape, car_model, car_color, driver_route
                FROM Car_Master ORDER BY admin_num
            """)
            rows = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("خطأ", "فشل في جلب البيانات: " + str(e))
            return

        if not rows:
            messagebox.showinfo("فارغ", "لا توجد شاحنات مسجلة!")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("كل الشاحنات (" + str(len(rows)) + ")")
        dialog.geometry("800x450")
        dialog.configure(bg="#0f172a")

        tk.Label(dialog, text="إجمالي الشاحنات: " + str(len(rows)),
                 font=("Arial", 14, "bold"), bg="#0f172a", fg="#38bdf8").pack(pady=10)

        columns = ("الرقم الإداري", "اللوحة", "السائق", "النوع", "الموديل")
        tree = ttk.Treeview(dialog, columns=columns, show="headings", height=15)

        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=140, anchor="center")

        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        for row in rows:
            tree.insert("", "end", values=(row[0], row[1], row[2], row[4] or "—", row[5] or "—"))

        def on_select():
            selected = tree.selection()
            if selected:
                idx = tree.index(selected[0])
                self.load_truck(rows[idx])
                dialog.destroy()

        tree.bind("<Double-1>", lambda e: on_select())
        tk.Button(dialog, text="اختيار", font=("Arial", 11, "bold"),
                  bg="#2563eb", fg="white", command=on_select).pack(pady=10)

    def save(self):
        if not self.is_truck_loaded:
            messagebox.showerror("قفل أمني", "استدعِ الشاحنة أولاً!")
            return

        km = self.txt_km.get().strip()
        workshop = self.txt_workshop.get().strip()
        m_type = self.combo_main_type.get()
        fault = self.txt_fault_details.get("1.0", tk.END).strip()

        if not km or not workshop or not m_type:
            messagebox.showwarning("بيانات ناقصة", "املأ: العداد، الورشة، ونوع الاستبدال!")
            return

        try:
            km_val = float(km)
            if km_val < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("بيانات خاطئة", "عداد الكيلومتر يجب أن يكون رقماً موجباً!")
            return

        item_name = self.dyn_widgets.get("item_name", type('obj', (object,), {'get': lambda: ''})()).get().strip()
        prod_date = self.dyn_widgets.get("prod_date", type('obj', (object,), {'get': lambda: ''})()).get().strip()
        sub_type = self.dyn_widgets.get("sub_type", type('obj', (object,), {'get': lambda: ''})()).get().strip()
        capacity = self.dyn_widgets.get("capacity", type('obj', (object,), {'get': lambda: ''})()).get().strip()
        supplier = self.dyn_widgets.get("supplier_name", type('obj', (object,), {'get': lambda: ''})()).get().strip()

        pwd = simpledialog.askstring("تفويض", "أدخل الرقم السري (2600):", show="*")
        if pwd != "2600":
            messagebox.showerror("فشل", "الرقم السري خطأ!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Truck_Maintenance_Logs
                (plate_num, admin_num, driver_name, km_reading, workshop_name, replacement_type,
                 item_name, prod_date, sub_type, capacity, supplier_name, fault_details, log_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.loaded_plate, self.loaded_admin, self.loaded_driver, km_val,
                  workshop, m_type, item_name, prod_date, sub_type, capacity, supplier, fault,
                  datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()

            messagebox.showinfo("تم الحفظ", "تم حفظ السجل في الأرشيف!")
            self.clear_form()
            self.status_bar.config(text="سجل جديد: " + str(self.loaded_plate))
        except Exception as e:
            messagebox.showerror("فشل", "خطأ في الحفظ: " + str(e))

    def clear_form(self):
        self.txt_km.delete(0, tk.END)
        self.txt_workshop.delete(0, tk.END)
        self.txt_fault_details.delete("1.0", tk.END)
        self.combo_main_type.set("")
        for widget in self.dynamic_panel.winfo_children():
            widget.destroy()
        self.dyn_widgets = {}
        tk.Label(self.dynamic_panel, text="اختر نوع الاستبدال لإظهار الحقول الإضافية",
                 font=("Arial", 11, "italic"), bg="#1e293b", fg="#94a3b8").pack(pady=10)

    def get_history(self, plate_num=None):
        if not plate_num:
            plate_num = self.loaded_plate
        if not plate_num:
            return []
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT log_date, km_reading, workshop_name, replacement_type, item_name,
                       sub_type, capacity, supplier_name, fault_details
                FROM Truck_Maintenance_Logs
                WHERE plate_num = ?
                ORDER BY log_date DESC
            """, (plate_num,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except:
            return []

    def show_archive(self):
        if not self.is_truck_loaded:
            messagebox.showwarning("تنبيه", "استدعِ الشاحنة أولاً!")
            return

        history = self.get_history()

        win = tk.Toplevel(self.root)
        win.title("أرشيف: " + str(self.loaded_plate))
        win.geometry("1200x600")
        win.configure(bg="#0f172a")

        tk.Label(win, text="أرشيف الصيانة - " + str(self.loaded_plate),
                 font=("Arial", 16, "bold"), bg="#0f172a", fg="#38bdf8").pack(pady=10)
        tk.Label(win, text="السائق: " + str(self.loaded_driver) + " | العمليات: " + str(len(history)),
                 font=("Arial", 12), bg="#0f172a", fg="#94a3b8").pack(pady=5)

        cols = ("التاريخ", "العداد", "الورشة", "النوع", "القطعة", "السعة", "المورد", "الأعطال")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=18)
        for col in cols:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=130)

        sb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        sb.pack(side="right", fill="y", pady=10)

        for row in history:
            item = row[4] or "—"
            if row[5]:
                item = item + " (" + str(row[5]) + ")"
            fault_short = row[8] or "—"
            if fault_short and len(fault_short) > 40:
                fault_short = fault_short[:40] + "..."
            tree.insert("", "end", values=(
                row[0] or "—", row[1] or "—", row[2] or "—", row[3] or "—",
                item, row[6] or "—", row[7] or "—", fault_short
            ))

        if not history:
            messagebox.showinfo("فارغ", "لا توجد سجلات صيانة.")

    def generate_html(self, full_report=False):
        if not self.is_truck_loaded:
            return ""
        
        history = self.get_history()
        
        if not full_report and history:
            history = history[:5]
            report_title = "تقرير صيانة - " + str(self.loaded_plate)
            subtitle = "آخر 5 عمليات صيانة"
        else:
            report_title = "تقرير شامل - " + str(self.loaded_plate)
            subtitle = "جميع عمليات الصيانة (" + str(len(history)) + " عملية)"

        html_lines = []
        html_lines.append("<!DOCTYPE html>")
        html_lines.append('<html dir="rtl" lang="ar">')
        html_lines.append("<head><meta charset=\"UTF-8\"><title>" + report_title + "</title>")
        html_lines.append("<style>")
        html_lines.append("body{font-family:Arial,sans-serif;margin:40px;background:#f8fafc;color:#1e293b}")
        html_lines.append(".header{text-align:center;border-bottom:3px solid #2563eb;padding-bottom:20px;margin-bottom:30px}")
        html_lines.append(".header h1{color:#1e40af;margin:0;font-size:28px}")
        html_lines.append(".header h2{color:#64748b;margin:5px 0;font-size:16px}")
        html_lines.append(".info-box{background:#eff6ff;border-right:5px solid #2563eb;padding:15px;margin-bottom:25px;border-radius:8px}")
        html_lines.append(".summary-box{background:#f0fdf4;border-right:5px solid #16a34a;padding:15px;margin-bottom:25px;border-radius:8px}")
        html_lines.append("table{width:100%;border-collapse:collapse;margin-top:20px;font-size:14px}")
        html_lines.append("th{background:#1e40af;color:white;padding:12px;text-align:right}")
        html_lines.append("td{padding:10px;border-bottom:1px solid #cbd5e1}")
        html_lines.append("tr:nth-child(even){background:#f1f5f9}")
        html_lines.append("tr:hover{background:#e0f2fe}")
        html_lines.append(".badge{display:inline-block;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:bold}")
        html_lines.append(".badge-engine{background:#dbeafe;color:#1e40af}")
        html_lines.append(".badge-tires{background:#dcfce7;color:#166534}")
        html_lines.append(".badge-battery{background:#fef3c7;color:#92400e}")
        html_lines.append(".badge-body{background:#fce7f3;color:#be185d}")
        html_lines.append(".badge-electric{background:#f3e8ff;color:#7c3aed}")
        html_lines.append(".footer{text-align:center;margin-top:40px;color:#94a3b8;font-size:12px;border-top:1px solid #e2e8f0;padding-top:20px}")
        html_lines.append("@media print{body{margin:0}}")
        html_lines.append("</style></head>")
        html_lines.append("<body>")
        html_lines.append("<div class=\"header\"><h1>🛡️ منظومة فاخر 2600</h1><h2>" + report_title + "</h2></div>")
        
        html_lines.append("<div class=\"info-box\">")
        html_lines.append("<p><strong>🔢 اللوحة:</strong> " + str(self.loaded_plate) + "</p>")
        html_lines.append("<p><strong>🆔 الرقم الإداري:</strong> " + str(self.loaded_admin) + "</p>")
        html_lines.append("<p><strong>👤 السائق:</strong> " + str(self.loaded_driver) + "</p>")
        html_lines.append("<p><strong>📱 الواتساب:</strong> " + str(self.loaded_whatsapp) + "</p>")
        html_lines.append("<p><strong>📅 تاريخ التقرير:</strong> " + datetime.now().strftime("%Y-%m-%d %H:%M") + "</p>")
        html_lines.append("</div>")

        html_lines.append("<div class=\"summary-box\"><p><strong>📊 " + subtitle + "</strong></p></div>")

        html_lines.append("<table><thead><tr>")
        html_lines.append("<th>#</th><th>التاريخ</th><th>العداد</th><th>الورشة</th><th>النوع</th><th>القطعة</th><th>التفاصيل</th><th>المورد</th>")
        html_lines.append("</tr></thead><tbody>")

        for idx, row in enumerate(history, 1):
            badge = "badge-engine"
            rtype = str(row[3] or "")
            if "إطار" in rtype: badge = "badge-tires"
            elif "بطاري" in rtype: badge = "badge-battery"
            elif "بودي" in rtype: badge = "badge-body"
            elif "كهرب" in rtype: badge = "badge-electric"
                
            det = str(row[4] or "—")
            if row[5]: det = det + " - " + str(row[5])
            if row[6]: det = det + " - " + str(row[6])
            
            html_lines.append("<tr>")
            html_lines.append("<td>" + str(idx) + "</td>")
            html_lines.append("<td>" + str(row[0] or "—") + "</td>")
            html_lines.append("<td>" + str(row[1] or "—") + "</td>")
            html_lines.append("<td>" + str(row[2] or "—") + "</td>")
            html_lines.append("<td><span class=\"badge " + badge + "\">" + rtype + "</span></td>")
            html_lines.append("<td>" + det + "</td>")
            html_lines.append("<td>" + str(row[8] or "—") + "</td>")
            html_lines.append("<td>" + str(row[7] or "—") + "</td>")
            html_lines.append("</tr>")

        if not history:
            html_lines.append('<tr><td colspan="8" style="text-align:center;color:#94a3b8;padding:30px">لا توجد سجلات صيانة</td></tr>')

        html_lines.append("</tbody></table>")
        html_lines.append("<div class=\"footer\"><p>🛡️ منظومة فاخر 2600 - المهندس جمال سويد</p>")
        html_lines.append("<p>تم إنشاء هذا التقرير بتاريخ: " + datetime.now().strftime("%Y/%m/%d") + "</p></div>")
        html_lines.append("</body></html>")

        return "\n".join(html_lines)

    def preview_report(self):
        if not self.is_truck_loaded:
            messagebox.showwarning("تنبيه", "استدعِ الشاحنة أولاً!")
            return
        self.current_report_html = self.generate_html()
        if not self.current_report_html:
            return
        win = tk.Toplevel(self.root)
        win.title("معاينة التقرير - " + str(self.loaded_plate))
        win.geometry("900x700")
        win.configure(bg="#0f172a")
        tk.Label(win, text="👁️ معاينة التقرير - يمكنك التعديل قبل الحفظ أو الطباعة",
                 font=("Arial", 14, "bold"), bg="#0f172a", fg="#38bdf8").pack(pady=10)
        text_frame = tk.Frame(win, bg="#0f172a")
        text_frame.pack(fill="both", expand=True, padx=15, pady=10)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        self.report_editor = tk.Text(text_frame, font=("Courier New", 10), 
                                     bg="#1e293b", fg="#e2e8f0", 
                                     insertbackground="white",
                                     yscrollcommand=scrollbar.set,
                                     wrap="word")
        self.report_editor.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.report_editor.yview)
        self.report_editor.insert("1.0", self.current_report_html)
        btn_frame = tk.Frame(win, bg="#0f172a")
        btn_frame.pack(fill="x", padx=15, pady=10)
        tk.Button(btn_frame, text="🔄 تحديث المعاينة", font=("Arial", 11, "bold"),
                  bg="#0ea5e9", fg="white", 
                  command=lambda: self._refresh_preview()).pack(side="right", padx=5)
        tk.Button(btn_frame, text="💾 حفظ التعديلات", font=("Arial", 11, "bold"),
                  bg="#10b981", fg="white",
                  command=lambda: self._save_edited_report()).pack(side="right", padx=5)
        tk.Button(btn_frame, text="🖨️ طباعة", font=("Arial", 11, "bold"),
                  bg="#db2777", fg="white",
                  command=lambda: self._print_edited_report()).pack(side="right", padx=5)
        tk.Button(btn_frame, text="📤 حفظ كملف", font=("Arial", 11, "bold"),
                  bg="#6366f1", fg="white",
                  command=lambda: self._save_edited_as_file()).pack(side="left", padx=5)

    def _refresh_preview(self):
        self.current_report_html = self.report_editor.get("1.0", tk.END)
        safe = re.sub(r'[^\w\-]', '_', self.loaded_plate)
        path = os.path.join(tempfile.gettempdir(), "Preview_" + safe + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.current_report_html)
        webbrowser.open("file:///" + path)

    def _save_edited_report(self):
        self.current_report_html = self.report_editor.get("1.0", tk.END)
        messagebox.showinfo("تم", "تم حفظ التعديلات في الذاكرة.")

    def _print_edited_report(self):
        html = self.report_editor.get("1.0", tk.END)
        safe = re.sub(r'[^\w\-]', '_', self.loaded_plate)
        path = os.path.join(tempfile.gettempdir(), "Report_" + safe + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open("file:///" + path)
        messagebox.showinfo("جاهز", "تم فتح التقرير في المتصفح للطباعة.")

    def _save_edited_as_file(self):
        html = self.report_editor.get("1.0", tk.END)
        safe = re.sub(r'[^\w\-]', '_', self.loaded_plate)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            initialfile="Report_" + safe + "_" + datetime.now().strftime("%Y%m%d"),
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            messagebox.showinfo("تم الحفظ", "تم حفظ التقرير في:\n" + file_path)

    def full_report(self):
        if not self.is_truck_loaded:
            messagebox.showwarning("تنبيه", "استدعِ الشاحنة أولاً!")
            return
        try:
            html = self.generate_html(full_report=True)
            safe = re.sub(r'[^\w\-]', '_', self.loaded_plate)
            path = os.path.join(tempfile.gettempdir(), "FullReport_" + safe + ".html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            webbrowser.open("file:///" + path)
            history = self.get_history()
            messagebox.showinfo("جاهز", 
                "تم فتح التقرير الشامل في المتصفح.\n"
                "إجمالي العمليات: " + str(len(history)))
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

    def save_report_file(self):
        if not self.is_truck_loaded:
            messagebox.showwarning("تنبيه", "استدعِ الشاحنة أولاً!")
            return
        html = self.generate_html(full_report=True)
        safe = re.sub(r'[^\w\-]', '_', self.loaded_plate)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            initialfile="Report_" + safe + "_" + datetime.now().strftime("%Y%m%d_%H%M"),
            filetypes=[("HTML files", "*.html"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html)
                messagebox.showinfo("تم الحفظ", 
                    "تم حفظ التقرير بنجاح!\n\n"
                    "المسار: " + file_path)
            except Exception as e:
                messagebox.showerror("خطأ", "فشل في الحفظ: " + str(e))

    def send_file_whatsapp(self):
        if not self.is_truck_loaded:
            messagebox.showwarning("تنبيه", "استدعِ الشاحنة أولاً!")
            return
        html = self.generate_html(full_report=True)
        safe = re.sub(r'[^\w\-]', '_', self.loaded_plate)
        file_path = os.path.join(tempfile.gettempdir(), "Report_" + safe + "_" + datetime.now().strftime("%Y%m%d_%H%M") + ".html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        if not self.loaded_whatsapp or self.loaded_whatsapp == "غير مسجل":
            messagebox.showinfo("تم حفظ الملف", 
                "تم حفظ التقرير في:\n" + file_path + "\n\n"
                "يمكنك إرساله يدوياً عبر واتساب ويب.")
            return
        phone = re.sub(r'[^\d]', '', self.loaded_whatsapp)
        if phone.startswith("05"): phone = "966" + phone[1:]
        elif phone.startswith("5"): phone = "966" + phone
        if len(phone) < 9:
            messagebox.showinfo("تم حفظ الملف", 
                "تم حفظ التقرير في:\n" + file_path + "\n\n"
                "رقم الواتساب غير صالح للإرسال المباشر.")
            return
        url = "https://web.whatsapp.com/send?phone=" + phone
        webbrowser.open(url)
        messagebox.showinfo("جاهز", 
            "تم حفظ التقرير في:\n" + file_path + "\n\n"
            "تم فتح واتساب ويب.\n"
            "📎 اسحب الملف وأفلته في الدردشة.")

    def send_email(self):
        if not self.is_truck_loaded:
            messagebox.showwarning("تنبيه", "استدعِ الشاحنة أولاً!")
            return
        history = self.get_history()
        subject = "تقرير صيانة شاحنة - " + str(self.loaded_plate)
        body = "السلام عليكم،\n\n"
        body = body + "مرفق تقرير صيانة الشاحنة:\n\n"
        body = body + "🔢 اللوحة: " + str(self.loaded_plate) + "\n"
        body = body + "🆔 الرقم الإداري: " + str(self.loaded_admin) + "\n"
        body = body + "👤 السائق: " + str(self.loaded_driver) + "\n"
        body = body + "📊 إجمالي عمليات الصيانة: " + str(len(history)) + "\n\n"
        body = body + "📋 تفاصيل العمليات:\n"
        for i, row in enumerate(history, 1):
            body = body + "\n" + str(i) + ". " + str(row[3] or 'صيانة') + "\n"
            body = body + "   التاريخ: " + str(row[0] or '—') + "\n"
            body = body + "   العداد: " + str(row[1] or '—') + " كم\n"
            body = body + "   الورشة: " + str(row[2] or '—') + "\n"
        body = body + "\n\nمع التحية،\n"
        body = body + "منظومة فاخر 2600\n"
        body = body + "المهندس جمال سويد (أبا عبد الله)"
        html = self.generate_html(full_report=True)
        safe = re.sub(r'[^\w\-]', '_', self.loaded_plate)
        attach_path = os.path.join(tempfile.gettempdir(), "Report_" + safe + "_" + datetime.now().strftime("%Y%m%d") + ".html")
        with open(attach_path, "w", encoding="utf-8") as f:
            f.write(html)
        mailto_url = "mailto:?subject=" + urllib.parse.quote(subject) + "&body=" + urllib.parse.quote(body)
        webbrowser.open(mailto_url)
        messagebox.showinfo("جاهز", 
            "تم فتح برنامج البريد الإلكتروني.\n\n"
            "📎 الملف المرفق محفوظ في:\n" + attach_path + "\n\n"
            "يمكنك إرفاقه يدوياً في البريد.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TruckMaintenanceSystem(root)
    root.mainloop()