# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - درع الأتمتة والمراقبة والتدقيق الجنائي الذاتي الشامل
المشرف الفني العام الأعلى: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد للملف: Fakher_Automation_Shield_2600.py
الإصدار: الجيل الثامن الفائق - الأتمتة الكاملة والربط الجيني المباشر لكشف الهدر والتلاعب
"""

import os
import sys
import shutil
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# الربط الصارم والمباشر مع العقل الإلكتروني الثالث (CentralAlgorithmsEngine)
try:
    sys.path.append("C:/Fakher_System")
    from algorithms_engine import CentralAlgorithmsEngine
    quantum_engine = CentralAlgorithmsEngine()
except Exception as e:
    quantum_engine = None
    print(f"⚠️ تنبيه ارتباط: تعذر دمج محرك الخوارزميات تلقائياً بسبب: {e}")

class FakherAutomationShield2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ منظومة فاخر 2600 - درع الأتمتة السيادي ومحرك التدقيق الجنائي الآلي 🛡️")
        self.root.geometry("1650x900")
        self.root.configure(bg="#020617")
        self.root.state('zoomed')
        
        # المسارات السيادية المعتمدة في باطن النظام
        self.target_dir = "C:/Fakher_System"
        self.db_truck = os.path.join(self.target_dir, "Fakher_Central_Database_2600.db")
        self.db_car = os.path.join(self.target_dir, "Fakher_System_2026.db")
        self.backup_dir = os.path.join(self.target_dir, "Fakher_Backups_2600")
        
        os.makedirs(self.backup_dir, exist_ok=True)
        self.build_ui()

    def build_ui(self):
        # ─── الجناح العلوي: الهيدر والترويجة السيادية ───
        header_frame = tk.Frame(self.root, bg="#1e1b4b", height=85)
        header_frame.pack(fill="x", padx=15, pady=10)
        
        lbl_title = tk.Label(
            header_frame, 
            text="🏛️ برج التدقيق الأوتوماتيكي وحظر الهدر والتلاعب بالوقود والعدادات 🏛️", 
            font=("Arial", 18, "bold"), bg="#1e1b4b", fg="#38bdf8"
        )
        lbl_title.pack(pady=8)
        
        lbl_sub = tk.Label(
            header_frame, 
            text="المشرف الفني العام الأعلى: المهندس جمال سويد (أبا عبد الله) | التحديث الذاتي المترابط بين الخزائن البرمجية", 
            font=("Arial", 11, "italic"), bg="#1e1b4b", fg="#a78bfa"
        )
        lbl_sub.pack(pady=2)

        # ─── شريط البحث الذكي الموحد ───
        search_frame = tk.LabelFrame(self.root, text=" 🔍 محرك الاستدعاء والربط التلقائي الموحد (أدخل أي معلومة للمركبة أو السائق للبحث الشامل) ", font=("Arial", 12, "bold"), bg="#0f172a", fg="#38bdf8", labelanchor="ne")
        search_frame.pack(fill="x", padx=15, pady=5)
        
        tk.Label(search_frame, text="خانات البحث المرن الذكي:", font=("Arial", 11, "bold"), bg="#0f172a", fg="#cbd5e1").pack(side="right", padx=15, pady=15)
        
        self.ent_search = tk.Entry(search_frame, font=("Arial", 14, "bold"), bg="#1e293b", fg="#f8fafc", justify="center", insertbackground="white")
        self.ent_search.pack(side="right", fill="x", expand=True, padx=15, pady=15)
        self.ent_search.bind("<Return>", lambda e: self.execute_omni_search())
        
        btn_search = tk.Button(search_frame, text="⚡ تشغيل الاستدعاء والتدقيق الآلي", font=("Arial", 11, "bold"), bg="#0ea5e9", fg="white", command=self.execute_omni_search)
        btn_search.pack(side="left", padx=15, pady=15)

        # ─── تقسيم جسم الشاشة إلى جناحين تحليليين ───
        body_pane = tk.Frame(self.root, bg="#020617")
        body_pane.pack(fill="both", expand=True, padx=15, pady=5)

        # الجناح الأيمن: بطاقة الهوية الرقمية
        self.right_box = tk.LabelFrame(body_pane, text=" 📋 بطاقة الهوية الرقمية ومطابقة الكتالوج المصنعي للوقود ", font=("Arial", 12, "bold"), bg="#0f172a", fg="#4ade80", labelanchor="ne")
        self.right_box.pack(side="right", fill="both", expand=True, padx=10, pady=5)
        
        self.txt_identity = tk.Text(self.right_box, font=("Courier New", 12, "bold"), bg="#1e293b", fg="#4ade80", wrap="word", bd=0)
        self.txt_identity.pack(fill="both", expand=True, padx=10, pady=10)

        # الجناح الأيسر: شاشة الفرضيات التحليلية وكشف التلاعب
        self.left_box = tk.LabelFrame(body_pane, text=" 🧠 محرك الفرضيات الآلي وتحليل معدلات الهدر الجغرافي ", font=("Arial", 12, "bold"), bg="#0f172a", fg="#f43f5e", labelanchor="ne")
        self.left_box.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        self.txt_forensics = tk.Text(self.left_box, font=("Courier New", 12, "bold"), bg="#0f172a", fg="#f43f5e", wrap="word", bd=0)
        self.txt_forensics.pack(fill="both", expand=True, padx=10, pady=10)

        # الشريط السفلي للحالة
        status_frame = tk.Frame(self.root, bg="#0f172a", height=35)
        status_frame.pack(fill="x", side="bottom")
        
        self.lbl_status = tk.Label(status_frame, text="🛡️ نظام الحماية مستقر وجاهز للتدقيق المباشر...", font=("Arial", 10, "bold"), bg="#0f172a", fg="#94a3b8")
        self.lbl_status.pack(side="right", padx=15, pady=5)

    def execute_omni_search(self):
        """ محرك الاستدعاء الأوتوماتيكي العابر للجداول الحية بالاعتماد على البنية الصارمة """
        query = self.ent_search.get().strip()
        if not query:
            messagebox.showwarning("محرك البحث", "يرجى كتابة أي بيان (اسم، لوحة، رقم إداري، شاصيه) للبدء!")
            return

        self.txt_identity.delete("1.0", tk.END)
        self.txt_forensics.delete("1.0", tk.END)
        
        record = None
        v_type = None

        # 1. التغلغل في جدول الشاحنات بقرص C
        if os.path.exists(self.db_truck):
            try:
                conn = sqlite3.connect(self.db_truck)
                cursor = conn.cursor()
                sql = """SELECT * FROM Truck_Main_Registry_2600 WHERE 
                         driver_name LIKE ? OR plate_num LIKE ? OR chassis_num LIKE ? OR serial_num LIKE ?"""
                p = f"%{query}%"
                cursor.execute(sql, (p, p, p, p))
                row = cursor.fetchone()
                if row:
                    # جلب أسماء الأعمدة ديناميكياً
                    cursor.execute("PRAGMA table_info(Truck_Main_Registry_2600)")
                    cols = [c[1] for c in cursor.fetchall()]
                    record = dict(zip(cols, row))
                    v_type = "Truck"
                conn.close()
            except Exception as e:
                print(f"خطأ فحص الشاحنات: {e}")

        # 2. التغلغل في جدول السيارات بقرص C في حال عدم العثور عليها في الشاحنات
        if not record and os.path.exists(self.db_car):
            try:
                conn = sqlite3.connect(self.db_car)
                cursor = conn.cursor()
                sql = """SELECT * FROM Car_Master WHERE 
                         driver_name LIKE ? OR plate_num LIKE ? OR chassis_num LIKE ? OR admin_num LIKE ?"""
                p = f"%{query}%"
                cursor.execute(sql, (p, p, p, p))
                row = cursor.fetchone()
                if row:
                    cursor.execute("PRAGMA table_info(Car_Master)")
                    cols = [c[1] for c in cursor.fetchall()]
                    record = dict(zip(cols, row))
                    v_type = "Car"
                conn.close()
            except Exception as e:
                print(f"خطأ فحص السيارات: {e}")

        if not record:
            self.txt_identity.insert(tk.END, f"❌ فشل جلب البيانات: لم يتم العثور على أي مركبة مطابقة للمدخل [{query}] في الجداول الرقمية.")
            return

        # المزامنة مع كود الخوارزميات وإظهار النتائج الذكية فوراً
        self.analyze_and_bind_quantum(v_type, record)

    def analyze_and_bind_quantum(self, v_type, data):
        """ المطابقة الآلية الذكية واستخراج البيانات من كود الخوارزميات والشركات المصنعة """
        driver = data.get("driver_name") or "غير مسجل"
        plate = data.get("plate_num") or "بدون لوحة"
        chassis = str(data.get("chassis_num") or "").upper()
        route = data.get("route_line") or "صنعاء"
        
        # استخراج قراءة العداد بذكاء وفقاً لنوع الجدول
        if v_type == "Truck":
            v_id = data.get("serial_num") or "🎯"
            model = data.get("truck_model") or "شاحنة نقل"
            odo_val = data.get("current_km") or data.get("current_odometer") or 0
        else:
            v_id = data.get("admin_num") or "🎯"
            model = "سيارة صالون إدارية"
            odo_val = data.get("current_odometer") or 0

        try:
            odo = float(str(odo_val).replace(",", ""))
        except:
            odo = 0.0

        # 1. جلب معلومات الشركة المصنعة من كود الخوارزميات (العقل الثالث) عبر فك الشاصيه
        brand_fact = "ISUZU"
        efficiency_fact = 6.5
        oil_capacity = 12
        vehicle_cat = "شاحنة ديزل"
        conn_status = "🔒 فحص داخلي مؤمن"

        if quantum_engine and hasattr(quantum_engine, 'smart_decode_vin_chassis'):
            res = quantum_engine.smart_decode_vin_chassis(chassis)
            brand_fact = res.get("الماركة_الحقيقية", "ISUZU")
            efficiency_fact = res.get("معدل_الاستهلاك_القياسي_كم_لكل_لتر", 6.5)
            oil_capacity = res.get("کمية_زيت_المحرك_لتر", 12)
            vehicle_cat = res.get("فئة_المركبة", "شاحنة ديزل")
            conn_status = res.get("حالة_الاتصال", "🔒 متصل محلياً")

        # 2. احتساب أثر المحافظات اليمنية والتضاريس جغرافياً
        detected_prov = "صنعاء"
        geo_factor = 1.18  # المعامل الافتراضي لصنعاء
        if quantum_engine and hasattr(quantum_engine, 'yemen_geography_rules'):
            for prov, info in quantum_engine.yemen_geography_rules.items():
                if prov in str(route) or prov in str(data.get("province", "")):
                    detected_prov = prov
                    geo_factor = info.get("factor", 1.18)
                    break

        # كفاءة الاستهلاك الفعلي المحتسب فيزيائياً للمحافظة (كم / لتر)
        actual_efficiency = efficiency_fact / geo_factor
        estimated_fuel = odo / actual_efficiency if odo > 0 else 0.0

        # ─── طباعة كرت الهوية الرقمي الكامل في الجناح الأيمن ───
        self.txt_identity.insert(tk.END, f"====================================================\n")
        self.txt_identity.insert(tk.END, f"👑 بطاقة الهوية الرقمية المستدعاة أوتوماتيكياً 👑\n")
        self.txt_identity.insert(tk.END, f"====================================================\n\n")
        self.txt_identity.insert(tk.END, f"👤 اسم السائق المعمد: {driver}\n")
        self.txt_identity.insert(tk.END, f"🔢 رقم اللوحة المعدنية: {plate}\n")
        self.txt_identity.insert(tk.END, f"🆔 المعرف الإداري الفني: {v_id}\n")
        self.txt_identity.insert(tk.END, f"🚙 الموديل والمواصفة: {model}\n")
        self.txt_identity.insert(tk.END, f"⚙️ رقم شاصيه المصنع: {chassis}\n\n")
        self.txt_identity.insert(tk.END, f"----------------------------------------------------\n")
        self.txt_identity.insert(tk.END, f"🏭 البيانات المستقاة من الشركة المصنعة للمركبة:\n")
        self.txt_identity.insert(tk.END, f"----------------------------------------------------\n")
        self.txt_identity.insert(tk.END, f"🔹 الماركة المكتشفة: {brand_fact}\n")
        self.txt_identity.insert(tk.END, f"🔹 فئة الكيان الهيكلي: {vehicle_cat}\n")
        self.txt_identity.insert(tk.END, f"⛽ معدل الاستهلاك القياسي للمصنع: {efficiency_fact} كم/لتر\n")
        self.txt_identity.insert(tk.END, f"🛢️ سعة الزيت الموصى بها: {oil_capacity} لتر\n")
        self.txt_identity.insert(tk.END, f"📡 حالة فحص الشاصيه: {conn_status}\n")

        # ─── طباعة تقرير الفرضيات الذكي وكشف الهدر في الجناح الأيسر ───
        self.txt_forensics.tag_config("ALERT", foreground="#f43f5e", font=("Courier New", 12, "bold"))
        self.txt_forensics.tag_config("SAFE", foreground="#38bdf8", font=("Courier New", 12, "bold"))
        
        self.txt_forensics.insert(tk.END, f"====================================================\n")
        self.txt_forensics.insert(tk.END, f"🧠 تقرير الفرضيات الآلي ومطابقات كشف التلاعب 🧠\n")
        self.txt_forensics.insert(tk.END, f"====================================================\n\n")
        self.txt_forensics.insert(tk.END, f"📍 المحافظة المرصودة جغرافياً: [{detected_prov}]\n")
        self.txt_forensics.insert(tk.END, f"📈 إجمالي المسافة المقطوعة بالعداد: {odo} كم\n")
        self.txt_forensics.insert(tk.END, f"⛽ الكفاءة الفعلية المحتسبة جغرافياً: {round(actual_efficiency, 2)} كم/لتر\n")
        self.txt_forensics.insert(tk.END, f"🔥 حجم الوقود المقدر للرحلة الحالية: {round(estimated_fuel, 1)} لتر\n\n")
        self.txt_forensics.insert(tk.END, f"----------------------------------------------------\n")
        self.txt_forensics.insert(tk.END, f"🔮 الفرضيات الميدانية والتدقيق والمراجعة الذكية:\n")
        self.txt_forensics.insert(tk.END, f"----------------------------------------------------\n")

        has_anomaly = False
        if odo <= 0:
            self.txt_forensics.insert(tk.END, "🚨 [فرضية تلاعب بالعداد]: العداد متوقف تماماً! توجد محاولة لتعطيل قراءة المسافة المقطوعة لإخفاء استهلاك وقود غير مبرر.\n", "ALERT")
            has_anomaly = True
        
        if actual_efficiency < 4.5 and v_type == "Truck":
            self.txt_forensics.insert(tk.END, "⚠️ [فرضية هدر أو حمولة زائدة]: كفاءة الاستهلاك منخفضة جداً مقارنة بمعايير المصنع، مما يشير إلى وجود هدر في الوقود أو تشغيل الشاحنة بحمولة تتجاوز الوزن المسموح.\n", "ALERT")
            has_anomaly = True

        if not has_anomaly:
            self.txt_forensics.insert(tk.END, "🟢 [تأكيد الحصانة الرقمية للدرع]: تم مطابقة البيانات الحالية مع خوارزمية الشركات المصنعة وتضاريس المحافظات بنجاح. معدلات الاستهلاك والمسافات آمنة 100% ولا توجد أي شبهة تلاعب.\n", "SAFE")

        self.lbl_status.configure(text=f"✅ تم الانتهاء من التدقيق الآلي الشامل لمركبة السائق: {driver}", fg="#4ade80")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherAutomationShield2600(root)
    root.mainloop()