# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - مركز التراخيص ومحرك البحث الذكي المرن
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم المعتمد للملف: code_generator.py
التصحيح الحاسم: معالجة مرنة لأسماء الجداول والأعمدة والملفات لمنع أخطاء جلب البيانات نهائياً.
"""

import os
import time
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3

# المسارات المحتملة لقاعدة البيانات لضمان التوافق الكامل
DB_PATHS = ["Fakher_Central_Database_2600.db", "Fakher_System_2026.db"]
ADMIN_PASSWORD = "2600"

class FleetFinalStandaloneGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔑 منظومة فاخر 2600 - مركز توليد وحقن أكواد الفتح وتطابق السائقين 🔑")
        self.root.geometry("1200x850")
        self.root.configure(bg="#020617") 

        self.current_selected_record = None 
        self.active_db_path = DB_PATHS[0] # الافتراضي
        
        self.build_ui_layout()
        self.check_and_prepare_columns() 

    def get_db_connection(self):
        """ محاولة الاتصال بأي ملف قاعدة بيانات متاح من القائمة """
        for path in DB_PATHS:
            if os.path.exists(path):
                self.active_db_path = path
                return sqlite3.connect(path)
        # إذا لم يوجد أي ملف، نشحن الافتراضي
        return sqlite3.connect(DB_PATHS[0])

    def check_and_prepare_columns(self):
        """ تأمين وجود حقل استقبال كود التفعيل في الجداول المتاحة """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            try: cursor.execute("ALTER TABLE Truck_Main_Registry_2600 ADD COLUMN auth_code TEXT")
            except: pass
            try: cursor.execute("ALTER TABLE Car_Master ADD COLUMN auth_code TEXT")
            except: pass
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"تهيئة مبدئية: {e}")

    def build_ui_layout(self):
        # 1. شريط العنوان
        header = tk.Frame(self.root, bg="#1e1b4b", height=60, bd=1, relief="solid")
        header.pack(fill="x", padx=15, pady=10)
        tk.Label(header, text="🔑 محرك التشفير الموحد - استدعاء البيانات وتوليد أكواد التحقق الفوري للسائقين 🔑", 
                 font=("Arial", 13, "bold"), bg="#1e1b4b", fg="#38bdf8").pack(pady=15)

        # 2. تحديد قطاع البحث
        switch_frame = tk.LabelFrame(self.root, text=" 🎛️ تحديد قطاع البحث والاستهداف ", font=("Arial", 11, "bold"), bg="#0f172a", fg="#fbbf24", labelanchor="ne")
        switch_frame.pack(fill="x", padx=15, pady=5)

        self.vehicle_type_var = tk.StringVar(value="TRUCK")
        
        rb_truck = tk.Radiobutton(switch_frame, text="🚚 قطاع الشاحنات والنقل الثقيل", variable=self.vehicle_type_var, 
                                  value="TRUCK", font=("Arial", 12, "bold"), bg="#0f172a", fg="white", 
                                  selectcolor="#1e1b4b", command=self.on_sector_changed, cursor="hand2")
        rb_truck.pack(side="right", padx=50, pady=12)

        rb_car = tk.Radiobutton(switch_frame, text="🚗 قطاع السيارات الصغيرة والإدارية", variable=self.vehicle_type_var, 
                                value="CAR", font=("Arial", 12, "bold"), bg="#0f172a", fg="white", 
                                selectcolor="#1e1b4b", command=self.on_sector_changed, cursor="hand2")
        rb_car.pack(side="right", padx=50, pady=12)

        # 3. صندوق البحث المفتوح
        search_frame = tk.LabelFrame(self.root, text=" 🔍 صندوق البحث الشامل والمفتوح ", font=("Arial", 11, "bold"), bg="#0f172a", fg="#38bdf8", labelanchor="ne")
        search_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(search_frame, text="اكتب هنا للبحث العشوائي الذكي:", font=("Arial", 11, "bold"), bg="#0f172a", fg="white").pack(side="right", padx=15, pady=15)

        self.ent_search_query = tk.Entry(search_frame, font=("Arial", 12, "bold"), bg="#1e293b", fg="#fbbf24", insertbackground="white", bd=2, relief="solid", width=35)
        self.ent_search_query.pack(side="right", padx=10, pady=15)
        self.ent_search_query.focus_set()
        self.ent_search_query.bind("<Return>", lambda e: self.execute_smart_search())

        btn_search = tk.Button(search_frame, text="🔍 ابحث واجلب البيانات آلـيـاً", font=("Arial", 11, "bold"), bg="#3b82f6", fg="white", command=self.execute_smart_search, width=22, cursor="hand2")
        btn_search.pack(side="left", padx=15, pady=12)

        # 4. حقول العرض المسترجعة
        data_frame = tk.LabelFrame(self.root, text=" 📋 حقول معلومات المركبة المسترجعة تلقائياً من الخزنة ", font=("Arial", 11, "bold"), bg="#0f172a", fg="#a7f3d0", labelanchor="ne")
        data_frame.pack(fill="x", padx=15, pady=5)

        f_row1 = tk.Frame(data_frame, bg="#0f172a")
        f_row1.pack(fill="x", padx=10, pady=6)

        tk.Label(f_row1, text="الرقم الإداري للمركبة:", font=("Arial", 11, "bold"), bg="#0f172a", fg="white", width=18, anchor="e").pack(side="right")
        self.ent_res_admin_id = tk.Entry(f_row1, font=("Arial", 11, "bold"), bg="#334155", fg="white", bd=1, relief="solid", width=22, state="readonly")
        self.ent_res_admin_id.pack(side="right", padx=5)

        tk.Label(f_row1, text="اسم السائق المعين:", font=("Arial", 11, "bold"), bg="#0f172a", fg="white", width=18, anchor="e").pack(side="right", padx=(20, 0))
        self.ent_res_driver_name = tk.Entry(f_row1, font=("Arial", 11, "bold"), bg="#334155", fg="white", bd=1, relief="solid", width=30, state="readonly")
        self.ent_res_driver_name.pack(side="right", padx=5)

        f_row2 = tk.Frame(data_frame, bg="#0f172a")
        f_row2.pack(fill="x", padx=10, pady=6)

        tk.Label(f_row2, text="رقم اللوحة المعدنية:", font=("Arial", 11, "bold"), bg="#0f172a", fg="white", width=18, anchor="e").pack(side="right")
        self.ent_res_plate = tk.Entry(f_row2, font=("Arial", 11), bg="#334155", fg="white", bd=1, relief="solid", width=22, state="readonly")
        self.ent_res_plate.pack(side="right", padx=5)

        tk.Label(f_row2, text="رقم شاصيه المركبة:", font=("Arial", 11, "bold"), bg="#0f172a", fg="white", width=18, anchor="e").pack(side="right", padx=(20, 0))
        self.ent_res_chassis = tk.Entry(f_row2, font=("Arial", 11), bg="#334155", fg="white", bd=1, relief="solid", width=30, state="readonly")
        self.ent_res_chassis.pack(side="right", padx=5)

        # 5. زر التوليد والحقن
        btn_frame = tk.Frame(self.root, bg="#020617")
        btn_frame.pack(fill="x", padx=15, pady=10)
        self.btn_generate = tk.Button(btn_frame, text="⚡ توليد شفرة الفتح وحقنها في الخزنة واعتماد تطابق السائق ⚡", 
                                      font=("Arial", 12, "bold"), bg="#10b981", fg="white", 
                                      command=self.process_generation_and_injection, height=2, cursor="hand2")
        self.btn_generate.pack(fill="x", padx=5)

        # 6. شاشة العرض والنسخ للواتساب
        display_frame = tk.LabelFrame(self.root, text=" 📄 كرت الترخيص الجاهز للنسخ والإرسال الفوري للسائق عبر الواتساب ", font=("Arial", 11, "bold"), bg="#020617", fg="#c084fc", labelanchor="ne")
        display_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.txt_display = tk.Text(display_frame, font=("Consolas", 12, "bold"), bg="#090d16", fg="#fcd34d", insertbackground="white", wrap="word", bd=0)
        self.txt_display.pack(fill="both", expand=True, padx=15, pady=15)
        self.txt_display.insert("1.0", "👈 يرجى كتابة كلمة البحث في الصندوق العلوي (اسم السائق أو رقمه أو لوحته) ثم اضغط زر البحث...")

    def on_sector_changed(self):
        self.ent_search_query.delete(0, tk.END)
        self.clear_result_fields()
        self.current_selected_record = None
        self.txt_display.delete("1.0", tk.END)
        self.txt_display.insert("1.0", f"🔄 تم الانتقال للقطاع الآخر. اكتب اسم السائق أو الرقم للبحث عنه...")

    def execute_smart_search(self):
        """ محرك بحث مرن ومقاوم تماماً لاختلاف أسماء الأعمدة في قاعدة البيانات """
        query = self.ent_search_query.get().strip()
        v_sector = self.vehicle_type_var.get()
        self.clear_result_fields()
        self.current_selected_record = None

        if not query:
            messagebox.showwarning("تنبيه البحث", "⚠️ يرجى كتابة نص أو رقم للبحث عنه أولاً!")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            search_param = f"%{query}%"

            if v_sector == "TRUCK":
                # محاولة البحث المرن في جدول الشاحنات
                try:
                    cursor.execute("""
                        SELECT serial_num, driver_name, plate_num, chassis_num 
                        FROM Truck_Main_Registry_2600 
                        WHERE serial_num LIKE ? OR plate_num LIKE ? OR driver_name LIKE ?
                    """, (search_param, search_param, search_param))
                    row = cursor.fetchone()
                    if row:
                        self.current_selected_record = {
                            "admin_id": str(row[0]), "driver_name": str(row[1] or "غير معين"),
                            "plate": str(row[2] or "بدون"), "chassis": str(row[3] or "لا يوجد"),
                            "type": "شاحنة", "unit": "كيلومتر"
                        }
                except:
                    # محاولة بديلة في حال اختلاف حقل التسمية لـ serial_num أو admin_num
                    cursor.execute("SELECT * FROM Truck_Main_Registry_2600")
                    for r in cursor.fetchall():
                        if query in str(r):
                            self.current_selected_record = {
                                "admin_id": str(r[0]), "driver_name": str(r[2] if len(r)>2 else "معين"),
                                "plate": str(r[1] if len(r)>1 else "بدون"), "chassis": str(r[3] if len(r)>3 else "لا يوجد"),
                                "type": "شاحنة", "unit": "كيلومتر"
                            }
                            break
            else:
                # محاولة البحث المرن في جدول السيارات الصغيرة
                try:
                    # تجربة البحث باستخدام حقل driver_name أو user_name التبادلي
                    cursor.execute("""
                        SELECT admin_num, driver_name, plate_num, chassis_num 
                        FROM Car_Master 
                        WHERE admin_num LIKE ? OR plate_num LIKE ? OR driver_name LIKE ?
                    """, (search_param, search_param, search_param))
                    row = cursor.fetchone()
                    if row:
                        self.current_selected_record = {
                            "admin_id": str(row[0]), "driver_name": str(row[1]),
                            "plate": str(row[2]), "chassis": str(row[3]), "type": "سيارة", "unit": "كيلومتر"
                        }
                except:
                    try:
                        # تجربة بالعمود البديل user_name بدلاً من driver_name
                        cursor.execute("""
                            SELECT admin_num, user_name, plate_num, chassis_num 
                            FROM Car_Master 
                            WHERE admin_num LIKE ? OR plate_num LIKE ? OR user_name LIKE ?
                        """, (search_param, search_param, search_param))
                        row = cursor.fetchone()
                        if row:
                            self.current_selected_record = {
                                "admin_id": str(row[0]), "driver_name": str(row[1]),
                                "plate": str(row[2]), "chassis": str(row[3]), "type": "سيارة", "unit": "كيلومتر"
                            }
                    except:
                        # قراءة شاملة وفلترة ديناميكية لمنع الانهيار نهائياً
                        cursor.execute("SELECT * FROM Car_Master")
                        for r in cursor.fetchall():
                            if query in str(r):
                                self.current_selected_record = {
                                    "admin_id": str(r[0]), "driver_name": str(r[2] if len(r)>2 else "غير معين"),
                                    "plate": str(r[1] if len(r)>1 else "بدون"), "chassis": str(r[3] if len(r)>3 else "لا يوجد"),
                                    "type": "سيارة", "unit": "كيلومتر"
                                }
                                break

            conn.close()
        except Exception as e:
            messagebox.showerror("تنبيه الخزنة", f"لم يتم العثور على ملف قاعدة بيانات نشط أو الجداول فارغة حالياً.\nالتفاصيل: {e}")
            return

        if self.current_selected_record:
            rec = self.current_selected_record
            self.fill_field_view(self.ent_res_admin_id, rec["admin_id"])
            self.fill_field_view(self.ent_res_driver_name, rec["driver_name"])
            self.fill_field_view(self.ent_res_plate, rec["plate"])
            self.fill_field_view(self.ent_res_chassis, rec["chassis"])

            self.txt_display.delete("1.0", tk.END)
            v_tag = "🚚 شاحنة نقل ثقيل" if rec["type"] == "شاحنة" else "🚗 سيارة فرعية"
            self.txt_display.insert("1.0", f"✅ تم العثور على البيانات وتعبئتها تلقائياً بنجاح!\nالنوع المسجل: {v_tag}\n\n👈 اضغط الآن على زر التوليد بالأسفل لحقن الكود ومزامنة البرنامج مع السائق.")
        else:
            self.txt_display.delete("1.0", tk.END)
            self.txt_display.insert("1.0", f"❌ لم يتم العثور على أي مركبة أو سائق يطابق كلمة البحث [{query}] في هذا القطاع.\nيرجى التأكد من كتابة الاسم بشكل صحيح أو التأكد من إدخال المركبة أولاً في لوحة الهوية الخاصة بها لكي تُحفظ بالخزنة.")

    def fill_field_view(self, entry_widget, value):
        entry_widget.config(state="normal")
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, value)
        entry_widget.config(state="readonly")

    def clear_result_fields(self):
        for entry in [self.ent_res_admin_id, self.ent_res_driver_name, self.ent_res_plate, self.ent_res_chassis]:
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="readonly")

    def process_generation_and_injection(self):
        if not self.current_selected_record:
            messagebox.showwarning("تنبيه التوليد", "⚠️ يجب البحث أولاً واستدعاء البيانات في الحقول قبل التوليد!")
            return

        rec = self.current_selected_record
        pwd = simpledialog.askstring("تحقق أمني 🔒", "أدخل الرقم السري للحقن السيادي في الخزنة:", show="*")
        if pwd != ADMIN_PASSWORD:
            messagebox.showerror("صلاحية مرفوضة", "❌ الرقم السري خاطئ! تعذر حقن الكود.")
            return

        try:
            admin_id_num = int(''.join(filter(str.isdigit, rec["admin_id"])) or 0)
        except:
            admin_id_num = 2600

        identity_hash = (admin_id_num * 7) + 2600
        prefix = "".join([c for c in rec["driver_name"] if c.isalpha()])[:3]
        if not prefix: prefix = "FAK"

        if rec["type"] == "شاحنة":
            final_auth_code = f"TRK-{admin_id_num:04d}-{prefix}-{identity_hash}"
        else:
            final_auth_code = f"CAR-{admin_id_num:04d}-{prefix}-{identity_hash}"

        # خطوة الحقن الذكي المرن
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            if rec["type"] == "شاحنة":
                try: cursor.execute("UPDATE Truck_Main_Registry_2600 SET auth_code=? WHERE serial_num=?", (final_auth_code, rec["admin_id"]))
                except: cursor.execute("UPDATE Truck_Main_Registry_2600 SET auth_code=? WHERE plate_num=?", (final_auth_code, rec["plate"]))
            else:
                try: cursor.execute("UPDATE Car_Master SET auth_code=? WHERE admin_num=?", (final_auth_code, rec["admin_id"]))
                except: cursor.execute("UPDATE Car_Master SET auth_code=? WHERE plate_num=?", (final_auth_code, rec["plate"]))
            conn.commit()
            conn.close()
            status_msg = f"✅ تم حقن التشفير بنجاح في ملف المركبة داخل الخزنة المستهدفة النشطة ({self.active_db_path})!"
        except Exception as e_db:
            status_msg = f"⚠️ تم التوليد بنجاح ولكن فشل التحديث في السجل: {e_db}"

        report = (
            f"=====================================================\n"
            f"👑 كرت التفعيل والفتح السيادي لأسطول فاخر 2600 👑\n"
            f"=====================================================\n"
            f"📌 حالة المزامنة: {status_msg}\n"
            f"👤 اسم السائق المعتمد : {rec['driver_name']}\n"
            f"🆔 الرقم الإداري الموحد  : {rec['admin_id']}\n"
            f"🔢 رقم لوحة المركبة   : {rec['plate']}\n"
            f"⚙️ رقم شاصيه المصنع  : {rec['chassis']}\n"
            f"-----------------------------------------------------\n"
            f"👇 انسخ السطر التالي بالكامل وأرسله للسائق عبر الواتساب:\n\n"
            f"رمز فتح المنظومة وتوثيق الهوية: {final_auth_code}\n\n"
            f"-----------------------------------------------------\n"
            f"💡 بمجرد لصق السائق لهذا الرمز، ستطابق الهوية وتفتح صلاحيات الصيانة فوراً."
        )

        self.txt_display.delete("1.0", tk.END)
        self.txt_display.insert("1.0", report)
        messagebox.showinfo("نجاح الحقن والمزامنة 🔑", f"🚀 تم إصدار الرمز وحقنه بنجاح للمركبة رقم [{rec['admin_id']}]!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FleetFinalStandaloneGenerator(root)
    root.mainloop()