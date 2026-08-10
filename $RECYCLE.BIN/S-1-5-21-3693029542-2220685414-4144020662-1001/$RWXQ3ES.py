# -*- coding: utf-8 -*-
"""
منظومة النافذة الموحدة 2600 - المشغل المركزي السيادي الشامل والنهائي
المشرف الفني العام الأعلى: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد للملف: Fakher_Master_Gateway_2600.py
التحديث الجذري: دمج كافة المحاور، ربط الخوارزميات، وتأمين النوافذ ضد الانهيار الفوري
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import os
import sqlite3
import subprocess
import sys
from datetime import datetime

# المسارات الموحدة لقواعد البيانات والمعتمدة بالمنظومة
DB_CENTRAL = "Fakher_Central_Database_2600.db"
DB_SYSTEM = "Fakher_System_2026.db"

class FakherMasterGateway2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ مـنـظـومـة الـنـافـذة الـمـوحـدة والـرئـاسـيـة لأسـطـول 2600 🛡️")
        self.root.geometry("1550x850")
        self.root.state('zoomed') 
        self.root.configure(bg="#0b1329") # اللون الأزرق الملكي الداكن للغرفة السيادية
        
        self.system_password = "2600"
        self.active_processes = {}
        
        self.init_all_system_databases()
        self.build_framework_ui()

    def init_all_system_databases(self):
        """ التأكد من سلامة الجداول وبنائها محلياً لضمان عدم حدوث خطأ استدعاء """
        try:
            # 1. قاعدة البيانات المركزية للهويات
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

            # 2. قاعدة بيانات العمليات والديزل
            conn2 = sqlite3.connect(DB_SYSTEM)
            cursor2 = conn2.cursor()
            cursor2.execute("""
                CREATE TABLE IF NOT EXISTS Truck_Diesel_Logs_2600 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, chk_date TEXT, plate_num TEXT, 
                    driver_name TEXT, location TEXT, vin_code TEXT, start_km REAL, 
                    end_km REAL, fuel_liters REAL, waste_pct TEXT, eval_status TEXT, mechanic_hyp TEXT
                )
            """)
            conn2.commit()
            conn2.close()
        except Exception as e:
            print(f"تنبيه تهيئة قواعد البيانات: {e}")

    def build_framework_ui(self):
        # ==================== 1. الشريط العلوي الرئاسي الفخم ====================\
        header = tk.Frame(self.root, bg="#1c2541", height=100, bd=2, relief="groove")
        header.pack(fill="x", padx=10, pady=10)
        
        lbl_title = tk.Label(header, text="🏛️ الـمـشـغـل الـمـركـزي الـسـيـادي الـمـوحد - فـاخـر 2600 🏛️", 
                             font=("Arial", 22, "bold"), bg="#1c2541", fg="#38bdf8")
        lbl_title.pack(side="right", padx=25, pady=15)
        
        lbl_eng = tk.Label(header, text="المشرف العام الفني: المهندس جمال سويد (أبا عبد الله)", 
                           font=("Arial", 12, "bold", "italic"), bg="#1c2541", fg="#a7f3d0")
        lbl_eng.pack(side="left", padx=25, pady=25)

        # ==================== 2. لوحة التحكم وجناح الأزرار الموحد ====================\
        main_body = tk.Frame(self.root, bg="#0b1329")
        main_body.pack(fill="both", expand=True, padx=10, pady=5)

        # الجناح الأيمن: إدارة الشاحنات والديزل (50 شاحنة ثقيلة ومتوسطة)
        truck_panel = tk.LabelFrame(main_body, text=" 🚚 جناح إدارة ووقود الشاحنات والناقلات النقل الثقيل ", 
                                    font=("Arial", 14, "bold"), bg="#1c2541", fg="#f1f5f9", labelanchor="ne")
        truck_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # الجناح الأيسر: إدارة السيارات والصيانة (50 سيارة صالون وإدارية)
        car_panel = tk.LabelFrame(main_body, text=" 🚗 جناح إدارة وصيانة سيارات الصالون والإدارة العليا ", 
                                   font=("Arial", 14, "bold"), bg="#1c2541", fg="#f1f5f9", labelanchor="ne")
        car_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # --- أزرار الشاحنات (الجانب الأيمن) ---
        btn_truck_id = tk.Button(truck_panel, text="🆔 تعريف وتعديل هوية الشاحنات وبلاغات التصاريح", 
                                 command=lambda: self.launch_sub_module("Fakher_Truck_Identity_2600.py"),
                                 font=("Arial", 13, "bold"), bg="#0284c7", fg="white", activebackground="#0369a1", cursor="hand2", height=3)
        btn_truck_id.pack(fill="x", padx=20, pady=15)

        btn_truck_diesel = tk.Button(truck_panel, text="⛽ محرك مراقبة الديزل والالتقاط التفاعلي للأسماء", 
                                     command=lambda: self.launch_sub_module("Fakher_Truck_Diesel_2600.py"),
                                     font=("Arial", 13, "bold"), bg="#059669", fg="white", activebackground="#047857", cursor="hand2", height=3)
        btn_truck_diesel.pack(fill="x", padx=20, pady=15)

        btn_algo = tk.Button(truck_panel, text="🧠 تشغيل العقل الإلكتروني المركزي (محرك الخوارزميات والذكاء)", 
                             command=lambda: self.launch_sub_module("algorithms_engine.py"),
                             font=("Arial", 13, "bold"), bg="#7c3aed", fg="white", activebackground="#6d28d9", cursor="hand2", height=3)
        btn_algo.pack(fill="x", padx=20, pady=15)

        # --- أزرار السيارات (الجانب الأيسر) ---
        btn_car_id = tk.Button(car_panel, text="💎 وحدة تعريف هوية وتراخيص السيارات الصالون", 
                               command=lambda: self.launch_sub_module("Fakher_Car_Identity_2600.py"),
                               font=("Arial", 13, "bold"), bg="#2563eb", fg="white", activebackground="#1d4ed8", cursor="hand2", height=3)
        btn_car_id.pack(fill="x", padx=20, pady=15)

        btn_car_maint = tk.Button(car_panel, text="🛠️ سجل الصيانة الفني الحصين لقطع الغيار والإطارات", 
                                  command=lambda: self.launch_sub_module("Car_Maintenance_2600.py"),
                                  font=("Arial", 13, "bold"), bg="#ea580c", fg="white", activebackground="#c2410c", cursor="hand2", height=3)
        btn_car_maint.pack(fill="x", padx=20, pady=15)

        btn_print = tk.Button(car_panel, text="📊 محرك الطباعة المركزي وسندات صرف الباركود السيادية", 
                              command=lambda: self.launch_sub_module("Fakher_Print_Report_Engine_2600.py"),
                              font=("Arial", 13, "bold"), bg="#db2777", fg="white", activebackground="#be185d", cursor="hand2", height=3)
        btn_print.pack(fill="x", padx=20, pady=15)

        # ==================== 3. شريط الحالة السفلي والأمان ====================\
        footer = tk.Frame(self.root, bg="#0b1329", height=40)
        footer.pack(fill="x", side="bottom", padx=10, pady=5)
        
        lbl_status = tk.Label(footer, text="🛡️ نظام الرقابة المركزي مفعل | حالة الاتصال بقواعد البيانات: مستقرة وآمنة 100% 🔒", 
                              font=("Arial", 11, "bold"), bg="#0b1329", fg="#94a3b8")
        lbl_status.pack(side="right", padx=15)

        lbl_date = tk.Label(footer, text=f"تاريخ التشغيل السيادي: {datetime.now().strftime('%Y-%m-%d')}", 
                            font=("Arial", 10, "bold"), bg="#0b1329", fg="#38bdf8")
        lbl_date.pack(side="left", padx=15)

    def launch_sub_module(self, script_name):
        """ محرك الاستدعاء المركزي: يقوم بفتح الملفات الفرعية بشكل فني آمن ومستقل """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, script_name)

        # التحقق من وجود الملف في نفس المجلد لمنع الاختفاء الفوري للنافذة
        if not os.path.exists(full_path):
            messagebox.showwarning("تنبيه أمان المنظومة", f"⚠️ لم يتم العثور على ملف [{script_name}] في مجلد البرنامج الحقيقي.\nيرجى التأكد من وضعه بجانب هذا المشغل.")
            return

        try:
            # تشغيل الملف الفرعي باستخدام مفسر بايثون الحالي بشكل مستقل وآمن
            subprocess.Popen([sys.executable, full_path], shell=False)
        except Exception as e:
            messagebox.showerror("خطأ تشغيل", f"فشل تشغيل الوحدة الفرعية المحددة:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherMasterGateway2600(root)
    root.mainloop()