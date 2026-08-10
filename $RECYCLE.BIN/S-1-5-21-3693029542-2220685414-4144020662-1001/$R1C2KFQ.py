# -*- coding: utf-8 -*-
import tkinter as tk
import subprocess
import os

class FakherDashboard2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🏛️ منظومة فاخر 2600 - واجهة المستقبل")
        self.root.geometry("1200x800")
        self.root.configure(bg="#050505") # خلفية داكنة جداً (Dark Mode)

        # عنوان الواجهة
        tk.Label(root, text="CENTRAL COMMAND 2600", font=("Orbitron", 24, "bold"), 
                 bg="#050505", fg="#00ffcc").pack(pady=20)

        # إطار الأزرار
        self.btn_frame = tk.Frame(root, bg="#050505")
        self.btn_frame.pack(pady=20)

        # تعريف الأدوات مع وصف عملها
        self.tools = [
            ("هوية الشاحنات", "Fakher_Truck_Identity_2600.PY", "إدارة السجلات"),
            ("النفق العالمي", "Fakher_Tunnel.py", "تأمين الاتصال"),
            ("سيرفر الشاحنات", "Fakher_Truck_Server_2600.py", "استقبال البيانات"),
            ("فحص الخزنة", "inspect_db.py", "تحليل القواعد"),
            ("كاشف البيانات", "Fakher_Search_Foretell_2600.py", "AI Scanner"),
            ("المحرك العالمي", "algorithms_engine.py", "النواة الحسابية")
        ]

        # إنشاء مفاتيح بأسلوب "Cyberpunk"
        for i, (name, script, desc) in enumerate(self.tools):
            btn = tk.Button(self.btn_frame, text=f"{name}\n[{desc}]", width=20, height=3,
                            bg="#1a1a1a", fg="#00ffcc", relief="flat",
                            font=("Segoe UI", 10, "bold"),
                            activebackground="#00ffcc", activeforeground="black",
                            command=lambda s=script: self.execute(s))
            btn.grid(row=i//3, column=i%3, padx=15, pady=15)

    def execute(self, script):
        if os.path.exists(script):
            # تشغيل الملف وإظهار رسالة تأكيد
            subprocess.Popen(["python", script])
        el: الملف {script} غير موجود.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherDashboard2600(root)
    root.mainlo1111111