# -*- coding: utf-8 -*-
"""
منظومة النافذة الموحدة 2600 - المشغل المركزي السيادي الشامل لكافة الملفات الـ 13
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد: Fakher_Master_Gateway_2600.py
التحديث: ضغط وتوسيع الواجهة هندسياً لتظهر كافة المفاتيح في الشاشة فوراً دون نزول.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
import os
import subprocess
import sys

class FakherMasterGateway2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ مـنـظـومـة الـنـافـذة الـمـوحـدة 2600 🛡️")
        self.root.geometry("1400x850")
        self.root.state('zoomed') 
        self.root.configure(bg="#0b1329") 
        
        self.system_password = "2600"
        self.is_whatsapp_locked = False
        self.active_processes = {}
        
        self.build_framework_ui()

    def build_framework_ui(self):
        # ==================== 1. الشريط العلوي الرئاسي الفخم ====================
        header = tk.Frame(self.root, bg="#1c2541", pady=8, bd=2, relief="groove")
        header.pack(fill="x", padx=12, pady=5)
        
        title_lbl = tk.Label(header, text="🛡️ مـنـظـومـة الـنـافـذة الـمـوحـدة 2600 - الـمـشـغـل الـمـركـزي الـشـامـل 🛡️", 
                             font=("Arial", 18, "bold"), bg="#1c2541", fg="#38bdf8")
        title_lbl.pack()
        
        sub_title = tk.Label(header, text="المشرف الفني العام: المهندس جمال سويد (أبا عبد الله) - لوحة التحكم المطلقة بملفات المنظومة الـ 13 كاملاً", 
                             font=("Arial", 10, "italic"), bg="#1c2541", fg="#94a3b8")
        sub_title.pack(pady=2)

        # ==================== 2. حقل هاتف واتساب البرنامج المعتمد ====================
        whatsapp_frame = tk.LabelFrame(self.root, text=" 📱 إعدادات وحماية هاتف واتساب البرنامج المركزي ", 
                                       font=("Arial", 10, "bold"), bg="#111c44", fg="#facc15", labelanchor="ne", padx=15, pady=4)
        whatsapp_frame.pack(fill="x", padx=12, pady=2)
        
        self.btn_lock_whatsapp = tk.Button(whatsapp_frame, text="🔒 قفل وحفظ الرقم", font=("Arial", 10, "bold"), bg="#dc2626", fg="white",
                                           padx=10, pady=1, cursor="hand2", command=self.toggle_whatsapp_lock)
        self.btn_lock_whatsapp.pack(side="left", padx=5)
        
        self.txt_system_whatsapp = tk.Entry(whatsapp_frame, font=("Arial", 12, "bold"), width=22, justify="center", bg="#1e293b", fg="#38bdf8", insertbackground="white")
        self.txt_system_whatsapp.pack(side="right", padx=10)
        self.txt_system_whatsapp.insert(0, "77XXXXXXX")
        
        tk.Label(whatsapp_frame, text="رقم هاتف واتساب البرنامج المركزي:", font=("Arial", 10, "bold"), bg="#111c44", fg="white").pack(side="right", padx=3)

        # ==================== 3. حاوية شبكة المفاتيح الكاملة (تم تقليص الارتفاع هندسياً) ====================
        main_container = tk.Frame(self.root, bg="#0b1329")
        main_container.pack(fill="both", expand=True, padx=12, pady=2)

        # --- المجموعة الأولى: تعريف وتسجيل الهوية ---
        group_id = tk.LabelFrame(main_container, text=" 🗂️ 1. مفاتيح تسجيل وتعريف هوية المركبات ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#a5f3fc", labelanchor="ne", padx=8, pady=4)
        group_id.pack(fill="x", pady=2)
        self.create_macro_button(group_id, "🚚 تشغيل مفتاح هوية شاحنة جديدة", ["Fakher_Truck_Identity_2600.py", "Truck_Identity_2600.py"], "#0284c7").pack(side="right", expand=True, fill="x", padx=5)
        self.create_macro_button(group_id, "🚗 تشغيل مفتاح هوية سيارة جديدة", ["Fakher_Car_Identity_2600.py", "Car_Identity_2600.py"], "#4f46e5").pack(side="right", expand=True, fill="x", padx=5)

        # --- المجموعة الثانية: حركات صرف الديزل والوقود اليومي ---
        group_fuel = tk.LabelFrame(main_container, text=" ⛽ 2. مفاتيح حركات صرف الديزل والوقود ومراقبة الاستهلاك ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#a5f3fc", labelanchor="ne", padx=8, pady=4)
        group_fuel.pack(fill="x", pady=2)
        self.create_macro_button(group_fuel, "⛽ تشغيل سجل صرف ديزل الشاحنات", ["Fakher_Truck_Diesel_2600.py", "Truck_Diesel_2600.py"], "#b45309").pack(side="right", expand=True, fill="x", padx=5)
        self.create_macro_button(group_fuel, "⛽ تشغيل سجل استهلاك وقود السيارات", ["Fakher_Car_Fuel_Consumption_2600.py", "Fakher_Car_Fuel_2600.py"], "#d97706").pack(side="right", expand=True, fill="x", padx=5)

        # --- المجموعة الثالثة: سجلات الصيانة الفنية الدورية ---
        group_maintenance = tk.LabelFrame(main_container, text=" 🔧 3. مفاتيح سجلات الصيانة الفنية والزيوت والفلاتر ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#a5f3fc", labelanchor="ne", padx=8, pady=4)
        group_maintenance.pack(fill="x", pady=2)
        self.create_macro_button(group_maintenance, "🛠️ تشغيل سجل الصيانة الفني للشاحنات", ["Fakher_Truck_Maintenance_Log_2600.py", "Truck_Maintenance_Log_2600.py"], "#2563eb").pack(side="right", expand=True, fill="x", padx=5)
        self.create_macro_button(group_maintenance, "🛠️ تشغيل سجل صيانة وإصلاح السيارات", ["Fakher_Car_Maintenance_Log_2600.py", "Car_Maintenance_Log_2600.py"], "#3b82f6").pack(side="right", expand=True, fill="x", padx=5)

        # --- المجموعة الرابعة: بوابات واتساب السائقين والربط الآلي ---
        group_whatsapp = tk.LabelFrame(main_container, text=" 📥 4. مفاتيح استقبال ومعالجة واتساب السائقين (الميداني) ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#a5f3fc", labelanchor="ne", padx=8, pady=4)
        group_whatsapp.pack(fill="x", pady=2)
        self.create_macro_button(group_whatsapp, "📲 معالج واتساب سائقين الشاحنات", ["Fakher_Driver_WhatsApp_2600.py", "Driver_WhatsApp_2600.py"], "#16a34a").pack(side="right", expand=True, fill="x", padx=5)
        self.create_macro_button(group_whatsapp, "📲 معالج واتساب سائقين السيارات", ["Fakher_Car_Driver_WhatsApp_2600.py", "Car_Driver_WhatsApp_2600.py"], "#0d9488").pack(side="right", expand=True, fill="x", padx=5)

        # --- المجموعة الخامسة: الحسابات، التذكيرات، والذكاء التحليلي (ارتفعت لأعلى الشاشة الآن!) ---
        group_logic = tk.LabelFrame(main_container, text=" ⚙️ 5. مفاتيح المعادلات، التذكيرات، والمقارنات والتحليل الفني ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#a5f3fc", labelanchor="ne", padx=8, pady=4)
        group_logic.pack(fill="x", pady=2)
        self.create_macro_button(group_logic, "🧮 مفتاح المعادلات الحسابية للمسافات", ["Fakher_Dynamic_Equations_2600.py", "Dynamic_Equations_2600.py"], "#4b5563").pack(side="right", expand=True, fill="x", padx=4)
        self.create_macro_button(group_logic, "⏰ مفتاح التذكيرات وجدول الصيانة", ["Fakher_Maintenance_Alert_Engine_2600.py", "Maintenance_Alert_Engine_2600.py"], "#dc2626").pack(side="right", expand=True, fill="x", padx=4)
        self.create_macro_button(group_logic, "⚖️ مفتاح المقارنات والتحليل الفني", ["Fakher_Intelligence_Comparison_2600.py", "Intelligence_Comparison_2600.py"], "#6d28d9").pack(side="right", expand=True, fill="x", padx=4)

        # --- المجموعة السادسة: التقارير وصندوق البريد المركزي الشامل ---
        group_reports = tk.LabelFrame(main_container, text=" 📬 6. بوابات التقارير والطباعة وصندوق البريد المركزي الشامل ", font=("Arial", 11, "bold"), bg="#111c44", fg="#facc15", labelanchor="ne", padx=8, pady=4)
        group_reports.pack(fill="x", pady=4)
        self.create_macro_button(group_reports, "🖨️ محرك تقارير الطباعة وسندات الصرف", ["Fakher_Print_Report_Engine_2600.py", "Print_Report_Engine_2600.py"], "#059669").pack(side="right", expand=True, fill="x", padx=5)
        self.create_macro_button(group_reports, "📬 فتح صندوق البريد والدرع الرقمي", ["Fakher_Automation_Shield_2600.py", "Automation_Shield_2600.py"], "#7c3aed").pack(side="right", expand=True, fill="x", padx=5)

        # ==================== 4. شريط الحالة السفلي ====================
        footer = tk.Frame(self.root, bg="#1c2541", pady=4)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="⚙️ منظومة النافذة الموحدة 2600 - لوحة المايسترو الشاملة لكافة الأكواد الـ 13 تحت إشراف المهندس جمال سويد ⚙️", 
                 font=("Arial", 9, "bold"), bg="#1c2541", fg="#a5f3fc").pack()

    def create_macro_button(self, parent, text, script_names, bg_color):
        # تم تعديل حجم الخط والبادئ ليكون 13 فخم ومضغوط هندسياً ليتطابق مع أبعاد الشاشة بدون نزول
        btn = tk.Button(parent, text=text, font=("Arial", 13, "bold"), bg=bg_color, fg="white",
                        activebackground="#ffffff", activeforeground=bg_color, cursor="hand2", pady=6, bd=2, relief="raised",
                        command=lambda: self.execute_sub_script(script_names))
        return btn

    def toggle_whatsapp_lock(self):
        if not self.is_whatsapp_locked:
            pwd = simpledialog.askstring("حماية النظام الموحد", "🔒 يرجى إدخال الرقم السري لتأمين وحفظ هاتف واتساب البرنامج:", show='*')
            if pwd == self.system_password:
                self.is_whatsapp_locked = True
                self.txt_system_whatsapp.configure(state='disabled', disabledbackground="#16a34a", disabledforeground="white")
                self.btn_lock_whatsapp.configure(text="🔓 فك قفل التعديل", bg="#eab308")
                messagebox.showinfo("أمان المنظومة", "✅ تم حفظ وتأمين رقم واتساب المنظومة بنجاح!")
            else:
                messagebox.showerror("خطأ في القفل", "❌ الرقم السري غير صحيح! تم رفض عملية التعديل.")
        else:
            pwd = simpledialog.askstring("حماية النظام الموحد", "🔓 لفك القفل والسماح باستبدال الرقم، أدخل الرقم السري:", show='*')
            if pwd == self.system_password:
                self.is_whatsapp_locked = False
                self.txt_system_whatsapp.configure(state='normal', bg="#1e293b", fg="#38bdf8")
                self.btn_lock_whatsapp.configure(text="🔒 قفل وحفظ الرقم", bg="#dc2626")
                messagebox.showinfo("أمان المنظومة", "🔓 تم فك قفل الحقل بنجاح، يمكنك التعديل الآن.")
            else:
                messagebox.showerror("خطأ في فك القفل", "❌ الرمز السري خاطئ!")

    def get_formatted_whatsapp(self):
        if self.is_whatsapp_locked:
            self.txt_system_whatsapp.configure(state='normal')
            raw_num = self.txt_system_whatsapp.get().strip()
            self.txt_system_whatsapp.configure(state='disabled')
        else:
            raw_num = self.txt_system_whatsapp.get().strip()
        cleaned = raw_num.lstrip('0').lstrip('+')
        return f"+{cleaned}" if cleaned.startswith('967') else f"+967{cleaned}"

    def execute_sub_script(self, script_names):
        primary_name = script_names[0]
        if primary_name in self.active_processes:
            poll = self.active_processes[primary_name].poll()
            if poll is None:
                messagebox.showwarning("تنبيه أمان المنظومة 2600", "⚠️ هذه الصفحة مفتوحة مسبقاً وتعمل حالياً!")
                return

        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_script_path = None
        for name in script_names:
            paths_to_check = [os.path.join("D:\\", name), os.path.join(current_dir, name)]
            for p in paths_to_check:
                if os.path.exists(p):
                    full_script_path = p
                    break
            if full_script_path: break

        if not full_script_path:
            messagebox.showwarning("تنبيه أمان المنظومة", f"⚠️ لم يتم العثور على ملف [{primary_name}] في جهازك بالقرص D.")
            return
        
        try:
            whatsapp_number = self.get_formatted_whatsapp()
            env = os.environ.copy()
            process = subprocess.Popen([sys.executable, full_script_path, whatsapp_number], env=env)
            self.active_processes[primary_name] = process
        except Exception as e:
            messagebox.showerror("خطأ في التشغيل", f"❌ تعذر تشغيل الملف.\nالسبب: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherMasterGateway2600(root)
    root.mainloop()