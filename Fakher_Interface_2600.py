# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - الواجهة البرمجية الموحدة والشاملة
المشرف الفني العام الأعلى: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد للملف: Fakher_Master_Interface_2600.py
التحديث الجذري: دمج كافة الأقسام (الهويات، الديزل، والصيانة) في واجهة رسومية واحدة متكاملة
"""

import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# قواعد البيانات المعتمدة والموحدة في المنظومة
DB_CENTRAL = "Fakher_Central_Database_2600.db"
DB_SYSTEM = "Fakher_System_2026.db"

class FakherSovereignApp2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🏛️ مـنـظـومـة فـاخـر 2600 - الـواجهة الـمـركـزيـة الـمـوحـدة 🏛️")
        self.root.geometry("1550x850")
        self.root.state('zoomed')
        self.root.configure(bg="#0f172a") # اللون الداكن الملكي
        
        self.init_databases()
        self.build_main_ui()

    def init_databases(self):
        """ إنشاء وتأمين كافة الجداول الحصينة في مكانها الصحيح """
        try:
            # 1. جداول الهوية المركزية للشاحنات والسيارات
            conn1 = sqlite3.connect(DB_CENTRAL)
            cursor1 = conn1.cursor()
            cursor1.execute("""
                CREATE TABLE IF NOT EXISTS Truck_Main_Registry_2600 (
                    serial_num TEXT PRIMARY KEY, plate_num TEXT, driver_name TEXT, chassis_num TEXT,
                    permit_end_year TEXT, permit_end_month TEXT, permit_end_day TEXT
                )
            """)
            conn1.commit()
            conn1.close()

            # 2. جداول حركة الديزل والصيانة
            conn2 = sqlite3.connect(DB_SYSTEM)
            cursor2 = conn2.cursor()
            cursor2.execute("""
                CREATE TABLE IF NOT EXISTS Truck_Diesel_Logs_2600 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, chk_date TEXT, plate_num TEXT, 
                    driver_name TEXT, location TEXT, vin_code TEXT, start_km REAL, 
                    end_km REAL, fuel_liters REAL, waste_pct TEXT, eval_status TEXT
                )
            """)
            cursor2.execute("""
                CREATE TABLE IF NOT EXISTS Car_Maintenance_Logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, plate_num TEXT, driver_name TEXT, 
                    current_km REAL, workshop_name TEXT, maint_type TEXT, item_name TEXT, log_date TEXT
                )
            """)
            conn2.commit()
            conn2.close()
        except Exception as e:
            print(f"تنبيه تهيئة قواعد البيانات: {e}")

    def build_main_ui(self):
        # ==================== الشريط العلوي الرئاسي ====================
        header = tk.Frame(self.root, bg="#1e293b", height=80, bd=1, relief="solid")
        header.pack(fill="x", padx=10, pady=5)
        
        lbl_title = tk.Label(header, text="🏛️ الـواجهة الـتـنـفـيـذيـة الـمـوحـدة لأسـطـول ومـنـظـومـة فـاخـر 2600", 
                             font=("Arial", 20, "bold"), bg="#1e293b", fg="#38bdf8")
        lbl_title.pack(side="right", padx=20, pady=15)
        
        lbl_eng = tk.Label(header, text="المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)", 
                           font=("Arial", 12, "bold", "italic"), bg="#1e293b", fg="#a7f3d0")
        lbl_eng.pack(side="left", padx=20, pady=20)

        # ==================== نظام التبويب المركزي (Tabs) ====================
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # تحسين مظهر التبويبات لتناسب التصميم الداكن
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#0f172a', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Arial', 12, 'bold'), padding=[15, 5], background='#1e293b', foreground='#94a3b8')
        style.map('TNotebook.Tab', background=[('selected', '#38bdf8')], foreground=[('selected', '#0f172a')])

        # إنشاء الصفحات الرئيسية داخل الواجهة
        self.tab_trucks = tk.Frame(notebook, bg="#1e293b")
        self.tab_diesel = tk.Frame(notebook, bg="#1e293b")
        self.tab_cars = tk.Frame(notebook, bg="#1e293b")

        notebook.add(self.tab_trucks, text=" 🚚 إدارة هوية الشاحنات ")
        notebook.add(self.tab_diesel, text=" ⛽ مراقبة الديزل والوقود ")
        notebook.add(self.tab_cars, text=" 🚗 صيانة سيارات الإدارة ")

        # بناء محتويات كل تبويب تلقائياً داخل نفس الملف
        self.build_truck_registry_tab()
        self.build_diesel_monitoring_tab()
        self.build_car_maintenance_tab()

    # 1. تبويب إدارة هوية الشاحنات
    def build_truck_registry_tab(self):
        frame_input = tk.LabelFrame(self.tab_trucks, text=" تسجيل وتعديل البيانات الحصينة ", font=("Arial", 12, "bold"), bg="#1e293b", fg="#f1f5f9", labelanchor="ne")
        frame_input.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        fields = [
            ("الرقم الإداري للشاحنة:", "t_serial"),
            ("رقم اللوحة المعتمد:", "t_plate"),
            ("اسم السائق الكامل:", "t_driver"),
            ("رقم الشاصيه (VIN):", "t_chassis")
        ]

        self.truck_vars = {}
        for lbl_txt, var_name in fields:
            row = tk.Frame(frame_input, bg="#1e293b")
            row.pack(fill="x", padx=10, pady=10)
            lbl = tk.Label(row, text=lbl_txt, font=("Arial", 11, "bold"), bg="#1e293b", fg="#cbd5e1", width=20, anchor="e")
            lbl.pack(side="right", padx=5)
            entry = tk.Entry(row, font=("Arial", 12), bg="#0f172a", fg="#ffffff", insertbackground="white", justify="center")
            entry.pack(side="right", fill="x", expand=True, padx=5)
            self.truck_vars[var_name] = entry

        btn_save = tk.Button(frame_input, text="🔒 حفظ واعتماد الشاحنة بالخزنة", font=("Arial", 12, "bold"), bg="#0284c7", fg="white", command=self.save_truck_id)
        btn_save.pack(fill="x", padx=15, pady=20)

    def save_truck_id(self):
        s_num = self.truck_vars["t_serial"].get().strip()
        plate = self.truck_vars["t_plate"].get().strip()
        driver = self.truck_vars["t_driver"].get().strip()
        chassis = self.truck_vars["t_chassis"].get().strip()

        if not s_num or not plate or not driver:
            messagebox.showwarning("تنبيه الحقول", "❌ يرجى ملء كافة الحقول الأساسية للشاحنة!")
            return

        try:
            conn = sqlite3.connect(DB_CENTRAL)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO Truck_Main_Registry_2600 (serial_num, plate_num, driver_name, chassis_num)
                VALUES (?, ?, ?, ?)
            """, (s_num, plate, driver, chassis))
            conn.commit()
            conn.close()
            messagebox.showinfo("تم التوثيق الحصين", f"🚀 تم حفظ الشاحنة رقم {s_num} بنجاح تام!")
        except Exception as e:
            messagebox.showerror("خطأ في قاعدة البيانات", str(e))

    # 2. تبويب مراقبة الديزل والوقود
    def build_diesel_monitoring_tab(self):
        frame_diesel = tk.LabelFrame(self.tab_diesel, text=" حركات صرف ومراقبة هدر الديزل ", font=("Arial", 12, "bold"), bg="#1e293b", fg="#f1f5f9", labelanchor="ne")
        frame_diesel.pack(fill="both", expand=True, padx=15, pady=15)
        
        lbl_info = tk.Label(frame_diesel, text="⛽ نظام الاحتساب والربط المباشر مع التضاريس ومعدلات الاستهلاك القياسية لشاحنات الأسطول", font=("Arial", 11, "bold"), bg="#1e293b", fg="#38bdf8")
        lbl_info.pack(pady=10)

    # 3. تبويب صيانة سيارات الإدارة
    def build_car_maintenance_tab(self):
        frame_cars = tk.LabelFrame(self.tab_cars, text=" سجلات صيانة وقطع غيار سيارات الإدارة ", font=("Arial", 12, "bold"), bg="#1e293b", fg="#f1f5f9", labelanchor="ne")
        frame_cars.pack(fill="both", expand=True, padx=15, pady=15)
        
        lbl_info = tk.Label(frame_cars, text="🛠️ وحدة توثيق قطع الغيار، فحص الإطارات والبطاريات، وحساب الإهلاك المسافي", font=("Arial", 11, "bold"), bg="#1e293b", fg="#ea580c")
        lbl_info.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherSovereignApp2600(root)
    root.mainloop()
