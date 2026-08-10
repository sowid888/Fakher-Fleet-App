# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

class FakherMasterControl:
    def __init__(self, root):
        self.root = root
        self.root.title("🏛️ منظومة فاخر 2600 - مركز القيادة الرقمي")
        self.root.geometry("900x700")
        self.root.configure(bg="#020617")
        
        # العنوان
        tk.Label(root, text="مركز القيادة الرقمي - منظومة فاخر 2600", 
                 font=("Segoe UI", 20, "bold"), bg="#020617", fg="#38bdf8").pack(pady=30)

        # حاوية الأزرار
        frame = tk.Frame(root, bg="#020617")
        frame.pack(pady=10, padx=20)

        # قائمة الأدوات المربوطة
        self.tools = [
            ("🚛 هوية الشاحنات", "Fakher_Truck_Identity_2600.PY"),
            ("🚗 هوية السيارات", "Fakher_Car_Identity_2600.py"),
            ("⚙️ صيانة الشاحنات", "Truck_Maintenance_2600.py"),
            ("🔧 صيانة السيارات", "Car_Maintenance_2600.py"),
            ("🛡️ الدرع السيادي", "Fakher_Automation_Shield_2600.py"),
            ("🧠 محرك الذكاء", "Fakher_Intelligence_Comparison_2600.py"),
            ("⛽ تحليل الوقود", "Fakher_Car_Fuel_Consumption_2600.py"),
            ("🖨️ محرك الطباعة", "Fakher_Print_Report_Engine_2600.py"),
            ("🔑 مركز التراخيص", "code_generator.py")
        ]

        for i, (name, script) in enumerate(self.tools):
            btn = tk.Button(frame, text=name, width=25, height=2, font=("Segoe UI", 11),
                            bg="#1e293b", fg="white", relief="flat",
                            activebackground="#38bdf8", cursor="hand2",
                            command=lambda s=script: self.launch_script(s))
            btn.grid(row=i//3, column=i%3, padx=10, pady=10)

    def launch_script(self, script_name):
        # البحث عن الملف في نفس المجلد الذي يوجد فيه هذا البرنامج
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        
        if os.path.exists(script_path):
            # تشغيل البرنامج كعملية منفصript_name}\nيرجى وضعه في نفس مجلد برنامج التحكم.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherMasterControl(root)
    root.mainloop()