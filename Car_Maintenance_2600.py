# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - سجل الصيانة الفني لسيارات الصالون (النسخة المعالجة والمربوطة بالخزنة الموحدة 100%)
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد: Car_Maintenance_2600.py
التعديل الإستراتيجي: إصلاح خوارزمية الاستدعاء للربط المباشر بجدول Car_Master وإنهاء مشكلة عدم العثور على المركبات
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
import os
from datetime import datetime

# المسار الصارم والموحد للمنظومة في قرص C لضمان قراءة الخزنة المشتركة
TARGET_DIR = "C:/Fakher_System"
DB_NAME_CAR_SYSTEM = "Fakher_System_2026.db"
SECRET_PASSWORD = "2600"

class CarMaintenanceSuperPro2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ منظومة فاخر 2600 - سجل الصيانة الفني العملاق للسيارات 🛡️")
        self.root.geometry("1300x850")
        self.root.state('zoomed')
        self.root.configure(bg="#0f172a")
        
        self.is_car_loaded = False
        self.loaded_admin_num = ""
        self.loaded_plate = ""
        self.loaded_driver = ""
        
        self.resolve_db_paths()
        self.init_db()
        self.build_ui_layout()

    def resolve_db_paths(self):
        """تحديد مسار قاعدة البيانات بدقة لضمان الارتباط التلقائي الخالي من الأخطاء"""
        if not os.path.exists(TARGET_DIR):
            try: os.makedirs(TARGET_DIR)
            except: pass
            
        # فرض المسار الموحد في قرص C ليتطابق تماماً مع كود الهوية
        self.db_car_system_path = os.path.join(TARGET_DIR, DB_NAME_CAR_SYSTEM)

    def init_db(self):
        """إنشاء جدول سجلات صيانة السيارات إذا لم يكن موجوداً"""
        try:
            conn = sqlite3.connect(self.db_car_system_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Car_Maintenance_Logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_num TEXT,
                    plate_num TEXT,
                    driver_name TEXT,
                    km_reading REAL,
                    workshop_name TEXT,
                    replacement_type TEXT,
                    item_name TEXT,
                    prod_date TEXT,
                    sub_type TEXT,
                    capacity TEXT,
                    supplier_name TEXT,
                    fault_details TEXT,
                    log_date TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Car Database Init Error: {e}")

    def build_ui_layout(self):
        # 1. الرأس العلوي
        header = tk.Frame(self.root, bg="#1e1b4b", pady=12)
        header.pack(fill="x", padx=15, pady=8)
        tk.Label(header, text="⚙️ سـجـل صـيـانـة ومـسـتـهـلـكـات الـسـيـارات الـمـركـزي 2600 ⚙️", 
                 font=("Arial", 18, "bold"), bg="#1e1b4b", fg="#38bdf8").pack()

        # 2. قطاع البحث والاستدعاء الفني الشامل
        search_frame = tk.LabelFrame(self.root, text=" 🔍 قطاع الاستدعاء المباشر الذكي من جدول الهوية الفاخر ", font=("Arial", 12, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne", padx=15, pady=10)
        search_frame.pack(fill="x", padx=15, pady=5)
        
        btn_search = tk.Button(search_frame, text="🔍 استدعاء ومطابقة هوية السيارة", font=("Arial", 12, "bold"), bg="#2563eb", fg="white", padx=15, command=self.search_car_action)
        btn_search.pack(side="left", padx=10)
        
        self.txt_search = tk.Entry(search_frame, font=("Arial", 14, "bold"), width=45, justify="center", bg="#334155", fg="white", insertbackground="white")
        self.txt_search.pack(side="right", padx=15, pady=5)
        self.txt_search.bind("<Return>", lambda e: self.search_car_action()) 
        tk.Label(search_frame, text="أدخل [الرقم الإداري] أو [رقم اللوحة] أو [اسم السائق]:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").pack(side="right", padx=5)

        # 3. محتوى الشاشة الرئيسي
        main_content = tk.Frame(self.root, bg="#0f172a")
        main_content.pack(fill="both", expand=True, padx=15, pady=5)

        # [الجانب الأيمن]: عرض هوية السيارة المستدعاة
        self.right_frame = tk.LabelFrame(main_content, text=" 📋 هوية السيارة التعريفية المستدعاة حالياً ", font=("Arial", 13, "bold"), bg="#1e293b", fg="#facc15", labelanchor="ne", padx=20, pady=15, width=400)
        self.right_frame.pack(side="right", fill="y", padx=10, pady=5)
        self.right_frame.pack_propagate(False)

        self.identity_fields = [
            ("الاسم الكامل للسائق الحركي:", "lbl_val_driver"),
            ("رقم اللوحة المعدنية المعتمد:", "lbl_val_plate"),
            ("الرقم الإداري للسيارة:", "lbl_val_admin"),
            ("رقم الشاصيه الهيكلي الفني:", "lbl_val_chassis"),
            ("فئة ونوع السيارة المجدول:", "lbl_val_unit_type"),
            ("تاريخ انتهاء تصريح الفحص العام:", "lbl_val_permit")
        ]
        
        for lbl_text, attr_name in self.identity_fields:
            tk.Label(self.right_frame, text=lbl_text, font=("Arial", 11, "bold"), bg="#1e293b", fg="#94a3b8").pack(anchor="e", pady=2)
            lbl = tk.Label(self.right_frame, text="🔒 بانتظار الاستدعاء...", font=("Arial", 12, "bold"), bg="#1e293b", fg="#ef4444", justify="right")
            lbl.pack(anchor="e", pady=4)
            setattr(self, attr_name, lbl)

        # [الجانب الأيسر]: مدخلات الصيانة الفنية للأعطال
        self.left_frame = tk.LabelFrame(main_content, text=" 🛠️ البيانات الفنية للقطع المستبدلة وصيانة السيارة ", font=("Arial", 13, "bold"), bg="#1e293b", fg="white", labelanchor="ne", padx=20, pady=15)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        top_inputs = tk.Frame(self.left_frame, bg="#1e293b")
        top_inputs.pack(fill="x", pady=5)

        tk.Label(top_inputs, text="عداد الكيلومتر الحالي للسيارة:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").pack(side="right", padx=5)
        self.txt_km = tk.Entry(top_inputs, font=("Arial", 13, "bold"), width=15, justify="center")
        self.txt_km.pack(side="right", padx=15)

        tk.Label(top_inputs, text="اسم الورشة المنفذة للصيانة:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").pack(side="right", padx=5)
        self.txt_workshop = tk.Entry(top_inputs, font=("Arial", 13, "bold"), width=20, justify="center")
        self.txt_workshop.pack(side="right", padx=15)

        type_select_frame = tk.Frame(self.left_frame, bg="#1e293b")
        type_select_frame.pack(fill="x", pady=10)
        
        tk.Label(type_select_frame, text="تصنيف ونوع الاستبدال الفني:", font=("Arial", 12, "bold"), bg="#1e293b", fg="#67e8f9").pack(side="right", padx=5)
        self.combo_main_type = ttk.Combobox(type_select_frame, values=["استبدال قطع في المحرك", "استبدال قطع في البودي", "استبدال قطع كهربائية", "استبدال قطع أخرى", "إطارات", "بطاريات"], font=("Arial", 12, "bold"), state="readonly", width=30, justify="center")
        self.combo_main_type.pack(side="right", padx=15)
        self.combo_main_type.bind("<<ComboboxSelected>>", self.handle_type_switching_logic)

        self.dynamic_fields_panel = tk.Frame(self.left_frame, bg="#1e293b", bd=1, relief="groove", pady=10, padx=10)
        self.dynamic_fields_panel.pack(fill="x", pady=10)
        
        self.lbl_dyn_hint = tk.Label(self.dynamic_fields_panel, text="يرجى اختيار نوع الاستبدال لإظهار الحقول الحيوية الخاصة به مخصصة", font=("Arial", 11, "italic"), bg="#1e293b", fg="#94a3b8")
        self.lbl_dyn_hint.pack(pady=10)

        desc_frame = tk.Frame(self.left_frame, bg="#1e293b")
        desc_frame.pack(fill="x", pady=5)
        tk.Label(desc_frame, text="✍️ وصف تفصيلي للقطع المستبدلة وطبيعة الأعطال المشخصة للسيارة:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").pack(anchor="e", pady=2)
        
        self.txt_fault_details = tk.Text(desc_frame, height=7, font=("Arial", 12, "bold"), bg="#0f172a", fg="white", insertbackground="white")
        self.txt_fault_details.pack(fill="x", pady=5)

        self.btn_save = tk.Button(self.left_frame, text="🔒 اعتماد وحفظ السجل الفني للسيارة بالخزنة الموحدة", font=("Arial", 13, "bold"), bg="#16a34a", fg="white", pady=8, command=self.secure_save_car_maintenance_action)
        self.btn_save.pack(fill="x", pady=10)

        self.setup_inputs_navigation()

    def setup_inputs_navigation(self):
        widgets = [self.txt_km, self.txt_workshop, self.combo_main_type, self.txt_fault_details]
        for idx, w in enumerate(widgets):
            w.bind("<Return>", lambda e, i=idx, w_list=widgets: w_list[(i+1)%len(w_list)].focus_set())

    def search_car_action(self):
        """🔍 خوارزمية الربط الصارم والمباشر بجدول Car_Master لضمان الاستدعاء الفوري والدقيق"""
        search_query = self.txt_search.get().strip()
        if not search_query:
            messagebox.showwarning("تنبيه المنظومة", "❌ يرجى إدخال قيمة للبحث أولاً!")
            return

        if not os.path.exists(self.db_car_system_path):
            messagebox.showerror("خطأ مسار قاعدة البيانات", f"❌ لم يتم العثور على ملف الخزنة المركزية.\n📍 تأكد من تشغيل كود الهوية أولاً لإنشاء قاعدة البيانات.")
            return

        try:
            conn = sqlite3.connect(self.db_car_system_path)
            cursor = conn.cursor()
            
            # التأكد أولاً من وجود جدول الهوية الرئيسي لتفادي الأخطاء الباطنية
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Car_Master';")
            if not cursor.fetchone():
                conn.close()
                messagebox.showerror("خطأ في بنية البيانات", "❌ جدول السيارات الرئيسي (Car_Master) غير موجود في هذه الخزنة، يرجى حفظ مركبة واحدة على الأقل من كود الهوية أولاً!")
                return
            
            # الاستعلام المباشر والصريح بناءً على الحقول الدقيقة لملف الهوية
            sql_query = """
                SELECT admin_num, plate_num, driver_name, chassis_num, manufacturer_en, car_class, 
                       permit_end_year, permit_end_month, permit_end_day 
                FROM Car_Master 
                WHERE admin_num = ? OR plate_num = ? OR driver_name LIKE ?
            """
            cursor.execute(sql_query, (search_query, search_query, f"%{search_query}%"))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                admin_num, plate_num, driver_name, chassis_num, make_en, class_en, p_year, p_month, p_day = row
                
                # صياغة تاريخ انتهاء التصريح بشكل أنيق إن وجد
                permit_str = "غير محدد"
                if p_year and p_month and p_day:
                    permit_str = f"{p_year}-{p_month}-{p_day}"
                
                # تحديث واجهة الهوية فوراً بالبيانات المجلوبة
                self.lbl_val_driver.config(text=str(driver_name if driver_name else "غير متوفر"), fg="#22c55e")
                self.lbl_val_plate.config(text=str(plate_num if plate_num else "غير متوفر"), fg="#22c55e")
                self.lbl_val_admin.config(text=str(admin_num if admin_num else "غير متوفر"), fg="#22c55e")
                self.lbl_val_chassis.config(text=str(chassis_num if chassis_num else "غير متوفر"), fg="#38bdf8")
                self.lbl_val_unit_type.config(text=f"{make_en} - {class_en}".strip(" -"), fg="#38bdf8")
                self.lbl_val_permit.config(text=permit_str, fg="#38bdf8")
                
                self.loaded_admin_num = str(admin_num)
                self.loaded_driver = str(driver_name)
                self.loaded_plate = str(plate_num)
                self.is_car_loaded = True
                
                messagebox.showinfo("خوارزمية التنقيب الفاخرة", f"✅ نجح استدعاء البيانات ومطابقتها بنجاح!\n👈 السائق الحالي: {driver_name}")
                self.txt_km.focus_set()
            else:
                messagebox.showwarning("تنبيه المطابقة", f"❌ لم يتم العثور على أي مركبة تطابق المدخلات [{search_query}] في الخزنة الموحدة.")
                self.is_car_loaded = False
                
        except Exception as e:
            messagebox.showerror("خطأ الفحص الذاتي", f"فشلت خوارزمية التنقيب بسبب العائق الفني التالي:\n{e}")
            self.is_car_loaded = False

    def handle_type_switching_logic(self, event):
        for widget in self.dynamic_fields_panel.winfo_children(): widget.destroy()
        selected_type = self.combo_main_type.get()
        grid_frame = tk.Frame(self.dynamic_fields_panel, bg="#1e293b")
        grid_frame.pack(fill="x")
        self.dyn_widgets = {}

        if selected_type == "بطاريات":
            tk.Label(grid_frame, text="نوع البطارية:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=0, column=3, padx=10, pady=8, sticky="e")
            c_type = ttk.Combobox(grid_frame, values=["بطارية إلكترونية", "بطارية أسيد سائل"], font=("Arial", 11, "bold"), state="readonly", width=18, justify="center")
            c_type.grid(row=0, column=2, padx=10, pady=8)
            self.dyn_widgets["sub_type"] = c_type

            tk.Label(grid_frame, text="سعة البطارية:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=0, column=1, padx=10, pady=8, sticky="e")
            c_cap = ttk.Combobox(grid_frame, values=["45 أمبير", "60 أمبير", "70 أمبير", "80 أمبير"], font=("Arial", 11, "bold"), state="readonly", width=15, justify="center")
            c_cap.grid(row=0, column=0, padx=10, pady=8)
            self.dyn_widgets["capacity"] = c_cap

            tk.Label(grid_frame, text="ماركة البطارية:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=1, column=3, padx=10, pady=8, sticky="e")
            e_name = tk.Entry(grid_frame, font=("Arial", 11, "bold"), width=20, justify="center")
            e_name.grid(row=1, column=2, padx=10, pady=8)
            self.dyn_widgets["item_name"] = e_name

            tk.Label(grid_frame, text="اسم المورد الحركي:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=1, column=1, padx=10, pady=8, sticky="e")
            c_supp = ttk.Combobox(grid_frame, values=["محل بنشر معتمد", "من الوكيل مباشر", "شراء محلي عاجل"], font=("Arial", 11, "bold"), state="readonly", width=18, justify="center")
            c_supp.grid(row=1, column=0, padx=10, pady=8)
            self.dyn_widgets["supplier_name"] = c_supp

        elif selected_type == "إطارات":
            tk.Label(grid_frame, text="ماركة الإطار والكوشوك:", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=0, column=3, padx=10, pady=8, sticky="e")
            e_iname = tk.Entry(grid_frame, font=("Arial", 11, "bold"), width=20, justify="center")
            e_iname.grid(row=0, column=2, padx=10, pady=8)
            self.dyn_widgets["item_name"] = e_iname

            tk.Label(grid_frame, text="تاريخ الإنتاج (DOT):", font=("Arial", 11, "bold"), bg="#1e293b", fg="white").grid(row=0, column=1, padx=10, pady=8, sticky="e")
            e_idate = tk.Entry(grid_frame, font=("Arial", 11, "bold"), width=15, justify="center")
            e_idate.grid(row=0, column=0, padx=10, pady=8)
            self.dyn_widgets["prod_date"] = e_idate
        else:
            tk.Label(grid_frame, text="✅ نظام القيد المفتوح للسيارات مفعل، يرجى كتابة التفاصيل في الصندوق بالأسفل.", font=("Arial", 11, "bold"), bg="#1e293b", fg="#a7f3d0").pack(pady=10)

    def secure_save_car_maintenance_action(self):
        """🔒 اعتماد وحفظ التوثيق الفني لعملية الصيانة"""
        if not self.is_car_loaded:
            messagebox.showerror("قفل أمني للعملية", "❌ تنبيه: لا يمكن قيد صيانة الأعطال إلا بعد عمل استدعاء فني ناجح للسيارة أولاً!")
            return

        km = self.txt_km.get().strip()
        workshop = self.txt_workshop.get().strip()
        m_type = self.combo_main_type.get()
        fault_txt = self.txt_fault_details.get("1.0", tk.END).strip()

        if not km or not workshop or not m_type:
            messagebox.showwarning("بيانات ناقصة", "❌ يرجى ملء العداد الحالي للسيارة، اسم الورشة، واختيار صنف الاستبدال!")
            return

        item_name = self.dyn_widgets["item_name"].get().strip() if "item_name" in self.dyn_widgets else ""
        prod_date = self.dyn_widgets["prod_date"].get().strip() if "prod_date" in self.dyn_widgets else ""
        sub_type = self.dyn_widgets["sub_type"].get().strip() if "sub_type" in self.dyn_widgets else ""
        capacity = self.dyn_widgets["capacity"].get().strip() if "capacity" in self.dyn_widgets else ""
        supplier_name = self.dyn_widgets["supplier_name"].get().strip() if "supplier_name" in self.dyn_widgets else ""

        secret_password = simpledialog.askstring("تفويض الإدارة العليا 2600", "🔒 الرجاء إدخل الرقم السري المركزي لإتمام الحفظ رسميًا:", show="*")
        
        if secret_password == SECRET_PASSWORD:
            try:
                conn = sqlite3.connect(self.db_car_system_path)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Car_Maintenance_Logs 
                    (admin_num, plate_num, driver_name, km_reading, workshop_name, replacement_type, item_name, prod_date, sub_type, capacity, supplier_name, fault_details, log_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.loaded_admin_num, self.loaded_plate, self.loaded_driver, float(km), workshop, m_type, item_name, prod_date, sub_type, capacity, supplier_name, fault_txt, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("تم التوثيق الفاخر", f"🚀 نجحت عملية التوثيق وضمه إلى سجل صيانة السيارة رقم [{self.loaded_plate}] بنجاح!")
                
                # إعادة تصفير حقول الشاشة وتجهيزها للقيد التالي
                self.txt_km.delete(0, tk.END)
                self.txt_workshop.delete(0, tk.END)
                self.txt_fault_details.delete("1.0", tk.END)
                self.combo_main_type.set("")
                for widget in self.dynamic_fields_panel.winfo_children(): widget.destroy()
                
                tk.Label(self.dynamic_fields_panel, text="يرجى اختيار نوع الاستبدال لإظهار الحقول الحيوية الخاصة به مخصصة", font=("Arial", 11, "italic"), bg="#1e293b", fg="#94a3b8").pack(pady=10)
                
            except Exception as e:
                messagebox.showerror("خطأ حفظ الخزنة", f"حدثت مشكلة باطنية أثناء الحفظ في قاعدة البيانات: {e}")
        else:
            messagebox.showerror("فشل التفويض", "❌ الرقم السري المالي والبرمجي غير صحيح! تم إلغاء العملية.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarMaintenanceSuperPro2600(root)
    root.mainloop()