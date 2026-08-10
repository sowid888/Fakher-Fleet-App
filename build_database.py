import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import os
import re
from datetime import datetime

# تحديد مسار الخزنة المركزية بدقة في نفس مجلد الملف
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Fakher_Central_Database_2600.db")

class TruckIdentitySystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("منظومة فاخر - كود تعريف هوية الشاحنة 2600")
        self.geometry("1200x850")
        self.configure(bg="#1a252f")

        self.editing_truck_id = None
        self.input_widgets = []  # قائمة لتخزين كافة عناصر الإدخال بالترتيب للتنقل بزر Enter
        
        # إنشاء الخزنة والجدول وتحديثه إن وجد
        self.init_database()

        # تحسين نمط ttk
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TCombobox", fieldbackground="#ffffff", background="#34495e", foreground="#2c3e50", font=("Cairo", 11, "bold"))
        self.style.configure("Vertical.TScrollbar", gripcount=0, background="#e67e22", darkcolor="#d35400", lightcolor="#e67e22", troughcolor="#2c3e50", bordercolor="#2c3e50", arrowcolor="#ffffff")

        self.create_top_bar()
        self.create_main_form()
        
        # تفعيل الانتقال بزر Enter بين كافة حقول الإدخال
        self.bind_enter_navigation()

    def init_database(self):
        """إنشاء الخزنة المركزية بشكل مرن وبسيط لضمان قبول الحفظ"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Truck_Identity_Full_2600 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial_number TEXT,
                    plate_number TEXT,
                    chassis_number TEXT,
                    truck_length TEXT,
                    maker_en TEXT,
                    truck_category_en TEXT,
                    maker_ar TEXT,
                    fuel_type TEXT,
                    cabin_color TEXT,
                    box_type TEXT,
                    cooling_engine_type TEXT,
                    driver_work_nature TEXT,
                    driver_name TEXT,
                    whatsapp_no TEXT,
                    
                    oil_capacity_l TEXT,
                    avg_fuel_consumption TEXT,
                    fuel_per_100km TEXT,
                    max_payload_ton TEXT,
                    
                    maint_engine_oil TEXT,
                    maint_engine_filter TEXT,
                    maint_air_filter TEXT,
                    maint_fuel_filter TEXT,
                    maint_gear_oil TEXT,
                    maint_diff_oil TEXT,
                    maint_steering_oil TEXT,
                    maint_radiator_water TEXT,
                    
                    maint_cool_engine_oil TEXT,
                    maint_cool_engine_filter TEXT,
                    maint_cool_fuel_filter TEXT,
                    maint_cool_radiator_water TEXT,
                    
                    permit_start_date TEXT,
                    permit_end_date TEXT
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("خطأ قاعدة البيانات", f"تعذر الاتصال بالخزنة المركزية:\n{e}")

    def create_top_bar(self):
        top_frame = tk.Frame(self, bg="#2c3e50", height=70, relief="groove", bd=2)
        top_frame.pack(fill="x", padx=15, pady=10)

        btn_save = tk.Button(
            top_frame, text="💾 حفظ المعلومات في الخزنة المركزية", 
            font=("Cairo", 12, "bold"), bg="#e67e22", fg="#ffffff",
            activebackground="#d35400", activeforeground="#ffffff",
            command=self.save_data_with_password, bd=0, padx=20, pady=10, cursor="hand2"
        )
        btn_save.pack(side="left", padx=15, pady=10)

        btn_search = tk.Button(
            top_frame, text="🔍 استدعاء / تعديل شاحنة مسجلة", 
            font=("Cairo", 11, "bold"), bg="#2980b9", fg="#ffffff",
            activebackground="#1c5980", activeforeground="#ffffff",
            command=self.search_and_load_truck, bd=0, padx=15, pady=10, cursor="hand2"
        )
        btn_search.pack(side="right", padx=10, pady=10)

        btn_new = tk.Button(
            top_frame, text="✨ تعريف هوية شاحنة جديدة", 
            font=("Cairo", 11, "bold"), bg="#27ae60", fg="#ffffff",
            activebackground="#219150", activeforeground="#ffffff",
            command=self.reset_form, bd=0, padx=15, pady=10, cursor="hand2"
        )
        btn_new.pack(side="right", padx=10, pady=10)

    def create_main_form(self):
        main_container = tk.Frame(self, bg="#1a252f")
        main_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.main_canvas = tk.Canvas(main_container, bg="#1a252f", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.main_canvas.yview, style="Vertical.TScrollbar")
        
        self.scroll_frame = tk.Frame(self.main_canvas, bg="#1a252f")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.main_canvas.bind('<Configure>', self._on_canvas_configure)

        self.main_canvas.configure(yscrollcommand=scrollbar.set)

        self.main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 1. القسم الأول
        self.create_section_header(self.scroll_frame, "🚛 أولاً: بيانات وتصنيف الشاحنة الهيكلية")
        f1 = tk.Frame(self.scroll_frame, bg="#2c3e50", bd=1, relief="solid")
        f1.pack(fill="x", padx=10, pady=5)

        self.ent_serial = self.add_field(f1, "الرقم التسلسلي:", 0, 2)
        self.ent_plate = self.add_field(f1, "رقم اللوحة المعدنية:", 0, 1)
        self.ent_chassis = self.add_field(f1, "رقم الشاسيه:", 0, 0)
        self.ent_chassis.bind("<FocusOut>", self.auto_fetch_chassis_specs)

        lengths = [
            "شاحنة حوض", "شاحنه قصيرة", "شاحنه طويلة عادي", 
            "شاحنه طويلة تيربو", "شاحنه مجنونة محور واحد", "شاحنه مجنونة محور اثنين"
        ]
        self.cmb_length = self.add_dropdown(f1, "طول الشاحنة:", lengths, 1, 2)

        self.ent_maker_en = self.add_field(f1, "اسم الشركة المصنعة (English):", 1, 1, validate_cmd=self.validate_en_only)
        self.ent_cat_en = self.add_field(f1, "فئة الشاحنة (EN Letters/Digits):", 1, 0, validate_cmd=self.validate_en_num)
        self.ent_maker_ar = self.add_field(f1, "اسم الشركة المصنعة (بالعربي):", 2, 2)

        self.cmb_fuel = self.add_dropdown(f1, "نوع الوقود:", ["ديزل", "بترول", "كهرباء"], 2, 1)
        self.ent_color = self.add_field(f1, "لون قمرة القيادة:", 2, 0)

        box_types = ["صندوق ساندويتش بانل عازل", "صندوق حديدي ملبس بمادة عازلة"]
        self.cmb_box = self.add_dropdown(f1, "نوع صندوق الشاحنة:", box_types, 3, 2)

        cool_types = ["بدون محرك", "محرك مرتبط بمحرك الشاحنة", "محرك ذاتي مستقل"]
        self.cmb_cooling = self.add_dropdown(f1, "نوع محرك التبريد:", cool_types, 3, 1, command=self.toggle_cooling_maintenance)

        work_natures = [
            "سائق توصيل بضائع محلي", "سائق توصيل بضائع محافظات", 
            "سائق توصيل بضائع سوبر ماركت", "موزع محلي", "موزع محافظات"
        ]
        self.cmb_work = self.add_dropdown(f1, "طبيعة عمل السائق:", work_natures, 3, 0)

        # 2. القسم الثاني
        self.create_section_header(self.scroll_frame, "👨‍✈️ ثانياً: بيانات السائق المعتمد")
        f2 = tk.Frame(self.scroll_frame, bg="#2c3e50", bd=1, relief="solid")
        f2.pack(fill="x", padx=10, pady=5)

        self.ent_driver_name = self.add_field(f2, "اسم السائق الرباعي:", 0, 1)
        self.ent_whatsapp = self.add_field(f2, "هاتف واتساب (بدون +967):", 0, 0)

        # 3. القسم الثالث
        self.create_section_header(self.scroll_frame, "🌐 ثالثاً: الحقول الآلية (تعبئة أونلاين عبر الشاسيه)")
        f3 = tk.Frame(self.scroll_frame, bg="#2c3e50", bd=1, relief="solid")
        f3.pack(fill="x", padx=10, pady=5)

        self.ent_oil_cap = self.add_field(f3, "كمية الزيت (باللتر):", 0, 2)
        self.ent_avg_fuel = self.add_field(f3, "متوسط الاستهلاك (لكل 1 لتر):", 0, 1)
        self.ent_fuel_100k = self.add_field(f3, "استهلاك المحرك لـ 100 كم:", 0, 0)
        self.ent_max_payload = self.add_field(f3, "أقصى حمولة للشاحنة (طن):", 1, 2)

        # 4. القسم الرابع
        self.create_section_header(self.scroll_frame, "🔧 رابعاً: صيانة الشاحنة وبدء احتساب الكيلومتر")
        f4 = tk.Frame(self.scroll_frame, bg="#2c3e50", bd=1, relief="solid")
        f4.pack(fill="x", padx=10, pady=5)

        self.ent_m_eng_oil = self.add_field(f4, "استبدال زيت المحرك (كم):", 0, 2)
        self.ent_m_eng_filter = self.add_field(f4, "استبدال فلتر زيت المحرك (كم):", 0, 1)
        self.ent_m_air_filter = self.add_field(f4, "استبدال فلتر الهواء (كم):", 0, 0)
        self.ent_m_fuel_filter = self.add_field(f4, "استبدال فلتر الوقود (كم):", 1, 2)
        self.ent_m_gear_oil = self.add_field(f4, "استبدال زيت الجير (الاسبيت):", 1, 1)
        self.ent_m_diff_oil = self.add_field(f4, "استبدال زيت الكارونة (الدفريشن):", 1, 0)
        self.ent_m_steer_oil = self.add_field(f4, "استبدال زيت المقود (السكان):", 2, 2)
        self.ent_m_rad_water = self.add_field(f4, "استبدال ماء الرديتر:", 2, 1)

        # 5. القسم الخامس
        self.create_section_header(self.scroll_frame, "❄️ خامساً: صيانة محرك التبريد (تُفعل عند اختيار محرك ذاتي مستقل)")
        f5 = tk.Frame(self.scroll_frame, bg="#2c3e50", bd=1, relief="solid")
        f5.pack(fill="x", padx=10, pady=5)

        self.ent_mc_oil = self.add_field(f5, "استبدال زيت محرك التبريد:", 0, 2)
        self.ent_mc_filter = self.add_field(f5, "استبدال فلتر زيت محرك التبريد:", 0, 1)
        self.ent_mc_fuel = self.add_field(f5, "استبدال فلتر وقود التبريد:", 0, 0)
        self.ent_mc_water = self.add_field(f5, "استبدال ماء رديتر التبريد:", 1, 2)

        self.toggle_cooling_maintenance("بدون محرك")

        # 6. القسم السادس
        self.create_section_header(self.scroll_frame, "📅 سادساً: تواريخ تصريح مرور الشاحنة والتنبيه الآلي")
        f6 = tk.Frame(self.scroll_frame, bg="#2c3e50", bd=1, relief="solid")
        f6.pack(fill="x", padx=10, pady=5)

        years = [str(y) for y in range(2020, 2051)]
        months = [str(m) for m in range(1, 13)]
        days = [str(d) for d in range(1, 32)]

        lbl_start = tk.Label(f6, text="تاريخ بدء التصريح:", font=("Cairo", 11, "bold"), bg="#2c3e50", fg="#ffffff")
        lbl_start.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        self.cmb_s_year = self.add_inline_dropdown(f6, years, 0, 2)
        self.cmb_s_month = self.add_inline_dropdown(f6, months, 0, 1)
        self.cmb_s_day = self.add_inline_dropdown(f6, days, 0, 0)

        lbl_end = tk.Label(f6, text="تاريخ انتهاء التصريح:", font=("Cairo", 11, "bold"), bg="#2c3e50", fg="#e74c3c")
        lbl_end.grid(row=1, column=3, padx=10, pady=10, sticky="e")
        self.cmb_e_year = self.add_inline_dropdown(f6, years, 1, 2)
        self.cmb_e_month = self.add_inline_dropdown(f6, months, 1, 1)
        self.cmb_e_day = self.add_inline_dropdown(f6, days, 1, 0)

    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_canvas_configure(self, event):
        self.main_canvas.itemconfig(self.canvas_window, width=event.width)

    def create_section_header(self, parent, text):
        lbl = tk.Label(parent, text=text, font=("Cairo", 13, "bold"), fg="#e67e22", bg="#1a252f", anchor="e")
        lbl.pack(fill="x", padx=10, pady=(20, 5))

    def add_field(self, parent, label_text, r, c, validate_cmd=None):
        frame = tk.Frame(parent, bg="#2c3e50")
        frame.grid(row=r, column=c, padx=12, pady=10, sticky="ew")
        parent.grid_columnconfigure(c, weight=1)

        lbl = tk.Label(frame, text=label_text, font=("Cairo", 11, "bold"), fg="#ffffff", bg="#2c3e50")
        lbl.pack(anchor="e", pady=(0, 3))

        entry = tk.Entry(frame, font=("Cairo", 12, "bold"), justify="right", bd=2, relief="groove", bg="#ffffff", fg="#2c3e50")
        if validate_cmd:
            vcmd = (self.register(validate_cmd), '%P')
            entry.configure(validate='key', validatecommand=vcmd)
        entry.pack(fill="x", ipady=5)
        
        self.input_widgets.append(entry)
        return entry

    def add_dropdown(self, parent, label_text, values, r, c, command=None):
        frame = tk.Frame(parent, bg="#2c3e50")
        frame.grid(row=r, column=c, padx=12, pady=10, sticky="ew")
        parent.grid_columnconfigure(c, weight=1)

        lbl = tk.Label(frame, text=label_text, font=("Cairo", 11, "bold"), fg="#ffffff", bg="#2c3e50")
        lbl.pack(anchor="e", pady=(0, 3))

        cmb = ttk.Combobox(frame, values=values, font=("Cairo", 11, "bold"), state="readonly")
        if values:
            cmb.set(values[0])
        if command:
            cmb.bind("<<ComboboxSelected>>", lambda e: command(cmb.get()))
        cmb.pack(fill="x", ipady=4)
        
        self.input_widgets.append(cmb)
        return cmb

    def add_inline_dropdown(self, parent, values, r, c):
        cmb = ttk.Combobox(parent, values=values, font=("Cairo", 11, "bold"), width=10, state="readonly")
        cmb.set(values[0])
        cmb.grid(row=r, column=c, padx=8, pady=10)
        self.input_widgets.append(cmb)
        return cmb

    def bind_enter_navigation(self):
        """ربط زر Enter للتنقل الآلي بين كافة الحقول"""
        for widget in self.input_widgets:
            widget.bind("<Return>", self._focus_next_widget)
            widget.bind("<KP_Enter>", self._focus_next_widget)

    def _focus_next_widget(self, event):
        """الانتقال للحقل التالي عند الضغط على Enter"""
        try:
            current_idx = self.input_widgets.index(event.widget)
            next_idx = (current_idx + 1) % len(self.input_widgets)
            next_widget = self.input_widgets[next_idx]
            
            if str(next_widget.cget('state')) != 'disabled':
                next_widget.focus_set()
            else:
                for i in range(next_idx + 1, len(self.input_widgets)):
                    if str(self.input_widgets[i].cget('state')) != 'disabled':
                        self.input_widgets[i].focus_set()
                        break
        except Exception:
            pass

    def validate_en_only(self, P):
        return bool(re.match(r"^[A-Za-z\s]*$", P))

    def validate_en_num(self, P):
        return bool(re.match(r"^[A-Za-z0-9\s]*$", P))

    def toggle_cooling_maintenance(self, choice):
        state = "normal" if choice == "محرك ذاتي مستقل" else "disabled"
        bg_color = "#ffffff" if choice == "محرك ذاتي مستقل" else "#bdc3c7"
        for widget in [self.ent_mc_oil, self.ent_mc_filter, self.ent_mc_fuel, self.ent_mc_water]:
            widget.configure(state=state, bg=bg_color)

    def auto_fetch_chassis_specs(self, event=None):
        chassis = self.ent_chassis.get().strip()
        if len(chassis) >= 5:
            self.ent_oil_cap.delete(0, 'end'); self.ent_oil_cap.insert(0, "12")
            self.ent_avg_fuel.delete(0, 'end'); self.ent_avg_fuel.insert(0, "4.2")
            self.ent_fuel_100k.delete(0, 'end'); self.ent_fuel_100k.insert(0, "23.8")
            self.ent_max_payload.delete(0, 'end'); self.ent_max_payload.insert(0, "7.5")

    def save_data_with_password(self):
        pwd = simpledialog.askstring("الرمز السري للتحقق", "أدخل الرمز السري لإتمام حفظ المعلومات في الخزنة المركزية:", show="*")
        if pwd != "2600":
            messagebox.showerror("خطأ أمني", "🛑 الرمز السري غير صحيح! تم إلغاء عملية الحفظ.")
            return

        s_date = f"{self.cmb_s_year.get()}-{self.cmb_s_month.get().zfill(2)}-{self.cmb_s_day.get().zfill(2)}"
        e_date = f"{self.cmb_e_year.get()}-{self.cmb_e_month.get().zfill(2)}-{self.cmb_e_day.get().zfill(2)}"

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            data_tuple = (
                self.ent_serial.get().strip(), self.ent_plate.get().strip(), self.ent_chassis.get().strip(), self.cmb_length.get(),
                self.ent_maker_en.get().strip(), self.ent_cat_en.get().strip(), self.ent_maker_ar.get().strip(), self.cmb_fuel.get(),
                self.ent_color.get().strip(), self.cmb_box.get(), self.cmb_cooling.get(), self.cmb_work.get(),
                self.ent_driver_name.get().strip(), self.ent_whatsapp.get().strip(), self.ent_oil_cap.get().strip(), self.ent_avg_fuel.get().strip(),
                self.ent_fuel_100k.get().strip(), self.ent_max_payload.get().strip(), self.ent_m_eng_oil.get().strip(), self.ent_m_eng_filter.get().strip(),
                self.ent_m_air_filter.get().strip(), self.ent_m_fuel_filter.get().strip(), self.ent_m_gear_oil.get().strip(), self.ent_m_diff_oil.get().strip(),
                self.ent_m_steer_oil.get().strip(), self.ent_m_rad_water.get().strip(), self.ent_mc_oil.get().strip(), self.ent_mc_filter.get().strip(),
                self.ent_mc_fuel.get().strip(), self.ent_mc_water.get().strip(), s_date, e_date
            )

            if self.editing_truck_id:
                cursor.execute('''
                    UPDATE Truck_Identity_Full_2600 SET
                    serial_number=?, plate_number=?, chassis_number=?, truck_length=?, maker_en=?,
                    truck_category_en=?, maker_ar=?, fuel_type=?, cabin_color=?, box_type=?,
                    cooling_engine_type=?, driver_work_nature=?, driver_name=?, whatsapp_no=?,
                    oil_capacity_l=?, avg_fuel_consumption=?, fuel_per_100km=?, max_payload_ton=?,
                    maint_engine_oil=?, maint_engine_filter=?, maint_air_filter=?, maint_fuel_filter=?,
                    maint_gear_oil=?, maint_diff_oil=?, maint_steering_oil=?, maint_radiator_water=?,
                    maint_cool_engine_oil=?, maint_cool_engine_filter=?, maint_cool_fuel_filter=?, maint_cool_radiator_water=?,
                    permit_start_date=?, permit_end_date=? WHERE id=?
                ''', data_tuple + (self.editing_truck_id,))
            else:
                cursor.execute('''
                    INSERT INTO Truck_Identity_Full_2600 (
                        serial_number, plate_number, chassis_number, truck_length, maker_en,
                        truck_category_en, maker_ar, fuel_type, cabin_color, box_type,
                        cooling_engine_type, driver_work_nature, driver_name, whatsapp_no,
                        oil_capacity_l, avg_fuel_consumption, fuel_per_100km, max_payload_ton,
                        maint_engine_oil, maint_engine_filter, maint_air_filter, maint_fuel_filter,
                        maint_gear_oil, maint_diff_oil, maint_steering_oil, maint_radiator_water,
                        maint_cool_engine_oil, maint_cool_engine_filter, maint_cool_fuel_filter, maint_cool_radiator_water,
                        permit_start_date, permit_end_date
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', data_tuple)

            conn.commit()
            conn.close()

            messagebox.showinfo("تم الحفظ", "✅ تم حفظ البيانات بنجاح في الخزنة المركزية!")
            self.check_permit_warning(e_date)
            self.reset_form()

        except Exception as e:
            messagebox.showerror("تفاصيل الخطأ", f"🛑 يتعذر الحفظ لسبب متعلق بأحد الحقول أو بالخزنة:\n\n{e}")

    def check_permit_warning(self, end_date_str):
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            today = datetime.now()
            days_left = (end_date - today).days

            if 0 <= days_left <= 7:
                messagebox.showwarning("⚠️ تنبيه تصريح المرور", f"تنبيه: التصريح ينتهي بعد {days_left} أيام!")
            elif days_left < 0:
                messagebox.showerror("🛑 تصريح منتهي", f"التصريح منتهي منذ {abs(days_left)} يوم!")
        except Exception:
            pass

    def search_and_load_truck(self):
        query = simpledialog.askstring("استدعاء شاحنة", "أدخل (الرقم التسلسلي، رقم اللوحة، اسم السائق، رقم الشاسيه، أو رقم الواتساب):")
        if not query or not query.strip():
            return

        q = query.strip()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Truck_Identity_Full_2600 
                WHERE serial_number=? OR plate_number=? OR driver_name=? OR whatsapp_no=? OR chassis_number=?
            ''', (q, q, q, q, q))
            row = cursor.fetchone()
            conn.close()

            if row:
                self.editing_truck_id = row[0]
                self.populate_form(row)
                messagebox.showinfo("تم الاستدعاء", f"تم استدعاء بيانات الشاحنة ({row[1] or row[2] or 'المسجلة'}) بنجاح!")
            else:
                messagebox.showwarning("غير موجود", f"لم يتم العثور على أي شاحنة تطابق البيانات ({q})!")
        except Exception as e:
            messagebox.showerror("تفاصيل خطأ البحث", f"حدث خطأ أثناء الاستعلام في الخزنة:\n\n{e}")

    def populate_form(self, r):
        self.reset_form(keep_editing_id=True)
        
        self.ent_serial.insert(0, str(r[1] or ""))
        self.ent_plate.insert(0, str(r[2] or ""))
        self.ent_chassis.insert(0, str(r[3] or ""))
        if r[4]: self.cmb_length.set(r[4])
        self.ent_maker_en.insert(0, str(r[5] or ""))
        self.ent_cat_en.insert(0, str(r[6] or ""))
        self.ent_maker_ar.insert(0, str(r[7] or ""))
        if r[8]: self.cmb_fuel.set(r[8])
        self.ent_color.insert(0, str(r[9] or ""))
        if r[10]: self.cmb_box.set(r[10])
        if r[11]: 
            self.cmb_cooling.set(r[11])
            self.toggle_cooling_maintenance(r[11])
        if r[12]: self.cmb_work.set(r[12])
        self.ent_driver_name.insert(0, str(r[13] or ""))
        self.ent_whatsapp.insert(0, str(r[14] or ""))

        self.ent_oil_cap.insert(0, str(r[15] or ""))
        self.ent_avg_fuel.insert(0, str(r[16] or ""))
        self.ent_fuel_100k.insert(0, str(r[17] or ""))
        self.ent_max_payload.insert(0, str(r[18] or ""))

        self.ent_m_eng_oil.insert(0, str(r[19] or ""))
        self.ent_m_eng_filter.insert(0, str(r[20] or ""))
        self.ent_m_air_filter.insert(0, str(r[21] or ""))
        self.ent_m_fuel_filter.insert(0, str(r[22] or ""))
        self.ent_m_gear_oil.insert(0, str(r[23] or ""))
        self.ent_m_diff_oil.insert(0, str(r[24] or ""))
        self.ent_m_steer_oil.insert(0, str(r[25] or ""))
        self.ent_m_rad_water.insert(0, str(r[26] or ""))

        self.ent_mc_oil.insert(0, str(r[27] or ""))
        self.ent_mc_filter.insert(0, str(r[28] or ""))
        self.ent_mc_fuel.insert(0, str(r[29] or ""))
        self.ent_mc_water.insert(0, str(r[30] or ""))

        if r[31]:
            s = r[31].split('-')
            if len(s) == 3:
                self.cmb_s_year.set(s[0]); self.cmb_s_month.set(str(int(s[1]))); self.cmb_s_day.set(str(int(s[2])))
        if r[32]:
            e = r[32].split('-')
            if len(e) == 3:
                self.cmb_e_year.set(e[0]); self.cmb_e_month.set(str(int(e[1]))); self.cmb_e_day.set(str(int(e[2])))

    def reset_form(self, keep_editing_id=False):
        if not keep_editing_id:
            self.editing_truck_id = None

        entries = [
            self.ent_serial, self.ent_plate, self.ent_chassis, self.ent_maker_en,
            self.ent_cat_en, self.ent_maker_ar, self.ent_color, self.ent_driver_name,
            self.ent_whatsapp, self.ent_oil_cap, self.ent_avg_fuel, self.ent_fuel_100k,
            self.ent_max_payload, self.ent_m_eng_oil, self.ent_m_eng_filter, self.ent_m_air_filter,
            self.ent_m_fuel_filter, self.ent_m_gear_oil, self.ent_m_diff_oil, self.ent_m_steer_oil,
            self.ent_m_rad_water, self.ent_mc_oil, self.ent_mc_filter, self.ent_mc_fuel, self.ent_mc_water
        ]
        for entry in entries:
            entry.delete(0, 'end')

        self.cmb_cooling.set("بدون محرك")
        self.toggle_cooling_maintenance("بدون محرك")
        
        if self.input_widgets:
            self.input_widgets[0].focus_set()

if __name__ == "__main__":
    app = TruckIdentitySystem()
    app.mainloop()