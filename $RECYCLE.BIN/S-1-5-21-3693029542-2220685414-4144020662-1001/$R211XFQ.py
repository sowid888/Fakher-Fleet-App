# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - بوابة التحكم المركزية والنافذة الموحدة
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد: Fakher_Master_Gateway_2600.py
الوظيفة: شاشة التحكم الرئاسية الموحدة المحمية من حلقة التكرار عند التحويل لملف تنفيذي.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys

class FakherMasterGateway:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ مـنـظـومـة الـنـافـذة الـمـوحـدة الـسـيـاديـة الـكـبـرى 2600 🛡️")
        self.root.geometry("900x650")
        self.root.configure(bg="#0b1329")
        
        self.whatsapp_central_phone = "+96777XXXXXXX" # الرقم المركزي للمشرف العام جمال سويد
        self.create_sovereign_header()
        self.create_control_buttons()

    def create_sovereign_header(self):
        header = tk.Frame(self.root, bg="#1c2541", pady=15, bd=3, relief="ridge")
        header.pack(fill="x", padx=20, pady=15)
        
        tk.Label(header, text="⚙️ مـنـظـومـة الـنـافـذة الـمـوحـدة الـتـقـنـيـة الـعـلـيـا 2600 ⚙️", 
                 font=("Arial", 18, "bold"), bg="#1c2541", fg="#38bdf8").pack()
        tk.Label(header, text="المشرف الفني العام: المهندس جمال سويد (أبا عبد الله) - شاشة التحكم والربط المركزي الموحد", 
                 font=("Arial", 11, "italic"), bg="#1c2541", fg="#94a3b8").pack(pady=4)

    def create_control_buttons(self):
        grid_frame = tk.Frame(self.root, bg="#0b1329")
        grid_frame.pack(fill="both", expand=True, padx=40, pady=10)
        
        # الزر الأول والأهم: مستشار استهلاك وقود السيارات والذكاء الاصطناعي
        btn_fuel = tk.Button(grid_frame, text="📊 حركة صرف وقود السيارات ومراقبة الهدر الفوري الـ AI", 
                             font=("Arial", 13, "bold"), bg="#2563eb", fg="white", bd=3, height=2,
                             command=self.launch_fuel_consumption_system)
        btn_fuel.pack(fill="x", pady=10)

        # أزرار فرعية لمحاكاة بقية أقسام النافذة الموحدة الفاخرة
        buttons_info = [
            ("🚚 إدارة ملفات هوية الشاحنات والسيارات المعتمدة 2600", "#1e293b"),
            ("🛠️ منظومة التنبيهات والصيانة الدورية وجداول المسافات", "#1e293b"),
            ("📡 نظام الربط السحابي والمطابقة الفورية للمصنع", "#1e293b")
        ]
        
        for text, color in buttons_info:
            btn = tk.Button(grid_frame, text=text, font=("Arial", 12, "bold"), bg=color, fg="#94a3b8", bd=2, height=2, state="disabled")
            btn.pack(fill="x", pady=6)
            
        # شريط الحالة السفلي الرئاسي للمنظومة
        lbl_status = tk.Label(self.root, text="📡 حالة المنظومة الموحدة: جاهزة ومستقرة تحت إشراف المهندس جمال سويد", font=("Arial", 10, "bold"), bg="#1c2541", fg="#a5f3fc", pady=4)
        lbl_status.pack(fill="x", side="bottom")

    def launch_fuel_consumption_system(self):
        """استدعاء وتشغيل ملف وقود السيارات الذكي بدقة وبدون تكرار الواجهة"""
        # تحديد مجلد التشغيل الفعلي لمنع فتح نافذة الماستر مرتين بالخطأ
        current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        script_path = os.path.join(current_dir, "Fakher_Car_Fuel_Consumption_2600.py")
        
        if os.path.exists(script_path):
            try:
                # تشغيل ملف وقود السيارات بشكل مستقل وآمن تماماً عبر نظام الويندوز
                os.startfile(script_path)
            except Exception:
                try:
                    os.system(f'python "{script_path}" "{self.whatsapp_central_phone}" &')
                except Exception as e:
                    messagebox.showerror("خطأ في التشغيل", f"تعذر تشغيل ملف الوقود: {str(e)}")
        else:
            # محاولة أخيرة للبحث عنه بالاسم المجرد في حال اختلف مكان التشغيل الداخلي للـ EXE
            if os.path.exists("Fakher_Car_Fuel_Consumption_2600.py"):
                os.startfile("Fakher_Car_Fuel_Consumption_2600.py")
            else:
                messagebox.showerror("ملف مفقود", f"🚨 خطأ: يرجى التأكد من وجود ملف [Fakher_Car_Fuel_Consumption_2600.py] بجانب هذا البرنامج الفخم في نفس المجلد!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherMasterGateway(root)
    root.mainloop()