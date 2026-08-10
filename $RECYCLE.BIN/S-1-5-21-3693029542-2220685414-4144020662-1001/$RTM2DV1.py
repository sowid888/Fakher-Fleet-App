# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - درع الأتمتة والمراقبة والتأمين التلقائي
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم المعتمد: Fakher_Automation_Shield_2600
الوصف: محرك حماية الأسطول من التلاعب بالعدادات، والأتمتة الخلفية، والنسخ الاحتياطي المشفر والآلي لحماية البيانات.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
import shutil
from datetime import datetime

DB_PATH = "Fakher_System_2026.db"
BACKUP_DIR = "Fakher_Backups_2600"

class FakherAutomationShield2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ منظومة فاخر 2600 - درع الأتمتة السيادي وحماية الأسطول 🛡️")
        self.root.geometry("1600x850")
        self.root.configure(bg="#020617") # لون داكن وهيب مغلق لغرفة التحكم الحصينة
        
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
            
        self.build_ui()
        self.trigger_auto_backup()
        self.load_security_logs()

    def build_ui(self):
        # 1. شريط الإدارة والسيادة العلوي
        top_bar = tk.Frame(self.root, bg="#1e1b4b", bd=1, relief="solid") # كحلي ملكي
        top_bar.pack(fill="x", padx=15, pady=10)
        
        tk.Label(top_bar, text="🛡️ غرفة المراقبة والتحصين الإلكتروني - الأتمتة الشاملة والنسخ الاحتياطي ومنع التلاعب 2600 🛡️", 
                 font=("Arial", 12, "bold"), bg="#1e1b4b", fg="#fbbf24").pack(side="right", padx=15, pady=15)
        
        # أزرار التحكم السريع بجانب العنوان
        tk.Button(top_bar, text="💾 إنشاء نسخة احتياطية فورية الآن", font=("Arial", 10, "bold"), 
                  bg="#10b981", fg="white", padx=10, command=self.trigger_auto_backup, cursor="hand2").pack(side="left", padx=15, pady=10)

        # حاوية تقسيم الشاشة إلى جناحين عرضيين متناسقين
        main_container = tk.Frame(self.root, bg="#020617")
        main_container.pack(fill="both", expand=True, padx=15, pady=5)

        # ================= الجناح الأيمن: رصد محاولات التلاعب بالعدادات (الأمان الداخلي) =================
        security_frame = tk.LabelFrame(main_container, text=" ⚠️ سجل رصد المخالفات ومحاولات التلاعب بالعدادات (حظر فوري) ", 
                                        font=("Arial", 11, "bold"), bg="#0f172a", fg="#f43f5e", labelanchor="ne")
        security_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        log_cols = ("time", "v_type", "v_id", "driver", "err_desc")
        self.log_tree = ttk.Treeview(security_frame, columns=log_cols, show="headings")
        self.log_tree.heading("time", text="التوقيت واللحظة")
        self.log_tree.heading("v_type", text="نوع المركبة")
        self.log_tree.heading("v_id", text="رقم المركبة")
        self.log_tree.heading("driver", text="السائق / الموزع")
        self.log_tree.heading("err_desc", text="التهديد المرصود والحظر البرمجي")
        
        for col in log_cols:
            self.log_tree.column(col, anchor="center")
        self.log_tree.column("err_desc", width=350)
        self.log_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log_tree.tag_configure("TAMPER", background="#450a0a", foreground="#fca5a5")

        # ================= الجناح الأيسر: إدارة النسخ الاحتياطي والأتمتة (الأمان الخارجي) =================
        backup_frame = tk.LabelFrame(main_container, text=" 🗄️ نظام الاستعادة والنسخ الاحتياطي المؤمّن تلقائياً ", 
                                       font=("Arial", 11, "bold"), bg="#0f172a", fg="#38bdf8", labelanchor="ne")
        backup_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        backup_cols = ("b_name", "b_date", "b_size")
        self.backup_tree = ttk.Treeview(backup_frame, columns=backup_cols, show="headings")
        self.backup_tree.heading("b_name", text="اسم ملف النسخة المعزولة")
        self.backup_tree.heading("b_date", text="تاريخ الحفظ التلقائي")
        self.backup_tree.heading("b_size", text="حجم البيانات المستقرة")
        
        for col in backup_cols:
            self.backup_tree.column(col, anchor="center")
        self.backup_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # شريط الحالة السفلي للأتمتة التلقائية
        self.lbl_status = tk.Label(self.root, text="🟢 المنظومة السيادية تحت الأتمتة الكاملة والمراقبة الخلفية مستمرة لأسطول الـ 100 مركبة...", 
                                   font=("Arial", 10), bg="#020617", fg="#10b981")
        self.lbl_status.pack(side="bottom", anchor="w", padx=20, pady=5)

    def trigger_auto_backup(self):
        """ خوارزمية الحماية الخارجية: عمل نسخة احتياطية من الخزنة المركزية بشكل دوري ومؤرشف """
        if not os.path.exists(DB_PATH):
            return
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_filename = f"Fakher_Backup_2600_{timestamp}.db"
            dest_path = os.path.join(BACKUP_DIR, backup_filename)
            
            # نسخ ملف الخزنة كاملاً إلى المجلد المعزول
            shutil.copy2(DB_PATH, dest_path)
            
            # تحديث شاشة العرض أمام المهندس جمال ليرى الملفات المحفوظة
            self.load_backup_list()
        except Exception as e:
            print(f"Backup Error: {e}")

    def load_backup_list(self):
        """ عرض ملفات النسخ الاحتياطي وحجمها الفعلي للتأكد من استقرار النظام """
        for item in self.backup_tree.get_children():
            self.backup_tree.delete(item)
            
        if not os.path.exists(BACKUP_DIR):
            return
            
        files = sorted(os.listdir(BACKUP_DIR), reverse=True)
        for f in files:
            if f.endswith(".db"):
                f_path = os.path.join(BACKUP_DIR, f)
                f_size = f"{round(os.path.getsize(f_path) / 1024, 2)} KB"
                # استخراج تاريخ التعديل للملف
                f_time = datetime.fromtimestamp(os.path.getmtime(f_path)).strftime("%Y-%m-%d %H:%M:%S")
                self.backup_tree.insert("", "end", values=(f, f_time, f_size))

    def verify_and_intercept_odometer(self, vehicle_id, vehicle_type, driver_name, proposed_odo):
        """ خوارزمية الحظر الداخلي السيادية: اعتراض وفحص قراءات السائقين قبل إعطائهم الضوء الأخضر """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # تفعيل قاعدة بيانات رصد المخالفات إن لم تكن موجودة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Security_Tamper_Logs (
                log_time TEXT,
                v_type TEXT,
                v_id TEXT,
                driver TEXT,
                err_desc TEXT
            )
        """)
        
        current_stored_odo = 0
        table_name = "Truck_Master" if vehicle_type == "Truck" else "Car_Master"
        id_col = "serial_num" if vehicle_type == "Truck" else "admin_num"
        
        try:
            cursor.execute(f"SELECT current_odometer FROM {table_name} WHERE {id_col} = ?", (vehicle_id,))
            row = cursor.fetchone()
            if row:
                current_stored_odo = int(row[0])
        except Exception:
            pass

        # 1. شرط فحص التراجع (العداد المدخل أقل من المخزن بالخزنة)
        if proposed_odo < current_stored_odo:
            log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            err_desc = f"🚨 محاولة تلاعب تراجعي! العداد الحالي بالخزنة ({current_stored_odo}) والمدخل ({proposed_odo})"
            cursor.execute("INSERT INTO Security_Tamper_Logs VALUES (?, ?, ?, ?, ?)", (log_time, vehicle_type, vehicle_id, driver_name, err_desc))
            conn.commit()
            conn.close()
            self.load_security_logs()
            return False # إرجاع رفض المعاملة وحظرها فورا لحماية النظام

        # 2. شرط فحص القفزة الجنونية الوهمية (أكثر من 2000 كم أو ميل في يوم واحد كحد أقصى مسموح به)
        if (proposed_odo - current_stored_odo) > 2000 and current_stored_odo > 0:
            log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            err_desc = f"❌ قفزة وهمية جنونية بالعداد! الفارق المكتوب ({proposed_odo - current_stored_odo}) يتجاوز المنطق اليومي"
            cursor.execute("INSERT INTO Security_Tamper_Logs VALUES (?, ?, ?, ?, ?)", (log_time, vehicle_type, vehicle_id, driver_name, err_desc))
            conn.commit()
            conn.close()
            self.load_security_logs()
            return False

        conn.close()
        return True # المعاملة آمنة، يُسمح للمدير بإعطاء الضوء الأخضر والمصادقة

    def load_security_logs(self):
        """ جلب سجلات الحظر والتلاعب من قاعدة البيانات وعرضها فوراً في الجناح الأيمن """
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT log_time, v_type, v_id, driver, err_desc FROM Security_Tamper_Logs ORDER BY log_time DESC")
            for row in cursor.fetchall():
                self.log_tree.insert("", "end", values=row, tags=("TAMPER",))
        except Exception:
            pass
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherAutomationShield2600(root)
    root.mainloop()