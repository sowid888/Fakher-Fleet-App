# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - محرك التذكيرات الفني وجدولة الإنذارات
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم المعتمد للملف: Truck_Maintenance_2600.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "Fakher_Central_Database_2600.db" # تم توحيد المسار مع كود الهوية

class FakherAlertEngine2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🚨 منظومة فاخر 2600 - محرك فحص وفصل التذكيرات والإنذارات الفورية 🚨")
        self.root.geometry("1500x800")
        self.root.configure(bg="#020617")
        
        self.build_ui()
        self.run_fleet_inspection()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#1e1b4b", height=70)
        header.pack(fill="x", padx=10, pady=10)
        tk.Label(header, text="🚨 لوحة المراقبة والإنذارات الفنية للشاحنات - مطابقة وفصل الميل والكيلو تلقائياً 🚨", 
                 font=("Arial", 14, "bold"), bg="#1e1b4b", fg="#ef4444").pack(pady=20)

        # زر المسح الفوري المربوط بالخزنة المشتركة
        tk.Button(self.root, text="🔄 تشغيل خوارزمية الفحص والمسح الشامل للأسطول الآن من قاعدة البيانات المشتركة", font=("Arial", 11, "bold"), 
                  bg="#10b981", fg="white", command=self.run_fleet_inspection, cursor="hand2").pack(fill="x", padx=20, pady=5)

        grid_frame = tk.Frame(self.root, bg="#020617")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=15)

        cols = ("v_type", "v_id", "driver", "rule_name", "current_val", "limit_val", "status")
        self.tree = ttk.Treeview(grid_frame, columns=cols, show="headings")
        
        self.tree.heading("v_type", text="نوع المركبة")
        self.tree.heading("v_id", text="رقم التعميد / التسلسلي")
        self.tree.heading("driver", text="السائق / المستلم")
        self.tree.heading("rule_name", text="البند الفني المستحق")
        self.tree.heading("current_val", text="العداد الحالي للمركبة")
        self.tree.heading("limit_val", text="الحد القانوني المسموح")
        self.tree.heading("status", text="مستوى الخطورة والإلحاح")

        for col in cols:
            self.tree.column(col, anchor="center")
        self.tree.column("rule_name", width=250)
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("CRITICAL", background="#450a0a", foreground="#fca5a5") 
        self.tree.tag_configure("WARNING", background="#1c1917", foreground="#fde047")  

    def run_fleet_inspection(self):
        """ قراءة وفحص قراءات العداد الحية من جدول الهوية المشترك لإصدار الإنذارات """
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # فحص قطاع الشاحنات من الجدول السيادي الموحد
            cursor.execute("SELECT serial_num, driver_name, current_odometer, unit_type FROM Truck_Main_Registry_2600")
            for s_num, driver, odo, unit in cursor.fetchall():
                odo_val = int(odo or 0)
                limit = 5000 # الحد الافتراضي لصيانة المحرك
                unit_label = "ميل" if unit == "Mile" else "كم"
                
                if odo_val >= limit:
                    self.tree.insert("", "end", values=("شاحنة 🚚", s_num, driver or "غير معين", "تغيير زيت المحرك الأساسي", f"{odo_val} {unit_label}", f"{limit} {unit_label}", "🚨 خطر حرج جداً!"), tags=("CRITICAL",))
                elif odo_val >= (limit - 500):
                    self.tree.insert("", "end", values=("شاحنة 🚚", s_num, driver or "غير معين", "اقتراب موعد صيانة المحرك", f"{odo_val} {unit_label}", f"{limit} {unit_label}", "⚠️ تنبيه قريب"), tags=("WARNING",))
                    
            conn.close()
        except Exception as e:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherAlertEngine2600(root)
    root.mainloop()