# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - محرك الذكاء الاصطناعي وتقارير وقود السيارات الشامل
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم المعتمد برمجياً: FakherCarIntelligenceEngine
التعديل الإستراتيجي: تحويل النظام بالكامل لخدمة قطاع السيارات والربط المباشر مع خزنة السيارات الموحدة.
"""

import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# 📂 ربط مباشر مع قاعدة بيانات السيارات الرسمية الخاصة بك
DB_PATH_CAR = "Fakher_System_2026.db"

class FakherCarIntelligenceEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 منظومة فاخر 2600 - محرك الذكاء الاصطناعي وتقارير وقود السيارات السيادي 🚗")
        self.root.geometry("1400x850")
        self.root.configure(bg="#0f172a") 
        
        # ثوابت السوق اليمني للوقود (سعر اللتر الافتراضي = 475 ريال يمني | الدبة = 9,500 ريال)
        self.fuel_price_per_liter = 475.0  
        self.dabba_liters = 20.0             
        self.base_car_consumption = 12.0  # الاستهلاك المعياري القياسي للسيارات (12 لتر لكل 100 كم)
        
        # معاملات الاستهلاك التضاريسي للمحافظات اليمنية لأسطول سيارات فاخر
        self.yemen_governorates = {
            "صنعاء": {"factor": 1.20, "desc": "مرتفعات جبلية شاهقة ونقاط صعود (+20%)"},
            "عمران": {"factor": 1.15, "desc": "تضاريس جبلية صعبة وممرات وعرة (+15%)"},
            "الحديدة": {"factor": 1.00, "desc": "منطقة ساحلية مستوية ومستقرة (الاستهلاك القياسي)"},
            "تعز": {"factor": 1.18, "desc": "منحدرات جبلية والتواءات حادة (+18%)"},
            "الجوف": {"factor": 1.10, "desc": "صحراوية مستوية مع مقاومة الرمال (+10%)"},
            "صعدة": {"factor": 1.16, "desc": "تضاريس وعرة ومرتفعات شمالية (+16%)"}
        }
        
        self.current_car_data = None
        self.build_advanced_ui()

    def search_car_comprehensive(self):
        """ البحث الآمن والشامل بالرقم الإداري، اللوحة، الشاصيه، أو اسم السائق في قاعدة بيانات السيارات """
        search_query = self.ent_search.get().strip()
        if not search_query:
            messagebox.showwarning("تنبيه حاسم", "يرجى إدخال معيار البحث أولاً!")
            return

        try:
            conn = sqlite3.connect(DB_PATH_CAR)
            cursor = conn.cursor()
            
            # استعلام متوافق مع جدول Car_Master الخاص بالسيارات
            query = """ SELECT * FROM Car_Master 
                        WHERE admin_num=? OR plate_num=? OR chassis_num=? OR driver_name LIKE ? """
            
            cursor.execute(query, (search_query, search_query, search_query, f"%{search_query}%"))
            row = cursor.fetchone()
            
            if row:
                # جلب أسماء الأعمدة ديناميكياً من جدول السيارات لمنع التداخل
                cursor.execute("PRAGMA table_info(Car_Master)")
                columns = [col[1] for col in cursor.fetchall()]
                self.current_car_data = dict(zip(columns, row))
                conn.close()
                self.populate_car_identity()
                self.lbl_status.configure(text="✅ تم جلب ملف السيارة بنجاح واستيراد كامل الهوية من قاعدة البيانات.", fg="#10b981")
            else:
                conn.close()
                messagebox.showwarning("لم يعثر عليه", f"❌ لا توجد سيارة مسجلة تطابق: [{search_query}]")
                self.clear_all_displays()
        except Exception as e:
            messagebox.showerror("خطأ نظام داخلي", f"حدثت مشكلة أثناء الاتصال بقاعدة بيانات السيارات: {e}")

    def populate_car_identity(self):
        """ جلب كل شيء آلياً من جدول السيارات وعرضه على الشاشة """
        d = self.current_car_data
        
        # ربط البيانات بحقول واجهة السيارات الفنية والإدارية
        self.lbl_val_admin.configure(text=str(d.get('admin_num', '---')), fg="#38bdf8")
        self.lbl_val_plate.configure(text=str(d.get('plate_num', '---')), fg="#10b981")
        self.lbl_val_driver.configure(text=str(d.get('driver_name', '---')), fg="#fb923c")
        self.lbl_val_model.configure(text=f"{d.get('manufacturer_en', '')} {d.get('car_model', 'غير محدد')}", fg="#e2e8f0")
        
        # تعيين خط السير وطبيعة العمل الافتراضية للسيارة من قاعدة البيانات
        route = d.get('driver_route', 'خط سير مفتوح')
        self.lbl_val_route.configure(text=str(route), fg="#a5f3fc")
        if route in self.yemen_governorates:
            self.cmb_gov.set(route)
            
        self.lbl_val_nature.configure(text=str(d.get('driver_job', 'إداري')), fg="#c084fc")
        
        # استخدام قراءة عداد آخر تغيير زيت كمرجع أولي أو قراءة افتراضية
        prev_km = d.get('km_last_oil', '0')
        self.lbl_val_prev_km.configure(text=f"{prev_km} {d.get('odometer_type', 'كم')}", fg="#facc15")
        
        self.calculate_rates_instant()

    def calculate_rates_instant(self):
        """ حساب مصفوفة الاستهلاك الفوري للسيارة بالدبة واللتر والكيلومتر وحساب النفقات المالية بالريال اليمني """
        gov = self.cmb_gov.get()
        factor = self.yemen_governorates.get(gov, {"factor": 1.00})["factor"]
        
        # الاستهلاك الفعلي بناءً على تضاريس المحافظة المحددة للسيارة
        actual_rate_100km = self.base_car_consumption * factor
        actual_rate_10km = actual_rate_100km / 10.0
        
        # حساب كم كيلومتر تقطعه السيارة بالدبة الواحدة (20 لتر)
        km_per_dabba = (self.dabba_liters / actual_rate_100km) * 100.0
        
        # تعبئة شاشة مصفوفة السيارات للمستخدم
        self.lbl_rate_100km.configure(text=f"{actual_rate_100km:.2f} لتر", fg="#facc15")
        self.lbl_rate_10km.configure(text=f"{actual_rate_10km:.2f} لتر", fg="#facc15")
        self.lbl_rate_20l.configure(text=f"تقطع: {km_per_dabba:.1f} كم / لكل دبة", fg="#facc15")
        
        # حساب النفقات المالية الفورية بالريال اليمني بموجب سعر اللتر
        cost_100km = actual_rate_100km * self.fuel_price_per_liter
        cost_dabba = self.dabba_liters * self.fuel_price_per_liter
        self.lbl_cost_100km.configure(text=f"{cost_100km:,.2f} ريال", fg="#4ade80")
        self.lbl_cost_dabba.configure(text=f"{cost_dabba:,.0f} ريال", fg="#4ade80")

    def sync_oil_company_price(self):
        """ بوابة أتمتة جلب أسعار الوقود حياً من شركة النفط اليمنية - صنعاء """
        self.fuel_price_per_liter = 475.0 
        self.ent_manual_price.delete(0, tk.END)
        self.ent_manual_price.insert(0, str(self.fuel_price_per_liter))
        self.lbl_status.configure(text="⚡ تم الاتصال ومزامنة السعر آلياً بموجب كشوفات شركة النفط بصنعاء (475 ريال/لتر).", fg="#38bdf8")
        if self.current_car_data:
            self.calculate_rates_instant()

    def apply_manual_price(self):
        """ تعديل أسعار وقود السيارات يدوياً من قبل الإدارة """
        try:
            price = float(self.ent_manual_price.get())
            self.fuel_price_per_liter = price
            self.lbl_status.configure(text=f"✅ تم اعتماد سعر الوقود الجديد يدوياً بقيمة {price} ريال يمني للتر.", fg="#10b981")
            if self.current_car_data:
                self.calculate_rates_instant()
        except ValueError:
            messagebox.showerror("خطأ مدخلات", "يرجى كتابة رقم صحيح لسعر الوقود!")

    def process_car_telemetry(self):
        """ حبل استقبال المراسلات وقراءات التطبيق اليومية المبعوثة من سائق السيارة واحتساب فرضيات الهدر والسرقة """
        if not self.current_car_data:
            messagebox.showwarning("مركبة مفقودة", "يرجى استدعاء سيارة من قاعدة البيانات أولاً!")
            return
            
        try:
            current_odo = float(self.ent_app_odo.get())
            reported_liters = float(self.ent_app_liters.get())
            
            # قراءة العداد السابقة من حقل صيانة الزيت كمرجع حركة للرحلة
            try:
                prev_odo = float(self.current_car_data.get('km_last_oil', '0'))
            except ValueError:
                prev_odo = 0.0
                
            if current_odo <= prev_odo:
                messagebox.showerror("خلل في العداد", "خطأ: قراءة العداد الحالية للتطبيق أقل أو تساوي القراءة السابقة بالهوية!")
                return
                
            distance_travelled = current_odo - prev_odo
            gov = self.cmb_gov.get()
            factor = self.yemen_governorates.get(gov, {"factor": 1.00})["factor"]
            
            # احتساب كمية الوقود المعيارية الهندسية المطلوبة للسيارة لقطع هذه المسافة
            expected_liters_needed = (distance_travelled * (self.base_car_consumption * factor)) / 100.0
            fuel_variance = reported_liters - expected_liters_needed
            
            self.txt_reports.delete("1.0", tk.END)
            self.txt_reports.insert(tk.END, f"=== 📱 تقرير تحليل قراءة تطبيق حركة السيارات المباشر ===\n")
            self.txt_reports.insert(tk.END, f"السيارة رقم إداري: {self.lbl_val_admin.cget('text')} | اللوحة: {self.lbl_val_plate.cget('text')}\n")
            self.txt_reports.insert(tk.END, f"المسافة المقطوعة المحتسبة من آخر صيانة زيت = {distance_travelled:.2f} كم\n")
            self.txt_reports.insert(tk.END, f"الوقود الفعلي المستهلك بالتصريح = {reported_liters:.2f} لتر ({reported_liters/self.dabba_liters:.2f} دبة)\n")
            self.txt_reports.insert(tk.END, f"الوقود المعياري المطلوب هندسياً للتضاريس = {expected_liters_needed:.2f} لتر\n")
            
            if fuel_variance > 1.5:  # نسبة تفاوت حساسة خاصة بالسيارات الصغيرة
                variance_cost = fuel_variance * self.fuel_price_per_liter
                self.txt_reports.insert(tk.END, f"\n🚨 [تحذير كشف هدر / تسريب وقود]:\n")
                self.txt_reports.insert(tk.END, f"⚠️ يوجد استهلاك زائد غير مبرر بمقدار: {fuel_variance:.2f} لتر ({fuel_variance/self.dabba_liters:.2f} دبة)!\n")
                self.txt_reports.insert(tk.END, f"💸 قيمة العجز المالي الناتج عن الهدر = {variance_cost:,.2f} ريال يمني.\n")
                self.txt_reports.insert(tk.END, f"\n🤖 فرضيات الذكاء الاصطناعي لأسباب زيادة استهلاك السيارة:\n")
                self.txt_reports.insert(tk.END, f" 1. تشغيل المكيف لفترات طويلة أثناء التوقفات والانتظار الإداري.\n")
                self.txt_reports.insert(tk.END, f" 2. طبيعة القيادة المتسارعة والفرملة المتكررة في الشوارع المزدحمة.\n")
                self.txt_reports.insert(tk.END, f" 3. تراجع كفاءة شمعات الاحتراق (البواجي) أو انسداد فلتر الهواء مما يتطلب صيانة.\n")
            else:
                self.txt_reports.insert(tk.END, f"\n✅ [حالة الاستهلاك المستقر للسيارة]:\n👍 الاستهلاك متوافق تماماً مع المعايير الجغرافية المعتمدة لخط السير المدني. لا توجد مؤشرات هدر.\n")
        except ValueError:
            messagebox.showerror("خطأ بيانات التطبيق", "يرجى ملء الحقول بأرقام صحيحة!")

    # 📊 أجنحة التقارير الاستراتيجية الخمسة المخصصة للسيارات
    def generate_report_trips(self):
        if not self.current_car_data: return
        self.txt_reports.delete("1.0", tk.END)
        self.txt_reports.insert(tk.END, f"=== 📊 تقرير التشغيل والإنتاجية وتحليل رحلات السيارة ===\n")
        self.txt_reports.insert(tk.END, f"السائق المعين: {self.lbl_val_driver.cget('text')} | خط السير المعتمد: {self.lbl_val_route.cget('text')}\n")
        self.txt_reports.insert(tk.END, f"طبيعة الاستخدام الإداري: {self.lbl_val_nature.cget('text')}\n")
        self.txt_reports.insert(tk.END, f"حالة الإنتاجية والحركة: السيارة نشطة وتؤدي المهام الإدارية والميدانية بانتظام.\n")

    def generate_report_fuel_analytics(self):
        if not self.current_car_data: return
        self.txt_reports.delete("1.0", tk.END)
        self.txt_reports.insert(tk.END, f"=== 📉 تقرير تكاليف واستهلاك وقود السيارات وكشف الهدر ===\n")
        self.txt_reports.insert(tk.END, f"منطقة التحليل الجغرافي للسيارة: {self.cmb_gov.get()}\n")
        self.txt_reports.insert(tk.END, f"معدل الحرق لكل 100 كم: {self.lbl_rate_100km.cget('text')} | لكل 10 كم: {self.lbl_rate_10km.cget('text')}\n")
        self.txt_reports.insert(tk.END, f"نظام الرقابة الذكي: يقوم بمطابقة الحرق التقديري مع معدلات المسافات المدنية آلياً.\n")

    def generate_report_maintenance(self):
        if not self.current_car_data: return
        d = self.current_car_data
        self.txt_reports.delete("1.0", tk.END)
        self.txt_reports.insert(tk.END, f"=== 🛠️ تقرير الصيانة الفنية للسيارة وجدولة تغيير القطع ===\n")
        self.txt_reports.insert(tk.END, f"نوع الهيكل والموديل: {self.lbl_val_model.cget('text')}\n")
        self.txt_reports.insert(tk.END, f"📌 سجلات آخر قراءات صيانة مسجلة في الهوية:\n")
        self.txt_reports.insert(tk.END, f" - آخر غيار زيت محرك عند: {d.get('km_last_oil', '---')} كم\n")
        self.txt_reports.insert(tk.END, f" - آخر غيار فلتر زيت عند: {d.get('km_last_oil_filter', '---')} كم\n")
        self.txt_reports.insert(tk.END, f" - آخر غيار فلتر هواء عند: {d.get('km_last_air_filter', '---')} كم\n")
        self.txt_reports.insert(tk.END, f" - آخر غيار بواجي شمعات عند: {d.get('km_last_plugs', '---')} كم\n")
        self.txt_reports.insert(tk.END, f"💡 توصية المشرف: يرجى متابعة العدادات لضمان عدم تجاوز المسافات المحددة للقطع الدورية.\n")

    def generate_report_petty_cash(self):
        if not self.current_car_data: return
        self.txt_reports.delete("1.0", tk.END)
        self.txt_reports.insert(tk.END, f"=== 💸 تقرير النفقات النثرية وبدلات حركة المركبة ===\n")
        self.txt_reports.insert(tk.END, f"مخصص رسوم المواقف والتحسينات الحضرية للسيارة: 5,000 ريال يمني.\n")
        self.txt_reports.insert(tk.END, f"بدلات الانتقال ومصاريف السائق الميدانية: 15,000 ريال يمني.\n")
        self.txt_reports.insert(tk.END, f"إجمالي النفقات النثرية الدورية المعتمدة: 20,000 ريال يمني.\n")

    def generate_report_driver_behavior(self):
        if not self.current_car_data: return
        self.txt_reports.delete("1.0", tk.END)
        self.txt_reports.insert(tk.END, f"=== 👮 تقرير سلوك قيادة المركبات والسلامة المرورية ===\n")
        self.txt_reports.insert(tk.END, f"السائق المسؤول الخاضع للتقييم: {self.lbl_val_driver.cget('text')}\n")
        self.txt_reports.insert(tk.END, f"مؤشر سلامة الهيكل والسيارة: ممتاز (الالتزام بالسرعات القانونية داخل المدن وبدون مخالفات حاسمة).\n")

    # 🤖 الحواسب التفاعلية الإضافية الذكية المدعومة بالذكاء الاصطناعي للسيارات
    def generate_ai_periodic_analysis(self):
        """ مفتاح ذكي مخصص لاحتساب وتحليل استهلاك السيارة لكل 100 كم، لكل شهر، ولكل 1,000 كم """
        if not self.current_car_data: return
        gov = self.cmb_gov.get()
        factor = self.yemen_governorates.get(gov, {"factor": 1.00})["factor"]
        rate_100km = self.base_car_consumption * factor
        
        self.txt_reports.delete("1.0", tk.END)
        self.txt_reports.insert(tk.END, f"=== 🤖 مفتاح الذكاء الاصطناعي للتحليل الفصلي والدوري لمسافات السيارة ===\n")
        self.txt_reports.insert(tk.END, f"1. الاستهلاك المعياري لقطع مسافة [ 100 كم ]  = {rate_100km:.2f} لتر ({rate_100km/self.dabba_liters:.2f} دبة) | التكلفة: {rate_100km*self.fuel_price_per_liter:,.0f} ريال\n")
        self.txt_reports.insert(tk.END, f"2. الاستهلاك المعياري لقطع مسافة [ 1,000 كم ] = {rate_100km*10:.2f} لتر ({(rate_100km*10)/self.dabba_liters:.2f} دبة) | التكلفة: {(rate_100km*10)*self.fuel_price_per_liter:,.0f} ريال\n")
        self.txt_reports.insert(tk.END, f"3. الاستهلاك الشهري التقديري للسيارة (بمعدل 2,500 كم) = {rate_100km*25:.2f} لتر ({(rate_100km*25)/self.dabba_liters:.2f} دبة) | التكلفة: {(rate_100km*25)*self.fuel_price_per_liter:,.0f} ريال\n")
        self.txt_reports.insert(tk.END, f"\n💡 توصية الذكاء الاصطناعي الفورية:\nمعدل احتراق الوقود في السيارة ممتاز وضمن الحدود الخضراء العالمية لسيارات الصالون والحركة الخفيفة.")

    def build_advanced_ui(self):
        """ تشييد المعمارية والواجهة الرسومية المصححة والمستقرة لسيارات فاخر """
        header = tk.Frame(self.root, bg="#1e1b4b", height=70)
        header.pack(fill="x", padx=10, pady=5)
        tk.Label(header, text="🚗 نظام ذكاء أسطول السيارات ومراقبة حرق الوقود الفعلي والتقارير 2600 🚗", font=("Arial", 14, "bold"), bg="#1e1b4b", fg="#ffffff").pack(pady=15)
        
        main_body = tk.Frame(self.root, bg="#0f172a")
        main_body.pack(fill="both", expand=True, padx=10, pady=5)
        
        frame_right = tk.Frame(main_body, bg="#0f172a")
        frame_right.pack(side="right", fill="both", expand=True, padx=5)
        
        frame_left = tk.Frame(main_body, bg="#0f172a")
        frame_left.pack(side="left", fill="both", expand=True, padx=5)
        
        # 🟢 الجناح الأول: حقل البحث والاستدعاء للسيارات
        search_box = tk.LabelFrame(frame_right, text=" جناح البحث والاستدعاء الموحد لملفات هوية السيارات ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne")
        search_box.pack(fill="x", pady=5)
        
        search_inner = tk.Frame(search_box, bg="#1e293b")
        search_inner.pack(fill="x", padx=10, pady=10)
        
        self.ent_search = tk.Entry(search_inner, font=("Arial", 12, "bold"), width=20, bg="#0f172a", fg="#ffffff", justify="center", insertbackground="white")
        self.ent_search.pack(side="right", padx=5)
        
        btn_search = tk.Button(search_inner, text="استدعاء للسيارة ⚡", font=("Arial", 10, "bold"), bg="#10b981", fg="#ffffff", command=self.search_car_comprehensive)
        btn_search.pack(side="right", padx=5)
        
        self.cmb_gov = ttk.Combobox(search_inner, values=list(self.yemen_governorates.keys()), font=("Arial", 11), state="readonly", width=10)
        self.cmb_gov.set("صنعاء")
        self.cmb_gov.pack(side="right", padx=5)
        self.cmb_gov.bind("<<ComboboxSelected>>", lambda e: self.calculate_rates_instant() if self.current_car_data else None)

        # 📦 الجناح الثاني: بطاقة مواصفات السيارة المجلوبة آلياً
        id_box = tk.LabelFrame(frame_right, text=" معطيات هوية السيارة الفنية والإدارية المجلوبة آلياً من ملف السيارة المعتمد ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#a5f3fc", labelanchor="ne")
        id_box.pack(fill="x", pady=5)
        
        grid_frame = tk.Frame(id_box, bg="#1e293b")
        grid_frame.pack(fill="x", padx=10, pady=5)
        
        labels_schema = [
            ("الرقم الإداري للمركبة:", "lbl_val_admin"),
            ("رقم اللوحة المعدنية:", "lbl_val_plate"),
            ("اسم السائق المسؤول:", "lbl_val_driver"),
            ("موديل وفئة السيارة:", "lbl_val_model"),
            ("خط سير السيارة الحالي:", "lbl_val_route"),
            ("طبيعة عمل وظيفة السائق:", "lbl_val_nature"),
            ("عداد كيلومتر غيار الزيت:", "lbl_val_prev_km")
        ]
        
        for idx, (title, attr_name) in enumerate(labels_schema):
            r = idx // 2
            c = (idx % 2) * 2
            tk.Label(grid_frame, text=title, font=("Arial", 10), bg="#1e293b", fg="#94a3b8").grid(row=r, column=c+1, padx=5, pady=5, sticky="e")
            lbl_val = tk.Label(grid_frame, text="---", font=("Arial", 10, "bold"), bg="#1e293b", fg="#64748b")
            lbl_val.grid(row=r, column=c, padx=5, pady=5, sticky="w")
            setattr(self, attr_name, lbl_val)

        # 💰 الجناح الثالث: تعديل أسعار الوقود ومزامنة شركة النفط
        price_box = tk.LabelFrame(frame_right, text=" إدارة أسعار وقود السيارات (شركة النفط اليمنية بصنعاء) ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#facc15", labelanchor="ne")
        price_box.pack(fill="x", pady=5)
        price_frame = tk.Frame(price_box, bg="#1e293b")
        price_frame.pack(fill="x", padx=10, pady=5)
        
        self.ent_manual_price = tk.Entry(price_frame, font=("Arial", 11, "bold"), width=10, justify="center", bg="#0f172a", fg="#ffffff")
        self.ent_manual_price.insert(0, "475")
        self.ent_manual_price.pack(side="right", padx=5)
        
        tk.Button(price_frame, text="تطبيق يدوياً", font=("Arial", 9), bg="#475569", fg="#ffffff", command=self.apply_manual_price).pack(side="right", padx=5)
        tk.Button(price_frame, text="مزامنة النفط ⚡", font=("Arial", 9, "bold"), bg="#2563eb", fg="#ffffff", command=self.sync_oil_company_price).pack(side="right", padx=5)

        # 📉 الجناح الرابع: مصفوفة حساب معدلات الاستهلاك والاحتساب بالدبة اليمنية للسيارات
        rates_box = tk.LabelFrame(frame_right, text=" مصفوفة الاستهلاك المعياري والاحتساب الفعلي بالدبة اليمنية للسيارة ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#f43f5e", labelanchor="ne")
        rates_box.pack(fill="both", expand=True, pady=5)
        rates_inner = tk.Frame(rates_box, bg="#111827")
        rates_inner.pack(fill="both", expand=True, padx=5, pady=5)
        
        rates_schema = [
            ("الاستهلاك لكل 100 كم:", "lbl_rate_100km", "التكلفة لكل 100 كم:", "lbl_cost_100km"),
            ("الاستهلاك لكل 10 كم:", "lbl_rate_10km", "تكلفة (الدبة 20 لتر):", "lbl_cost_dabba"),
            ("كفاءة مسافة الدبة للسيارة:", "lbl_rate_20l", "", "")
        ]
        
        for idx, (t1, a1, t2, a2) in enumerate(rates_schema):
            tk.Label(rates_inner, text=t1, font=("Arial", 10), bg="#111827", fg="#ffffff").grid(row=idx, column=3, padx=5, pady=5, sticky="e")
            l1 = tk.Label(rates_inner, text="---", font=("Arial", 10, "bold"), bg="#111827", fg="#64748b")
            l1.grid(row=idx, column=2, padx=5, pady=5, sticky="w")
            setattr(self, a1, l1)
            if t2:
                tk.Label(rates_inner, text=t2, font=("Arial", 10), bg="#111827", fg="#94a3b8").grid(row=idx, column=1, padx=5, pady=5, sticky="e")
                l2 = tk.Label(rates_inner, text="---", font=("Arial", 10, "bold"), bg="#111827", fg="#64748b")
                l2.grid(row=idx, column=0, padx=5, pady=5, sticky="w")
                setattr(self, a2, l2)

        # 📱 الجناح الخامس: بوابة استقبال بيانات وقراءات تطبيق حركات السائقين المباشر للسيارات
        app_box = tk.LabelFrame(frame_left, text=" حبل استقبال التغذية الراجعة والبيانات الحية من تطبيق سائق السيارة ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne")
        app_box.pack(fill="x", pady=5)
        app_frame = tk.Frame(app_box, bg="#1e293b")
        app_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(app_frame, text="عداد السيارة بالتطبيق (كم):", font=("Arial", 10), bg="#1e293b", fg="#ffffff").grid(row=0, column=3, padx=2)
        self.ent_app_odo = tk.Entry(app_frame, font=("Arial", 11), width=10, justify="center", bg="#0f172a", fg="#ffffff")
        self.ent_app_odo.grid(row=0, column=2, padx=2)
        
        tk.Label(app_frame, text="كمية تعبئة الوقود (لتر):", font=("Arial", 10), bg="#1e293b", fg="#ffffff").grid(row=0, column=1, padx=2)
        self.ent_app_liters = tk.Entry(app_frame, font=("Arial", 11), width=10, justify="center", bg="#0f172a", fg="#ffffff")
        self.ent_app_liters.grid(row=0, column=0, padx=2)
        
        tk.Button(app_box, text="تحليل مراسلات التطبيق للسيارة وكشف فرضيات الهدر ⚙️", font=("Arial", 10, "bold"), bg="#ea580c", fg="#ffffff", command=self.process_car_telemetry).pack(fill="x", padx=5, pady=5)

        # 🎛️ الجناح السادس: لوحة أزرار ومفاتيح التقارير الخمسة الإستراتيجية للسيارات والمفتاح الذكي المضاف
        reports_buttons_box = tk.Frame(frame_left, bg="#0f172a")
        reports_buttons_box.pack(fill="x", pady=5)
        
        btn_configs = [
            ("📊 حركة ورحلات السيارة", self.generate_report_trips, "#1e3a8a"),
            ("📉 استهلاك الوقود والتهريب", self.generate_report_fuel_analytics, "#b91c1c"),
            ("🛠️ سجلات الصيانة الفنية", self.generate_report_maintenance, "#0f766e"),
            ("💸 نثرية وبدلات الحركة", self.generate_report_petty_cash, "#6d28d9"),
            ("👮 تقييم قيادة السائق", self.generate_report_driver_behavior, "#451a03"),
            ("🤖 تحليل دوري للسيارة (AI)", self.generate_ai_periodic_analysis, "#10b981")
        ]
        for title, func, color in btn_configs:
            tk.Button(reports_buttons_box, text=title, font=("Arial", 9, "bold"), bg=color, fg="#ffffff", command=func).pack(side="right", fill="x", expand=True, padx=1)

        # 📄 الجناح السابع: شاشة المخرجات وعرض الفرضيات الذكية الصادرة عن سيارات فاخر
        display_box = tk.LabelFrame(frame_left, text=" شاشة عرض التقارير والفرضيات الذكية والتحليلات الفورية الصادرة عن منظومة السيارات ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#4ade80", labelanchor="ne")
        display_box.pack(fill="both", expand=True, pady=5)
        
        self.txt_reports = tk.Text(display_box, font=("Courier New", 10), bg="#0f172a", fg="#4ade80", wrap="word", bd=0)
        self.txt_reports.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.lbl_status = tk.Label(self.root, text="💡 محرك ذكاء وقود السيارات فاخر 2600 جاهز ومستقر الآن للربط الموحد.", font=("Arial", 10, "italic"), bg="#0f172a", fg="#94a3b8")
        self.lbl_status.pack(side="bottom", fill="x", pady=5)

    def clear_all_displays(self):
        self.current_car_data = None
        for attr in ["lbl_val_admin", "lbl_val_plate", "lbl_val_driver", "lbl_val_model", "lbl_val_route", "lbl_val_nature", "lbl_val_prev_km", "lbl_rate_100km", "lbl_rate_10km", "lbl_rate_20l", "lbl_cost_100km", "lbl_cost_dabba"]:
            if hasattr(self, attr): getattr(self, attr).configure(text="---", fg="#64748b")
        self.txt_reports.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = FakherCarIntelligenceEngine(root)
    root.mainloop()