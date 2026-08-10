# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية 2600 - الإصدار الاستراتيجي الموسع
المشرف الفني العام الأعلى: المهندس جمال سويد (أبا عبد الله)
"""

import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class FakherAutomationShield2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🏛️ مركز القيادة والتحكم السيادي لأسطول فاخر 2600 🏛️")
        self.root.geometry("1650x900")
        self.root.configure(bg="#020617")
        self.root.state('zoomed')
        
        self.target_dir = "C:/Fakher_System"
        self.db_truck = os.path.join(self.target_dir, "Fakher_Central_Database_2600.db")
        self.db_car = os.path.join(self.target_dir, "Fakher_System_2026.db")
        
        self.build_ui()
        self.refresh_fleet_data()

    def build_ui(self):
        # الهيدر
        header = tk.Frame(self.root, bg="#1e1b4b", height=80)
        header.pack(fill="x")
        tk.Label(header, text="🏛️ لوحة التحكم السيادية - إدارة الأسطول الموحدة 🏛️", font=("Arial", 20, "bold"), bg="#1e1b4b", fg="#38bdf8").pack(pady=15)

        # منطقة الجدول
        self.tree = ttk.Treeview(self.root, columns=("Type", "Driver", "Plate", "Odo", "Status"), show="headings")
        self.tree.heading("Type", text="نوع المركبة")
        self.tree.heading("Driver", text="السائق")
        self.tree.heading("Plate", text="اللوحة")
        self.tree.heading("Odo", text="العداد")
        self.tree.heading("Status", text="الحالة الفنية")
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        
        # زر الإجراء
        btn_frame = tk.Frame(self.root, bg="#020617")
        btn_frame.pack(fill="x", padx=20, pady=10)
        tk.Button(btn_frame, text="🔍 كشف تفاصيل المركبة المختارة", font=("Arial", 12, "bold"), bg="#0ea5e9", fg="white", command=self.show_details).pack(side="left")

    def refresh_fleet_data(self):
        """ جلب كل البيانات من قاعدة بيانات الشاحنات والسيارات ودمجها في لوحة واحدة """
        for i in self.tree.get_children(): self.tree.delete(i)
        
        # جلب الشاحنات
        if os.path.exists(self.db_truck):
            conn = sqlite3.connect(self.db_truck)
            cursor = conn.cursor()
            cursor.execute("SELECT 'شاحنة', driver_name, plate_num, current_odometer FROM Truck_Main_Registry_2600")
            for row in cursor.fetchall(): self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], "مؤمنة"))
            conn.close()
            
        # جلب السيارات
        if os.path.exists(self.db_car):
            conn = sqlite3.connect(self.db_car)
            cursor = conn.cursor()
            cursor.execute("SELECT 'سيارة', driver_name, plate_num, current_odometer FROM Car_Master")
            for row in cursor.fetchall(): self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], "مؤمنة"))
            conn.close()

    def show_details(self):
        """ عرض تفاصيل المركبة عند اختيارها """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "يرجى اختيار مركبة من الجدول أولاً!")
            return
        
        item = self.tree.item(selected[0])
        driver = item['values'][1]
        messagebox.showinfo("تفاصيل المركبة"
if __name__ == "__main__":
    root = tk.Tk()
    app = FakherAutomationShield2600(root)
    root.mainloop()