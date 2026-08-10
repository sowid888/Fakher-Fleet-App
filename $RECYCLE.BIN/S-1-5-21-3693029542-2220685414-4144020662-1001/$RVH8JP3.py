# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# تحديد المسار للعمل المستقل
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class FakherMasterDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🏛️ غـرفـة الـقـيـادة الـعـلـيـا - منظومة فاخر 2600 🏛️")
        self.root.geometry("1400x900")
        self.root.configure(bg="#020617")

        # العنوان الرئيسي
        tk.Label(root, text="منظومة فاخر السيادية 2600 - مركز القيادة الرقمي", 
                 font=("Arial", 22, "bold"), bg="#020617", fg="#38bdf8").pack(pady=20)

        # حاوية رئيسية للأزرار
        self.main_frame = tk.Frame(root, bg="#020617")
        self.main_frame.pack(expand=True, fill="both", padx=50, pady=20)

        # تعريف القائمة الشاملة (23 ملفاً)
        self.all_tools = [
            ("🚛 هوية الشاحنات", "Fakher_Truck_Identity_2600.PY"),
            ("🚗 هوية السيارات", "Fakher_Car_Identity_2600.py"),
            ("⚙️ صيانة الشاحنات", "Truck_Maintenance_2600.py"),
            ("🔧 صيانة السيارات", "Car_Maintenance_2600.py"),
            ("🛡️ درع الأتمتة", "Fakher_Automation_Shield_2600.py"),
            ("🧠 محرك الذكاء", "Fakher_Intelligence_Comparison_2600.py"),
            ("⛽ وقود السيارات", "Fakher_Car_Fuel_Consumption_2600.py"),
            ("🖨️ محرك الطباعة", "Fakher_Print_Report_Engine_2600.py"),
            ("🔑 مركز التراخيص", "code_generator.py"),
            ("🚨 إنذارات الصيانة", "Fakher_Maintenance_Alert_Engine_2600.py"),
            ("📈 معادلات الصيانة", "Fakher_Dynamic_Equations_2600.py"),
            ("🌐 النفق العالمي", "Fakher_Tunnel.py"),
            ("🕵️ كشاف البيانات", "Fakher_Search_Foretell_2600.py"),
            ("🛠️ فحص الخزنة", "inspect_db.py"),
            ("🤖 واجهة السائق", "main.py"),
            ("📡 سيرفر الشاحنات", "Fakher_Truck_Server_2600.py"),
            ("📊 محرك السيارات", "Fakher_Car_Intelligence_Engine.py"),
            ("💰 المحرك المالي", "Fakher_Financial_And_Depreciation_Engine.py"),
            ("📋 واجهة الإدارة", "Fakher_Admin_App.py"),
            ("🏛️ الواجهة المركزية", "Fakher_Interface_2600.py"),
            ("🔧 إصلاح الجداول", "Fakher_DB_Fixer.py.py")
        ]

        # بناء الأزرار بنظام الشبكة (Grid)
        for i, (name, script) in enumerate(self.all_tools):
            btn = tk.Button(self.main_frame, text=name, width=25, height=2, 
                            font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0",
                            activebackground="#38bdf8", relief="flat", cursor="hand2",
                            command=lambda s=script: self.run_script(s))
            btn.grid(row=i//4, column=i%4, padx=10, pady=10)

    def run_script(self, script_name):
        script_path = os.path.join(BASE_DIR, script_name)
        if os.path.exists(script_path):
            # تشغيل البرنامج كعملية منفصلة تماماً
            subprocess.Popen([sys.executable, script_path])
        else:
            messagebox.showerror("خطأ سيادي", f"الملف '{script_name}' مفقود! تأكد من وجوده في المجلد الرئيسي.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherMasterDashboard(root)
    root.mainloop()