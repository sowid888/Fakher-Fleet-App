# -*- coding: utf-8 -*-
"""
منظومة السَّد الفني 2600 - المشغل المركزي السيادي الشامل للملفات الـ 13
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد للحفظ: Fakher_Master_Gateway_2600.py
"""

import tkinter as tk
from tkinter import messagebox, ttk
import os
import subprocess

class FakherMasterGateway2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ منظومة السَّد الفني 2600 - الواجهة المركزية السيادية 🛡️")
        self.root.geometry("1300 import")
        self.root.state('zoomed') # ملء الشاشة بالكامل فور التشغيل
        self.root.configure(bg="#0b1329") # اللون الملكي المحمي
        
        # بناء عناصر الواجهة الرئاسية للبرنامج
        self.build_framework_ui()

    def build_framework_ui(self):
        # ==================== 1. الشريط العلوي الرئاسي الفخم ====================
        header = tk.Frame(self.root, bg="#1c2541", pady=15, bd=3, relief="groove")
        header.pack(fill="x", padx=15, pady=10)
        
        title_lbl = tk.Label(header, text="🛡️ مـنـظـومـة السَّـد الـفـنـي 2600 - الـمـشـغـل الـمـركـزي الـشـامـل 🛡️", 
                             font=("Arial", 18, "bold"), bg="#1c2541", fg="#38bdf8")
        title_lbl.pack()
        
        sub_title = tk.Label(header, text="المشرف الفني العام: المهندس جمال سويد (أبا عبد الله) - بوابة التحكم بملفات المنظومة الـ 13", 
                             font=("Arial", 11, "italic"), bg="#1c2541", fg="#94a3b8")
        sub_title.pack(pady=4)

        # ==================== 2. حقل هاتف واتساب البرنامج المعتمد (أعلى الواجهة) ====================
        whatsapp_frame = tk.LabelFrame(self.root, text=" 📱 إعدادات هاتف واتساب البرنامج المركزي ", 
                                       font=("Arial", 12, "bold"), bg="#111c44", fg="#facc15", labelanchor="ne", padx=20, pady=10)
        whatsapp_frame.pack(fill="x", padx=15, pady=5)
        
        # حقل الإدخال
        self.txt_system_whatsapp = tk.Entry(whatsapp_frame, font=("Arial", 14, "bold"), width=30, justify="center", bg="#1e293b", fg="#38bdf8", insertbackground="white")
        self.txt_system_whatsapp.pack(side="right", padx=15)
        self.txt_system_whatsapp.insert(0, "77XXXXXXX")
        
        tk.Label(whatsapp_frame, text="رقم هاتف واتساب البرنامج (المعالج التلقائي يضيف كود اليمن +967 في الخلفية):", 
                 font=("Arial", 11, "bold"), bg="#111c44", fg="white").pack(side="right", padx=5)

        # ==================== 3. شبكة المفاتيح والأزرار التنفيذية للملفات الـ 13 ====================
        grid_frame = tk.Frame(self.root, bg="#0b1329")
        grid_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # تكوين وتوزيع الأزرار هندسياً على شكل مجموعات واضحة
        
        # المجموعة الأولى: تعريف وتسجيل الهوية
        group_id = tk.LabelFrame(grid_frame, text=" 🗂️ مفاتيح تسجيل وتعريف هوية المركبات ", font=("Arial", 12, "bold"), bg="#1e293b", fg="#a5f3fc", labelanchor="ne", padx=10, pady=10)
        group_id.pack(fill="x", pady=5)
        
        self.create_macro_button(group_id, "🚚 تشغيل مفتاح هوية شاحنة جديدة", "Truck_Identity_2600.py", "#0284c7").pack(side="right", expand=True, fill="x", padx=10)
        self.create_macro_button(group_id, "🚗 تشغيل مفتاح هوية سيارة جديدة", "Car_Identity_2600.py", "#4f46e5").pack(side="right", expand=True, fill="x", padx=10)

        # المجموعة الثانية: بوابات معالجة واستقبال واتساب السائقين الميدانيين
        group_whatsapp = tk.LabelFrame(grid_frame, text=" 📥 مفاتيح استقبال ومعالجة واتساب السائقين (ربط آلي) ", font=("Arial", 12, "bold"), bg="#1e293b", fg="#a5f3fc", labelanchor="ne", padx=10, pady=10)
        group_whatsapp.pack(fill="x", pady=5)
        
        self.create_macro_button(group_whatsapp, "📲 معالج واتساب سائقين الشاحنات", "Truck_Drivers_WhatsApp_2600.py", "#16a34a").pack(side="right", expand=True, fill="x", padx=10)
        self.create_macro_button(group_whatsapp, "📲 معالج واتساب سائقين السيارات", "Car_Drivers_WhatsApp_2600.py", "#0d9488").pack(side="right", expand=True, fill="x", padx=10)

        # المجموعة الثالثة: الحسابات، المعادلات، والتذكيرات الفنية الفورية
        group_logic = tk.LabelFrame(grid_frame, text=" ⚙️ مفاتيح المعادلات، التذكيرات، والمقارنات الفنية ", font=("Arial", 12, "bold"), bg="#1e293b", fg="#a5f3fc", labelanchor="ne", padx=10, pady=10)
        group_logic.pack(fill="x", pady=5)
        
        self.create_macro_button(group_logic, "🧮 مفتاح المعادلات الحسابية للمسافات", "Distance_Equations_2600.py", "#b45309").pack(side="right", expand=True, fill="x", padx=5)
        self.create_macro_button(group_logic, "⏰ مفتاح التذكيرات الدورية وجدول الصيانة", "Maintenance_Alerts_2600.py", "#dc2626").pack(side="right", expand=True, fill="x", padx=5)
        self.create_macro_button(group_logic, "⚖️ مفتاح المقارنات والتحليل الفني للاستهلاك", "Consumption_Comparisons_2600.py", "#2563eb").pack(side="right", expand=True, fill="x", padx=5)

        # المجموعة الرابعة: النواة والمستودع البريدي المركزي
        group_mailbox = tk.LabelFrame(grid_frame, text=" 📬 مستودع صندوق البريد المركزي الشامل (الملخص الفوري) ", font=("Arial", 12, "bold"), bg="#111c44", fg="#facc15", labelanchor="ne", padx=10, pady=10)
        group_mailbox.pack(fill="x", pady=10)
        
        self.create_macro_button(group_mailbox, "📬 فتح صندوق البريد المركزي (وصول التذكيرات والأعمال والتقارير الفورية)", "Central_Mailbox_2600.py", "#7c3aed").pack(fill="x", padx=20, pady=5)

        # ==================== 4. شريط الحالة السفلي ====================
        footer = tk.Frame(self.root, bg="#1c2541", pady=8)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="⚙️ منظومة السَّد الفني 2600 - لوحة المايسترو الرابطة للأكواد الـ 13 تحت إشراف المهندس جمال سويد ⚙️", 
                 font=("Arial", 10, "bold"), bg="#1c2541", fg="#a5f3fc").pack()

    def create_macro_button(self, parent, text, script_name, bg_color):
        """إنشاء زر تنفيذي يقوم باستدعاء الملف المستقل فور النقر عليه"""
        btn = tk.Button(parent, text=text, font=("Arial", 12, "bold"), bg=bg_color, fg="white",
                        activebackground="#ffffff", activeforeground=bg_color, cursor="hand2", pady=8, bd=2, relief="raised",
                        command=lambda: self.execute_sub_script(script_name))
        return btn

    def get_formatted_whatsapp(self):
        """معالجة رقم واتساب البرنامج وتأكيد إضافة مفتاح اليمن تلقائياً في الخلفية قبل التمرير للأكواد"""
        raw_num = self.txt_system_whatsapp.get().strip()
        cleaned = raw_num.lstrip('0').lstrip('+')
        if cleaned.startswith('967'):
            return f"+{cleaned}"
        else:
            return f"+967{clean3516ed}"
