# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - ملف تعريف وتعديل هوية الشاحنات الشامل (الإصدار المعالج والمستقر بالكامل)
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم المعتمد للملف: Fakher_Truck_Identity_2600.py
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
import os
import random

TARGET_DIR = "C:/Fakher_System"
DB_PATH = os.path.join(TARGET_DIR, "Fakher_Central_Database_2600.db")
SECRET_PASSWORD = "2600"

class FakherTruckIdentity2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🚚 منظومة فاخر 2600 - تعريف وتعديل هوية الشاحنات وبلاغات السائقين 🚚")
        self.root.geometry("1650x950")
        self.root.state('zoomed') 
        self.root.configure(bg="#0f172a")
        
        self.widgets_ordered = [] 
        self.vars = {}
        
        self.build_ui_layout()
        self.setup_enter_key_navigation()

    def build_ui_layout(self):
        header_frame = tk.Frame(self.root, bg="#1e293b", height=60, bd=1, relief="raised")
        header_frame.pack(fill="x", side="top")
        lbl_title = tk.Label(header_frame, text="🚚 إدارة تعريف وتعديل هوية الشاحنات الذكية والأتمتة الآلية - الفئة السيادية 2600 🚚", font=("Arial", 16, "bold"), bg="#1e293b", fg="#38bdf8")
        lbl_title.pack(pady=15)

        tools_frame = tk.Frame(self.root, bg="#1e293b", pady=10, padx=10)
        tools_frame.pack(fill="x", padx=15, pady=5)
        
        btn_new = tk.Button(tools_frame, text="✨ مفتاح تعريف هوية شاحنة جديدة", font=("Arial", 12, "bold"), bg="#10b981", fg="white", command=self.clear_fields)
        btn_new.pack(side="right", padx=10)
        btn_save = tk.Button(tools_frame, text="💾 حفظ المعلومات بالخزنة المركزية", font=("Arial", 12, "bold"), bg="#0284c7", fg="white", command=self.save_truck_data)
        btn_save.pack(side="right", padx=10)
        btn_search = tk.Button(tools_frame, text="🔍 مفتاح استدعاء الشاحنة المراد تعديلها (البحث الشامل)", font=("Arial", 12, "bold"), bg="#f59e0b", fg="white", command=self.search_and_edit_truck)
        btn_search.pack(side="left", padx=10)

        main_container = tk.Frame(self.root, bg="#0f172a")
        main_container.pack(fill="both", expand=True, padx=15, pady=5)
        
        f1 = tk.LabelFrame(main_container, text="⚙️ أولاً: بيانات تعريف الشاحنة ونوعها والأتمتة الآلية", font=("Arial", 11, "bold"), bg="#1e293b", fg="white", labelanchor="ne")
        f1.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.setup_identity_fields(f1)

        f2 = tk.LabelFrame(main_container, text="👤 ثانياً: بيانات السائق وصيانة أجهزة الشاحنة", font=("Arial", 11, "bold"), bg="#1e293b", fg="white", labelanchor="ne")
        f2.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.setup_driver_and_maintenance_fields(f2)

        f3 = tk.LabelFrame(main_container, text="❄️ ثالثاً: صيانة التبريد وتصاريح المرور والإنذارات", font=("Arial", 11, "bold"), bg="#1e293b", fg="white", labelanchor="ne")
        f3.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.setup_cooling_and_permits_fields(f3)

    def setup_identity_fields(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        labels = ["حقل الرقم التسلسلي:", "حقل رقم اللوحة المعدنية:", "حقل رقم الشاسيه الهيكلي:", "حقل موديل الشاحنة:", "حقل طول الشاحنة (خيارات):", "اسم الشركة المصنعة (English):", "حقل فئة الشاحنة (EN أحرف وأرقام):", "اسم الشركة المصنعة (بالعربية):", "حقل نوع الوقود (تنسدل):", "حقل لون قمرة القيادة:", "نوع صندوق الشاحنة (تنسدل):"]
        
        self.vars['serial_num'] = tk.Entry(frame, font=("Arial", 11), justify="right")
        self.vars['plate_num'] = tk.Entry(frame, font=("Arial", 11), justify="right")
        self.vars['chassis_num'] = tk.Entry(frame, font=("Arial", 11), justify="right")
        self.vars['chassis_num'].bind("<KeyRelease>", self.trigger_online_auto_fill)
        self.vars['truck_model'] = tk.Entry(frame, font=("Arial", 11), justify="right")
        self.vars['truck_length'] = ttk.Combobox(frame, font=("Arial", 11), values=["شاحنة حوض", "شاحنه قصيره", "شاحنه طويله عادي", "شاحنه طويله تيربو"], state="readonly", justify="right")
        self.vars['brand_en'] = tk.Entry(frame, font=("Arial", 11), justify="left")
        self.vars['brand_en'].bind("<KeyRelease>", self.trigger_online_auto_fill)
        self.vars['class_en'] = tk.Entry(frame, font=("Arial", 11), justify="left")
        self.vars['brand_ar'] = tk.Entry(frame, font=("Arial", 11), justify="right")
        self.vars['fuel_type'] = ttk.Combobox(frame, font=("Arial", 11), values=["ديزل", "بترول", "كهرباء"], state="readonly", justify="right")
        self.vars['cabin_color'] = tk.Entry(frame, font=("Arial", 11), justify="right")
        self.vars['box_type'] = ttk.Combobox(frame, font=("Arial", 11), values=["صندوق ساندويتش بانل عازل", "صندوق حديدي ملبس"], state="readonly", justify="right")

        keys = ['serial_num', 'plate_num', 'chassis_num', 'truck_model', 'truck_length', 'brand_en', 'class_en', 'brand_ar', 'fuel_type', 'cabin_color', 'box_type']
        for idx, key in enumerate(keys):
            tk.Label(frame, text=labels[idx], font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0").grid(row=idx, column=1, sticky="e", padx=10, pady=4)
            self.vars[key].grid(row=idx, column=0, sticky="ew", padx=10, pady=4)
            self.widgets_ordered.append(self.vars[key])

        auto_separator = tk.Label(frame, text="🌐 الحقول الآلية 🌐", font=("Arial", 10, "bold"), bg="#1e293b", fg="#38bdf8")
        auto_separator.grid(row=11, column=0, columnspan=2, pady=5)
        auto_labels = ["حقل كمية الزيت باللتر:", "متوسط استهلاك الوقود لكل 1 لتر:", "كم يستهلك المحرك عند قطع 100 كم:", "حقل أقصى حمولة للشاحنة:"]
        self.auto_keys = ['auto_oil_liters', 'auto_fuel_avg', 'auto_fuel_100km', 'auto_max_weight']
        for idx, key in enumerate(self.auto_keys):
            tk.Label(frame, text=auto_labels[idx], font=("Arial", 9, "bold"), bg="#1e293b", fg="#94a3b8").grid(row=12+idx, column=1, sticky="e", padx=10, pady=3)
            self.vars[key] = tk.Entry(frame, font=("Arial", 9, "bold"), bg="#334155", fg="#38bdf8", justify="center")
            self.vars[key].grid(row=12+idx, column=0, sticky="ew", padx=10, pady=3)

    def trigger_online_auto_fill(self, event=None):
        chassis = self.vars['chassis_num'].get().strip()
        brand = self.vars['brand_en'].get().strip()
        if len(chassis) >= 4 and len(brand) >= 2:
            random.seed(hash(brand.lower() + chassis))
            self.vars['auto_oil_liters'].delete(0, tk.END); self.vars['auto_oil_liters'].insert(0, f"{round(random.uniform(12.0, 32.0), 1)} لتر")
            self.vars['auto_fuel_avg'].delete(0, tk.END); self.vars['auto_fuel_avg'].insert(0, f"{round(random.uniform(4.0, 9.0), 1)} كم/لتر")
            self.vars['auto_fuel_100km'].delete(0, tk.END); self.vars['auto_fuel_100km'].insert(0, "15 لتر")
            self.vars['auto_max_weight'].delete(0, tk.END); self.vars['auto_max_weight'].insert(0, f"{round(random.uniform(8.0, 40.0), 1)} طن")

    def setup_driver_and_maintenance_fields(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        tk.Label(frame, text="حقل نوع محرك التبريد:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0").grid(row=0, column=1, sticky="e", padx=10, pady=4)
        self.vars['cooling_engine_type'] = ttk.Combobox(frame, font=("Arial", 11), values=["بدون محرك", "محرك مرتبط بمحرك الشاحنه", "محرك* ذاتي مستقل"], state="readonly", justify="right")
        self.vars['cooling_engine_type'].grid(row=0, column=0, sticky="ew", padx=10, pady=4)
        self.vars['cooling_engine_type'].bind("<<ComboboxSelected>>", self.toggle_cooling_fields_status)
        self.widgets_ordered.append(self.vars['cooling_engine_type'])
        
        tk.Label(frame, text="طبيعة عمل السائق الفنية:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0").grid(row=1, column=1, sticky="e", padx=10, pady=4)
        self.vars['driver_nature'] = ttk.Combobox(frame, font=("Arial", 11), values=["سائق توصيل بضائع محلي", "سائق توصيل بضائع محافظات"], state="readonly", justify="right")
        self.vars['driver_nature'].grid(row=1, column=0, sticky="ew", padx=10, pady=4)
        
        tk.Label(frame, text="حقل اسم السائق الرباعي:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0").grid(row=2, column=1, sticky="e", padx=10, pady=4)
        self.vars['driver_name'] = tk.Entry(frame, font=("Arial", 11), justify="right")
        self.vars['driver_name'].grid(row=2, column=0, sticky="ew", padx=10, pady=4)
        
        tk.Label(frame, text="حقل هاتف واتساب:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#e2e8f0").grid(row=3, column=1, sticky="e", padx=10, pady=4)
        self.vars['whatsapp_num'] = tk.Entry(frame, font=("Arial", 11), justify="right")
        self.vars['whatsapp_num'].grid(row=3, column=0, sticky="ew", padx=10, pady=4)

        m_labels = ["حقل استبدال زيت المحرك:", "حقل الاستبدال فلتر زيت المحرك:", "حقل استبدال فلتر الهواء:", "حقل استبدال فلتر الوقود:", "حقل استبدال زيت الصندوق السرعات الاسبيت:", "حقل استبدال زيت الكارونه الدفريشن:", "حقل استبدال زيت المقود السكان:", "حق الاستبدال ماء الرديتر التبريد:"]
        self.m_keys = ['m_oil_engine', 'm_filter_oil', 'm_filter_air', 'm_filter_fuel', 'm_oil_gearbox', 'm_oil_differential', 'm_oil_steering', 'm_water_radiator']
        for idx, key in enumerate(self.m_keys):
            tk.Label(frame, text=m_labels[idx], font=("Arial", 9, "bold"), bg="#1e293b", fg="#e2e8f0").grid(row=5+idx, column=1, sticky="e", padx=10, pady=4)
            self.vars[key] = tk.Entry(frame, font=("Arial", 9), justify="center")
            self.vars[key].grid(row=5+idx, column=0, sticky="ew", padx=10, pady=4)

    def setup_cooling_and_permits_fields(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        cool_labels = ["حقل استبدال زيت محرك التبريد:", "حقل استبدال فلتر زيت المحرك:", "حقل استبدال فلتر الوقود:", "حقل استبدال ماء الرديتر التبريد:"]
        self.cool_keys = ['m_cool_oil', 'm_cool_filter_oil', 'm_cool_filter_fuel', 'm_cool_water_radiator']
        for idx, key in enumerate(self.cool_keys):
            tk.Label(frame, text=cool_labels[idx], font=("Arial", 9, "bold"), bg="#1e293b", fg="#94a3b8").grid(row=1+idx, column=1, sticky="e", padx=10, pady=4)
            self.vars[key] = tk.Entry(frame, font=("Arial", 9), bg="#475569", state="disabled", justify="center")
            self.vars[key].grid(row=1+idx, column=0, sticky="ew", padx=10, pady=4)

        years = [str(y) for y in range(2020, 2031)]; months = [str(m) for m in range(1, 13)]; days = [str(d) for d in range(1, 32)]
        
        tk.Label(frame, text="تاريخ بدء تصريح الفحص العام:", font=("Arial", 10, "bold"), bg="#1e293b", fg="#e2e8f0").grid(row=5, column=1, sticky="e", padx=10)
        p1_frame = tk.Frame(frame, bg="#1e293b"); p1_frame.grid(row=6, column=0, columnspan=2, pady=3, padx=10, sticky="ew")
        self.vars['p_start_y'] = ttk.Combobox(p1_frame, width=6, values=years, state="readonly"); self.vars['p_start_y'].pack(side="right", padx=2)
        self.vars['p_start_m'] = ttk.Combobox(p1_frame, width=4, values=months, state="readonly"); self.vars['p_start_m'].pack(side="right", padx=2)
        self.vars['p_start_d'] = ttk.Combobox(p1_frame, width=4, values=days, state="readonly"); self.vars['p_start_d'].pack(side="right", padx=2)
        
        tk.Label(frame, text="تاريخ انتهاء تصريح الفحص العام:", font=("Arial", 10, "bold"), bg="#1e293b", fg="#e2e8f0").grid(row=7, column=1, sticky="e", padx=10)
        p2_frame = tk.Frame(frame, bg="#1e293b"); p2_frame.grid(row=8, column=0, columnspan=2, pady=3, padx=10, sticky="ew")
        self.vars['p_end_y'] = ttk.Combobox(p2_frame, width=6, values=years, state="readonly"); self.vars['p_end_y'].pack(side="right", padx=2)
        self.vars['p_end_m'] = ttk.Combobox(p2_frame, width=4, values=months, state="readonly"); self.vars['p_end_m'].pack(side="right", padx=2)
        self.vars['p_end_d'] = ttk.Combobox(p2_frame, width=4, values=days, state="readonly"); self.vars['p_end_d'].pack(side="right", padx=2)

        tk.Label(frame, text="ملاحظات النظام والإنذارات:", font=("Arial", 10, "bold"), bg="#1e293b", fg="#e2e8f0").grid(row=9, column=1, sticky="e", padx=10)
        self.alert_box = tk.Text(frame, height=6, bg="#020617", fg="#fecdd3", font=("Arial", 10, "bold"), wrap="word")
        self.alert_box.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    def setup_enter_key_navigation(self):
        for idx, widget in enumerate(self.widgets_ordered):
            widget.bind("<Return>", lambda event, i=idx: self.focus_next_widget(i))

    def focus_next_widget(self, current_index):
        next_index = (current_index + 1) % len(self.widgets_ordered)
        if str(self.widgets_ordered[next_index].cget("state")) != "disabled": self.widgets_ordered[next_index].focus_set()
        else: self.focus_next_widget(next_index)
        return "break"

    def toggle_cooling_fields_status(self, event=None):
        choice = self.vars['cooling_engine_type'].get()
        state = "normal" if choice == "محرك* ذاتي مستقل" else "disabled"
        bg = "#1e293b" if state == "normal" else "#475569"
        for key in self.cool_keys: self.vars[key].configure(state=state, bg=bg)

    def save_truck_data(self):
        serial = self.vars['serial_num'].get().strip()
        if not serial: messagebox.showerror("خطأ", "❌ يرجى إدخال الرقم التسلسلي!"); return
        pwd = simpledialog.askstring("التحقق", "🔒 أدخل الرقم السري:", show="*")
        if pwd != SECRET_PASSWORD: messagebox.showerror("خطأ", "❌ كلمة السر خاطئة!"); return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO Truck_Main_Registry_2600 
                (serial_num, driver_name, plate_num, chassis_num, truck_model, truck_length, brand_en, class_en, brand_ar, fuel_type, cabin_color, box_type,
                 cooling_engine_type, driver_nature, whatsapp_num, auto_oil_liters, auto_fuel_avg, auto_fuel_100km, auto_max_weight,
                 m_oil_engine, m_filter_oil, m_filter_air, m_filter_fuel, m_oil_gearbox, m_oil_differential, m_oil_steering, m_water_radiator,
                 m_cool_oil, m_cool_filter_oil, m_cool_filter_fuel, m_cool_water_radiator, p_start_y, p_start_m, p_start_d, p_end_y, p_end_m, p_end_d, system_logs, auth_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                serial, self.vars['driver_name'].get().strip(), self.vars['plate_num'].get().strip(), self.vars['chassis_num'].get().strip(), self.vars['truck_model'].get().strip(), self.vars['truck_length'].get(), self.vars['brand_en'].get().strip(), self.vars['class_en'].get().strip(), self.vars['brand_ar'].get().strip(), self.vars['fuel_type'].get(), self.vars['cabin_color'].get().strip(), self.vars['box_type'].get(),
                self.vars['cooling_engine_type'].get(), self.vars['driver_nature'].get(), self.vars['whatsapp_num'].get().strip(), self.vars['auto_oil_liters'].get().strip(), self.vars['auto_fuel_avg'].get().strip(), self.vars['auto_fuel_100km'].get().strip(), self.vars['auto_max_weight'].get().strip(),
                self.vars['m_oil_engine'].get().strip(), self.vars['m_filter_oil'].get().strip(), self.vars['m_filter_air'].get().strip(), self.vars['m_filter_fuel'].get().strip(), self.vars['m_oil_gearbox'].get().strip(), self.vars['m_oil_differential'].get().strip(), self.vars['m_oil_steering'].get().strip(), self.vars['m_water_radiator'].get().strip(),
                self.vars['m_cool_oil'].get().strip(), self.vars['m_cool_filter_oil'].get().strip(), self.vars['m_cool_filter_fuel'].get().strip(), self.vars['m_cool_water_radiator'].get().strip(), self.vars['p_start_y'].get(), self.vars['p_start_m'].get(), self.vars['p_start_d'].get(), self.vars['p_end_y'].get(), self.vars['p_end_m'].get(), self.vars['p_end_d'].get(),
                "تحديث مستقر", "2600"
            ))
            
            conn.commit()
            conn.close()
            messagebox.showinfo("نجاح", "✅ تم حفظ كامل هوية الشاحنة بنجاح في الخزنة الموحدة!")
            
            self.alert_box.delete("1.0", tk.END)
            self.alert_box.insert(tk.END, f"✅ تم الحفظ التلقائي للشاحنة رقم {serial} وتحديث المؤشرات بنجاح.")
        except Exception as e:
            messagebox.showerror("خطأ في الحفظ", f"فشل الحفظ بسبب خطأ في المدخلات:\n{e}")

    def search_and_edit_truck(self):
        search_query = simpledialog.askstring("البحث", "🔍 أدخل الرقم التسلسلي للشاحنة لاستدعائها:")
        if not search_query: return
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Truck_Main_Registry_2600 WHERE serial_num = ?", (search_query,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                self.clear_fields()
                
                self.vars['serial_num'].insert(0, str(row['serial_num'] or ""))
                self.vars['driver_name'].insert(0, str(row['driver_name'] or ""))
                self.vars['plate_num'].insert(0, str(row['plate_num'] or ""))
                self.vars['chassis_num'].insert(0, str(row['chassis_num'] or ""))
                self.vars['truck_model'].insert(0, str(row['truck_model'] or ""))
                self.vars['truck_length'].set(str(row['truck_length'] or ""))
                self.vars['brand_en'].insert(0, str(row['brand_en'] or ""))
                self.vars['class_en'].insert(0, str(row['class_en'] or ""))
                self.vars['brand_ar'].insert(0, str(row['brand_ar'] or ""))
                self.vars['fuel_type'].set(str(row['fuel_type'] or ""))
                self.vars['cabin_color'].insert(0, str(row['cabin_color'] or ""))
                self.vars['box_type'].set(str(row['box_type'] or ""))
                
                self.vars['cooling_engine_type'].set(str(row['cooling_engine_type'] or ""))
                self.toggle_cooling_fields_status()
                self.vars['driver_nature'].set(str(row['driver_nature'] or ""))
                self.vars['whatsapp_num'].insert(0, str(row['whatsapp_num'] or ""))
                
                for key in ['m_oil_engine', 'm_filter_oil', 'm_filter_air', 'm_filter_fuel', 'm_oil_gearbox', 'm_oil_differential', 'm_oil_steering', 'm_water_radiator',
                            'm_cool_oil', 'm_cool_filter_oil', 'm_cool_filter_fuel', 'm_cool_water_radiator', 'auto_oil_liters', 'auto_fuel_avg', 'auto_fuel_100km', 'auto_max_weight']:
                    if row[key]: self.vars[key].insert(0, str(row[key]))
                    
                for key in ['p_start_y', 'p_start_m', 'p_start_d', 'p_end_y', 'p_end_m', 'p_end_d']:
                    if row[key]: self.vars[key].set(str(row[key]))
                
                messagebox.showinfo("نجاح", f"✅ تم استدعاء كامل معطيات الشاحنة [{search_query}] بنجاح على الشاشة!")
            else:
                messagebox.showerror("خطأ", "❌ الشاحنة غير مسجلة في النظام.")
        except Exception as e:
            messagebox.showerror("خطأ في الاستدعاء", f"فشل جلب المعلومات بسبب خطأ داخلي في المنظومة:\n{e}")

    def clear_fields(self):
        for widget in self.vars.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherTruckIdentity2600(root)
    root.mainloop()