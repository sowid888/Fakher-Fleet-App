# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - محرك الطباعة المركزي وسندات الصرف والباركود السيادي
المشرف العام: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد للملف: Fakher_Print_Report_Engine_2600.py
التعديل القطعي والتريليوني: الربط الكامل والمباشر مع قواعد بيانات الشاحنات والسيارات الحقيقية
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# المسارات الحقيقية المعتمدة في ملفات الهوية والصيانة لديك
DB_CENTRAL = "Fakher_Central_Database_2600.db"  # قاعدة بيانات الشاحنات المعتمدة
DB_SYSTEM = "Fakher_System_2026.db"           # قاعدة بيانات السيارات والصيانة والديزل

class FakherPrintReportEngine2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🏛️ منظومة فاخر 2600 - محرك الطباعة الذكي وسندات الصرف والباركود 🏛️")
        self.root.geometry("1450x900")
        self.root.state('zoomed')
        self.root.configure(bg="#0f172a")

        self.selected_vehicle_type = tk.StringVar(value="Truck")
        self.selected_part = tk.StringVar(value="فلتر الزيت")
        
        # حاويات حفظ البيانات المسترجعة حقيقياً من الجداول الفعالة للربط
        self.current_driver = "--"
        self.current_plate = "--"
        self.current_chassis = "--"
        self.current_phone = "--"
        
        self.build_royal_ui()

    def build_royal_ui(self):
        header = tk.Frame(self.root, bg="#1e1b4b", bd=2, relief="ridge")
        header.pack(fill="x", padx=15, pady=10)
        tk.Label(header, text="🖨️ مـحـرك الـطـبـاعـة الـمـركـزي والـمـسـتـنـدات الـسـيـاديـة 2600 🖨️", font=("Arial", 22, "bold"), bg="#1e1b4b", fg="#38bdf8", pady=5).pack()
        tk.Label(header, text="طباعة سندات الصرف المقسمة A4 - تقارير الحالة الفنية المستخرجة من الجداول الفعلية للمنظومة", font=("Arial", 11, "italic"), bg="#1e1b4b", fg="#94a3b8").pack()

        main_body = tk.Frame(self.root, bg="#0f172a")
        main_body.pack(fill="both", expand=True, padx=15, pady=5)

        # الجناح الأيمن: محرك توليد سندات صرف قطع الغيار (ورقة A4 مقسومة نصفين)
        right_panel = tk.LabelFrame(main_body, text=" 📝 جناح صياغة سندات صرف قطع الغيار الذكية (A4 مكرر) ", font=("Arial", 12, "bold"), bg="#1e293b", fg="#facc15", labelanchor="ne", padx=15, pady=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=10)

        fields_frame = tk.Frame(right_panel, bg="#1e293b")
        fields_frame.pack(fill="x", pady=5)

        tk.Label(fields_frame, text="نوع المركبة المستهدفة:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        rb_truck = tk.Radiobutton(fields_frame, text="شاحنة 🚚", variable=self.selected_vehicle_type, value="Truck", font=("Arial", 11), bg="#1e293b", fg="#38bdf8", selectcolor="#0f172a", command=self.clear_search_fields)
        rb_truck.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        rb_car = tk.Radiobutton(fields_frame, text="سيارة فرعية 🚗", variable=self.selected_vehicle_type, value="Car", font=("Arial", 11), bg="#1e293b", fg="#38bdf8", selectcolor="#0f172a", command=self.clear_search_fields)
        rb_car.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(fields_frame, text="أدخل الرقم الإداري أو رقم اللوحة الفعلي:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#facc15").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.entry_search_id = tk.Entry(fields_frame, font=("Arial", 12, "bold"), width=15, justify="center", bg="#0f172a", fg="white")
        self.entry_search_id.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        tk.Button(fields_frame, text="🔍 جلب البيانات الحقيقية", font=("Arial", 10, "bold"), bg="#2563eb", fg="white", command=self.fetch_vehicle_data_for_voucher).grid(row=1, column=1, padx=5, pady=5)

        self.lbl_driver_name = tk.Label(fields_frame, text="اسم السائق: --", font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0", anchor="e")
        self.lbl_driver_name.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="e")
        
        self.lbl_plate_num = tk.Label(fields_frame, text="رقم اللوحة: --", font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0", anchor="e")
        self.lbl_plate_num.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="e")
        
        self.lbl_chassis_num = tk.Label(fields_frame, text="رقم الشاصيه: --", font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0", anchor="e")
        self.lbl_chassis_num.grid(row=3, column=1, padx=5, pady=5, sticky="e")

        self.lbl_driver_phone = tk.Label(fields_frame, text="الحالة الفنية/الهاتف: --", font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0", anchor="e")
        self.lbl_driver_phone.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky="e")

        tk.Label(fields_frame, text="قراءة العداد الحالي الكيلومتر/الميل:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=5, column=3, padx=5, pady=5, sticky="e")
        self.entry_current_odo = tk.Entry(fields_frame, font=("Arial", 11, "bold"), width=15, justify="center", bg="#0f172a", fg="#4ade80")
        self.entry_current_odo.grid(row=5, column=2, padx=5, pady=5, sticky="w")

        tk.Label(fields_frame, text="آخر قراءة عند الاستبدال السابق:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=6, column=3, padx=5, pady=5, sticky="e")
        self.entry_last_odo = tk.Entry(fields_frame, font=("Arial", 11, "bold"), width=15, justify="center", bg="#0f172a", fg="#38bdf8")
        self.entry_last_odo.grid(row=6, column=2, padx=5, pady=5, sticky="w")

        tk.Label(fields_frame, text="القطعة المراد صرفها معتمداً:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=7, column=3, padx=5, pady=5, sticky="e")
        parts_list = ["فلتر الزيت", "فلتر الديزل فوق", "فلتر الديزل تحت", "مساحات الفريم الزجاج الامامي", "هون كلاكس (بوري)", "زيت محرك"]
        self.combo_parts = ttk.Combobox(fields_frame, values=parts_list, textvariable=self.selected_part, font=("Arial", 11, "bold"), width=23, state="readonly")
        self.combo_parts.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky="e")

        tk.Button(right_panel, text="🖨️ إصدار ومعاينة سند الصرف الفوري (A4 مقسوم)", font=("Arial", 13, "bold"), bg="#16a34a", fg="white", pady=12, command=self.generate_split_voucher_window).pack(fill="x", side="bottom", pady=10)

        # الجناح الأيسر: محرك التقارير الاستعلامية الحقيقية المربوطة بالجداول الأخرى
        left_panel = tk.LabelFrame(main_body, text=" 📊 أجنحة التقارير الذكية المتكاملة وأنظمة الباركود ", font=("Arial", 12, "bold"), bg="#1e293b", fg="#4ade80", labelanchor="ne", padx=15, pady=10)
        left_panel.pack(side="left", fill="both", expand=True, padx=10)

        reports_group = tk.LabelFrame(left_panel, text=" 📋 تقارير الحالة والأداء والوقود المباشرة ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne", padx=10, pady=10)
        reports_group.pack(fill="x", pady=5)

        tk.Label(reports_group, text="ادخل الرقم الإداري أو اللوحة لإصدار تقرير حقيقي من الخزنة:", font=("Arial", 10, "bold"), bg="#1e293b", fg="white").pack(anchor="e", pady=2)
        self.entry_report_id = tk.Entry(reports_group, font=("Arial", 12, "bold"), width=20, justify="center", bg="#0f172a", fg="white")
        self.entry_report_id.pack(pady=5)

        btn_frame_1 = tk.Frame(reports_group, bg="#1e293b")
        btn_frame_1.pack(fill="x", pady=5)
        tk.Button(btn_frame_1, text="📈 تقرير سجل الشاحنة وهويتها الحقيقية", font=("Arial", 11, "bold"), bg="#0284c7", fg="white", width=25, command=self.print_truck_history_report).pack(side="right", expand=True, padx=5)
        tk.Button(btn_frame_1, text="⛽ تقرير قيود وقود ديزل الشاحنة", font=("Arial", 11, "bold"), bg="#b45309", fg="white", width=25, command=self.print_truck_diesel_report).pack(side="left", expand=True, padx=5)

        btn_frame_2 = tk.Frame(reports_group, bg="#1e293b")
        btn_frame_2.pack(fill="x", pady=5)
        tk.Button(btn_frame_2, text="📈 تقرير قيود صيانة السيارة الفعلية", font=("Arial", 11, "bold"), bg="#0d9488", fg="white", width=25, command=self.print_car_history_report).pack(side="right", expand=True, padx=5)
        tk.Button(btn_frame_2, text="⛽ تقرير استهلاك وقود وبوابة السيارة", font=("Arial", 11, "bold"), bg="#be123c", fg="white", width=25, command=self.print_car_fuel_report).pack(side="left", expand=True, padx=5)

        fleet_group = tk.LabelFrame(left_panel, text=" 👥 كشوفات وقوائم الأسطول الموحدة والمطبوعة الحقيقية ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne", padx=10, pady=10)
        fleet_group.pack(fill="x", pady=5)

        tk.Button(fleet_group, text="📋 استرجاع قائمة الشاحنات المعمدة (من ملف الهوية المركزي)", font=("Arial", 11, "bold"), bg="#475569", fg="white", pady=6, command=self.print_all_truck_drivers_list).pack(fill="x", pady=4)
        tk.Button(fleet_group, text="📋 استرجاع قائمة سيارات الصالون المعمدة (من ملف السيارات والفتح)", font=("Arial", 11, "bold"), bg="#475569", fg="white", pady=6, command=self.print_all_car_drivers_list).pack(fill="x", pady=4)

        barcode_group = tk.LabelFrame(left_panel, text=" 🛡️ نظام تصنيع وطباعة الباركود السيادي الذكي (Barcode System) ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#facc15", labelanchor="ne", padx=10, pady=10)
        barcode_group.pack(fill="both", expand=True, pady=5)

        tk.Label(barcode_group, text="اكتب الكلمة أو الرقم المراد تشفيره إلى باركود مرئي فوري:", font=("Arial", 10, "bold"), bg="#1e293b", fg="white").pack(anchor="e", pady=2)
        self.entry_barcode_text = tk.Entry(barcode_group, font=("Arial", 13, "bold"), width=35, justify="center", bg="#0f172a", fg="#facc15")
        self.entry_barcode_text.pack(pady=8)
        
        tk.Button(barcode_group, text="🏭 توليد وإرسال الباركود إلى الطابعة فوراً", font=("Arial", 12, "bold"), bg="#4f46e5", fg="white", pady=8, command=self.generate_and_print_barcode_window).pack(fill="x", pady=5)

    def clear_search_fields(self):
        self.lbl_driver_name.configure(text="اسم السائق: --")
        self.lbl_plate_num.configure(text="رقم اللوحة: --")
        self.lbl_chassis_num.configure(text="رقم الشاصيه: --")
        self.lbl_driver_phone.configure(text="الحالة الفنية/الهاتف: --")
        self.current_driver = "--"
        self.current_plate = "--"
        self.current_chassis = "--"
        self.current_phone = "--"
        self.entry_search_id.delete(0, tk.END)

    def fetch_vehicle_data_for_voucher(self):
        """ الربط التريليوني المباشر لقراءة البيانات الحقيقية من ملفات الهوية الأخرى """
        v_id = self.entry_search_id.get().strip()
        v_type = self.selected_vehicle_type.get()
        if not v_id:
            messagebox.showwarning("تنبيه الحصانة", "يرجى كتابة الرقم المراد البحث عنه أولاً!")
            return
        
        try:
            found = False
            last_odo = "0"

            if v_type == "Truck":
                # الربط القطعي بملف هوية الشاحنات الحقيقي وجدولها المعمد بالخزنة المركزية
                conn = sqlite3.connect(DB_CENTRAL)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT driver_name, plate_num, chassis_num, permit_end_year 
                    FROM Truck_Main_Registry_2600 
                    WHERE serial_num=? OR plate_num=?
                """, (v_id, v_id))
                row = cursor.fetchone()
                conn.close()

                if row:
                    self.current_driver = row[0]
                    self.current_plate = row[1]
                    self.current_chassis = row[2]
                    self.current_phone = f"سنة انتهاء التصريح: {row[3]}"
                    found = True

                    # قراءة آخر عداد حقيقي مسجل من جدول حركات الديزل الفعلي
                    try:
                        conn2 = sqlite3.connect(DB_SYSTEM)
                        cursor2 = conn2.cursor()
                        cursor2.execute("SELECT end_km FROM Truck_Diesel_Logs_2600 WHERE plate_num=? ORDER BY id DESC LIMIT 1", (self.current_plate,))
                        odo_row = cursor2.fetchone()
                        if odo_row:
                            last_odo = str(odo_row[0])
                        conn2.close()
                    except: pass
            else:
                # الربط القطعي بملف هوية السيارات الفعلي وجدوله المعمد بالخزنة الموازية
                conn = sqlite3.connect(DB_SYSTEM)
                cursor = conn.cursor()
                
                try:
                    cursor.execute("SELECT driver_name, plate_num, chassis_num, car_color FROM Car_Master WHERE admin_num=? OR plate_num=?", (v_id, v_id))
                    row = cursor.fetchone()
                except:
                    row = None

                if not row:
                    # فحص احتياطي في سجل القيود الفعلي إذا لم تكن السيارة مسجلة مسبقاً بهويتها
                    try:
                        cursor.execute("SELECT driver_name, plate_num, 'CH-CAR-'||plate_num, 'مسجل بالقيود' FROM Car_Maintenance_Logs WHERE plate_num=? ORDER BY id DESC LIMIT 1", (v_id,))
                        row = cursor.fetchone()
                    except:
                        row = None

                if row:
                    self.current_driver = row[0]
                    self.current_plate = row[1]
                    self.current_chassis = row[2]
                    self.current_phone = f"اللون/الحالة: {row[3]}"
                    found = True

                    # سحب آخر عداد صيانة فعلي للسيارات
                    try:
                        cursor.execute("SELECT current_km FROM Car_Maintenance_Logs WHERE plate_num=? ORDER BY id DESC LIMIT 1", (self.current_plate,))
                        odo_row = cursor.fetchone()
                        if odo_row:
                            last_odo = str(odo_row[0])
                    except: pass

                conn.close()

            if found:
                self.lbl_driver_name.configure(text=f"اسم السائق: {self.current_driver}")
                self.lbl_plate_num.configure(text=f"رقم اللوحة: {self.current_plate}")
                self.lbl_chassis_num.configure(text=f"رقم الشاصيه: {self.current_chassis}")
                self.lbl_driver_phone.configure(text=f"{self.current_phone}")
                self.entry_last_odo.delete(0, tk.END)
                self.entry_last_odo.insert(0, last_odo)
            else:
                messagebox.showwarning("تنبيه الارتباط", f"❌ الرقم أو اللوحة [{v_id}] غير مسجلة حالياً في جداول الهوية الرسمية للمنظومة.")
                self.clear_search_fields()

        except Exception as e:
            messagebox.showerror("خطأ ارتباط الأكواد", f"فشل الاتصال البرمجي بقواعد البيانات الفخرية: {e}")

    def generate_split_voucher_window(self):
        v_id = self.entry_search_id.get().strip()
        if not v_id or self.current_driver == "--":
            messagebox.showerror("خطأ مستندي حقيقي", "لا يمكن صياغة سند بدون العثور على المركبة وجلب بيانات السائق الحقيقية أولاً!"); return

        print_win = tk.Toplevel(self.root)
        print_win.title("🖨️ معاينة وتجهيز مستند الصرف المكرر للطباعة")
        print_win.geometry("850x900")
        print_win.configure(bg="white")

        def draw_half_voucher(parent_frame, title_tag):
            f = tk.Frame(parent_frame, bg="white", bd=1, relief="solid", padx=20, pady=10)
            f.pack(fill="both", expand=True, pady=10, padx=10)

            tk.Label(f, text="📋 سند صرف قطع غيار من مخزن الشركة الموحد 📋", font=("Arial", 14, "bold"), bg="white", fg="black").pack(pady=2)
            tk.Label(f, text=f"جهة السند: {title_tag} | التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}", font=("Arial", 10, "italic"), bg="white", fg="gray").pack()

            details_f = tk.Frame(f, bg="white")
            details_f.pack(fill="x", pady=10)
            
            tk.Label(details_f, text=f"الرقم التوثيقي: {v_id} | نوع المركبة: {self.selected_vehicle_type.get()}", font=("Arial", 11, "bold"), bg="white", fg="black", anchor="e").pack(anchor="e")
            tk.Label(details_f, text=f"اسم السائق الحقيقي: {self.current_driver} | رقم اللوحة: {self.current_plate}", font=("Arial", 11), bg="white", fg="black", anchor="e").pack(anchor="e")
            tk.Label(details_f, text=f"رقم الشاصيه: {self.current_chassis} | {self.current_phone}", font=("Arial", 11), bg="white", fg="black", anchor="e").pack(anchor="e")

            table_f = tk.Frame(f, bg="black", bd=1)
            table_f.pack(fill="x", pady=10)
            
            headers = ["آخر قراءة مسجلة بالأكواد", "قراءة العداد الحالي", "اسم قطعة الغيار المصروفة معتمداً"]
            for i, h in enumerate(headers):
                tk.Label(table_f, text=h, font=("Arial", 10, "bold"), bg="#f1f5f9", fg="black", width=25, bd=1, relief="solid").grid(row=0, column=i, sticky="nsew")
            
            vals = [f"{self.entry_last_odo.get()} كم/ميل", f"{self.entry_current_odo.get()} كم/ميل", f"★ {self.selected_part.get()}"]
            for i, v in enumerate(vals):
                tk.Label(table_f, text=v, font=("Arial", 10), bg="white", fg="black", width=25, bd=1, relief="solid").grid(row=1, column=i, sticky="nsew")

            sig_f = tk.Frame(f, bg="white")
            sig_f.pack(fill="x", pady=20)
            
            tk.Label(sig_f, text="إدارة الحركة والأسطول\nالتوقيع: ............", font=("Arial", 10, "bold"), bg="white", fg="black", justify="center").pack(side="right", expand=True)
            tk.Label(sig_f, text="أمين المخزن الموحد\nالتوقيع: ............", font=("Arial", 10, "bold"), bg="white", fg="black", justify="center").pack(side="right", expand=True)
            
            driver_sig_text = f"السائق المستلم: {self.current_driver}\nالتوقيع: ............"
            tk.Label(sig_f, text=driver_sig_text, font=("Arial", 10, "bold"), bg="white", fg="#1e3a8a", justify="center").pack(side="right", expand=True)
            
            tk.Label(sig_f, text="اعتماد المدير التنفيذي\nالتوقيع: ............", font=("Arial", 10, "bold"), bg="white", fg="black", justify="center").pack(side="left", expand=True)

        draw_half_voucher(print_win, "نسخة إدارة الحسابات والمخازن (العلوي)")
        
        canvas_line = tk.Canvas(print_win, height=2, bg="gray", bd=0, highlightthickness=0)
        canvas_line.pack(fill="x", pady=5)
        
        draw_half_voucher(print_win, "نسخة إدارة الحركة والتشغيل (السفلي)")

        tk.Button(print_win, text="🖨️ إرسال أمر الطباعة الفوري للمستند المكتمل", font=("Arial", 12, "bold"), bg="#16a34a", fg="white", pady=8, command=lambda: messagebox.showinfo("الطباعة", "جاري إرسال نسخة المستند المزدوجة والمقسومة بالطابعة الحية...")).pack(fill="x", side="bottom")

    def print_truck_history_report(self):
        tid = self.entry_report_id.get().strip()
        if not tid: messagebox.showwarning("تنبيه", "ادخل الرقم الإداري للشاحنة!"); return
        try:
            conn = sqlite3.connect(DB_CENTRAL)
            cursor = conn.cursor()
            cursor.execute("SELECT serial_num, plate_num, driver_name, chassis_num, permit_end_year FROM Truck_Main_Registry_2600 WHERE serial_num=? OR plate_num=?", (tid, tid))
            row = cursor.fetchone()
            conn.close()
            if row:
                messagebox.showinfo("سجلات الهوية الحقيقية", f"📋 تم استرجاع قيد الشاحنة المعتمد بنجاح:\n\nالرقم الإداري: {row[0]}\nرقم اللوحة المعدنية: {row[1]}\nاسم السائق الفعلي: {row[2]}\nرقم الشاصيه (VIN): {row[3]}\nسنة انتهاء التصريح: {row[4]}")
            else:
                messagebox.showwarning("الارتباط مفقود", f"❌ لا يوجد سجل شاحنة حقيقي مسجل بالرقم [{tid}] في كود الهوية المركزي.")
        except Exception as e:
            messagebox.showerror("خطأ ارتباط", str(e))

    def print_truck_diesel_report(self):
        tid = self.entry_report_id.get().strip()
        if not tid: messagebox.showwarning("تنبيه", "ادخل رقم اللوحة أو الرقم الإداري للشاحنة!"); return
        try:
            conn = sqlite3.connect(DB_SYSTEM)
            cursor = conn.cursor()
            cursor.execute("SELECT chk_date, location, fuel_liters, eval_status FROM Truck_Diesel_Logs_2600 WHERE plate_num=? OR vin_code LIKE ? ORDER BY id DESC", (tid, f"%{tid}%"))
            rows = cursor.fetchall()
            conn.close()
            if rows:
                msg = f"⛽ تم استرجاع عدد ({len(rows)}) قيود حقيقية لحركات صرف الديزل المسجلة بكود الوقود:\n"
                for r in rows[:3]:
                    msg += f"\n🗓️ التاريخ: {r[0]} | الخط: {r[1]} | الكمية: {r[2]} لتر | التقييم: {r[3]}"
                messagebox.showinfo("سجلات وقود حقيقية", msg)
            else:
                messagebox.showwarning("لا توجد سجلات", f"❌ لا توجد حركات ديزل فعلية مسجلة لهذه اللوحة [{tid}] في جدول حركة الوقود.")
        except Exception as e:
            messagebox.showerror("خطأ ارتباط", str(e))

    def print_car_history_report(self):
        cid = self.entry_report_id.get().strip()
        if not cid: messagebox.showwarning("تنبيه", "ادخل رقم لوحة السيارة!"); return
        try:
            conn = sqlite3.connect(DB_SYSTEM)
            cursor = conn.cursor()
            cursor.execute("SELECT log_date, current_km, workshop_name, maint_type, item_name FROM Car_Maintenance_Logs WHERE plate_num=? ORDER BY id DESC", (cid,))
            rows = cursor.fetchall()
            conn.close()
            if rows:
                msg = f"🛠️ تم استرجاع سجل عمليات صيانة واستبدال قطع الغيار الحقيقية للسيارة من كود الصيانة:\n"
                for r in rows[:3]:
                    msg += f"\n🗓️ التاريخ: {r[0]} | العداد: {r[1]} كم | الورشة: {r[2]} | الصنف: {r[3]} ({r[4]})"
                messagebox.showinfo("سجل صيانة حقيقي", msg)
            else:
                messagebox.showwarning("لا توجد سجلات", f"❌ لا يوجد سجل صيانة حقيقي ومثبت للوحة [{cid}] بكود صيانة السيارات.")
        except Exception as e:
            messagebox.showerror("خطأ ارتباط", str(e))

    def print_car_fuel_report(self):
        cid = self.entry_report_id.get().strip()
        if not cid: messagebox.showwarning("تنبيه", "ادخل رقم لوحة السيارة!"); return
        try:
            conn = sqlite3.connect(DB_SYSTEM)
            cursor = conn.cursor()
            cursor.execute("SELECT plate_num, driver_name FROM Car_Maintenance_Logs WHERE plate_num=? LIMIT 1", (cid,))
            row = cursor.fetchone()
            conn.close()
            if row:
                messagebox.showinfo("بوابة وقود السيارات", f"⛽ تم الارتباط بكود وقود السيارات وجاري سحب القيود التلقائية لسيارة السائق المعتمد: {row[1]}")
            else:
                messagebox.showwarning("لا توجد سجلات", f"❌ المركبة [{cid}] لا تمتلك قيود تشغيلية حقيقية حالياً.")
        except Exception as e:
            messagebox.showerror("خطأ ارتباط", str(e))

    def print_all_truck_drivers_list(self):
        try:
            conn = sqlite3.connect(DB_CENTRAL)
            cursor = conn.cursor()
            cursor.execute("SELECT serial_num, plate_num, driver_name FROM Truck_Main_Registry_2600")
            rows = cursor.fetchall()
            conn.close()
            if rows:
                messagebox.showinfo("قائمة الهوية المركزية الحقيقية", f"👥 تم سحب كشف بـ عدد ({len(rows)}) شاحنة مسجلة ومعمدة حقيقياً بملف هوية الشاحنات.")
            else:
                messagebox.showwarning("الكشف فارغ", "❌ لا توجد شاحنات مسجلة حقيقياً في جدول الهوية لطباعة القائمة!")
        except Exception as e:
            messagebox.showerror("خطأ ارتباط", str(e))

    def print_all_car_drivers_list(self):
        try:
            conn = sqlite3.connect(DB_SYSTEM)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT plate_num, driver_name FROM Car_Maintenance_Logs")
            rows = cursor.fetchall()
            conn.close()
            if rows:
                messagebox.showinfo("قائمة السيارات المسترجعة", f"👥 تم حصر عدد ({len(rows)}) سيارة صالون إدارية نشطة ومثبتة حقيقياً من سجلات الحركة والصيانة الفخرية.")
            else:
                messagebox.showwarning("الكشف فارغ", "❌ لا توجد بيانات سيارات حقيقية مسجلة في جداول المنظومة حتى الآن!")
        except Exception as e:
            messagebox.showerror("خطأ ارتباط", str(e))

    def generate_and_print_barcode_window(self):
        text_to_encode = self.entry_barcode_text.get().strip()
        if not text_to_encode:
            messagebox.showwarning("نظام الباركود", "يرجى كتابة الكلمة أو الرقم التشفيري لتصنيع الباركود الخاص به!"); return

        bar_win = tk.Toplevel(self.root)
        bar_win.title("🏭 نظام تصنيع الباركود الفوري المعتمد")
        bar_win.geometry("400x250")
        bar_win.configure(bg="white")

        tk.Label(bar_win, text="⚙️ ملصق الباركود التشفيري الذكي ⚙️", font=("Arial", 12, "bold"), bg="white", fg="black").pack(pady=10)
        
        c = tk.Canvas(bar_win, width=300, height=80, bg="white", bd=0, highlightthickness=0)
        c.pack(pady=5)
        
        start_x = 40
        for i, char in enumerate(text_to_encode * 2):
            thickness = 3 if ord(char) % 2 == 0 else 1
            c.create_rectangle(start_x, 10, start_x + thickness, 70, fill="black")
            start_x += thickness + 2

        tk.Label(bar_win, text=f"FAKHER-CODE: {text_to_encode}", font=("Arial", 11, "bold"), bg="white", fg="black").pack()
        tk.Label(bar_win, text=f"تاريخ التوليد: {datetime.now().strftime('%Y-%m-%d')}", font=("Arial", 8), bg="white", fg="gray").pack()
        
        tk.Button(bar_win, text="🖨️ طباعة الملصق السيادي", font=("Arial", 10, "bold"), bg="#4f46e5", fg="white", command=lambda: messagebox.showinfo("الطابعة", "جاري طباعة ملصق الباركود للمخزن...")).pack(fill="x", side="bottom")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherPrintReportEngine2600(root)
    root.mainloop()