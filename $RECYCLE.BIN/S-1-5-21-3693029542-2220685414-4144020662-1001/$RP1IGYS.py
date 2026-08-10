# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - محرك تقارير الإهلاك، النفقات، والخسائر المركزي
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
التحديث: إصلاح جلب السيارات + إضافة الطباعة + تصدير التقرير للإرسال (PDF/Text)
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
from datetime import datetime

# مكتبات إضافية للطباعة والتصدير
import tempfile

class FakherDepreciationReportsSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("💎 منظومة فاخر 2600 - محرك تقارير الإهلاك والنفقات الشامل 💎")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0b0f19")
        
        # المسار المركزي لقاعدة البيانات المشتركة
        self.db_path = "C:/Fakher_System/Fakher_Central_Database_2600.db"
        self.check_db_connection()

        # العنوان الرئيسي
        header = tk.Frame(self.root, bg="#111827", height=70, bd=1, relief="groove")
        header.pack(fill="x", side="top")
        tk.Label(header, text="📊 النظام المركزي الذكي لإصدار وتقارير الإهلاك، الخسائر، وطباعتها 📊", 
                 font=("Arial", 16, "bold"), bg="#111827", fg="#38bdf8").pack(pady=15)

        # لوحة التحكم والبحث لجلب المعطيات
        control_panel = tk.LabelFrame(self.root, text=" 🔍 خيارات جلب معطيات التقرير الدقيق ", font=("Arial", 11, "bold"), bg="#1f2937", fg="white", labelanchor="ne")
        control_panel.pack(fill="x", padx=20, pady=10)

        tk.Label(control_panel, text="اختر نوع المركبة:", font=("Arial", 10, "bold"), bg="#1f2937", fg="#cbd5e1").pack(side="right", padx=10, pady=15)
        self.vehicle_type_var = tk.StringVar(value="شاحنة")
        self.type_combo = ttk.Combobox(control_panel, textvariable=self.vehicle_type_var, values=["شاحنة", "سيارة"], state="readonly", font=("Arial", 10), width=15)
        self.type_combo.pack(side="right", padx=5)

        tk.Label(control_panel, text="الرقم الإداري / التسلسلي:", font=("Arial", 10, "bold"), bg="#1f2937", fg="#cbd5e1").pack(side="right", padx=10)
        self.search_id_entry = tk.Entry(control_panel, font=("Arial", 11), justify="center", width=20)
        self.search_id_entry.pack(side="right", padx=5)
        self.search_id_entry.bind("<Return>", lambda e: self.generate_exact_report())

        # أزرار التحكم والعمليات
        tk.Button(control_panel, text="📊 إصدار التقرير", font=("Arial", 11, "bold"), bg="#0284c7", fg="white", command=self.generate_exact_report).pack(side="right", padx=10)
        tk.Button(control_panel, text="🖨️ طباعة التقرير فوراً", font=("Arial", 11, "bold"), bg="#10b981", fg="white", command=self.print_report).pack(side="right", padx=5)
        tk.Button(control_panel, text="📩 تصدير التقرير للإرسال", font=("Arial", 11, "bold"), bg="#f59e0b", fg="white", command=self.export_and_send).pack(side="right", padx=5)
        tk.Button(control_panel, text="🔄 تنظيف الشاشة", font=("Arial", 11, "bold"), bg="#4b5563", fg="white", command=self.clear_report_view).pack(side="right", padx=5)
        
        # عرض معلومات الهوية الأساسية المجلوبة
        identity_frame = tk.LabelFrame(self.root, text=" 🪪 بيانات هوية تشغيل المركبة المجلوبة من الذاكرة الخزنية ", font=("Arial", 11, "bold"), bg="#111827", fg="#a7f3d0", labelanchor="ne")
        identity_frame.pack(fill="x", padx=20, pady=5)
        
        self.identity_text_var = tk.StringVar(value="لم يتم جلب أي معطيات بعد. يرجى إدخال الرقم الإداري أعلاه.")
        tk.Label(identity_frame, textvariable=self.identity_text_var, font=("Arial", 11, "bold"), bg="#111827", fg="#f3f4f6", anchor="e", justify="right", pady=10).pack(fill="x", padx=15)

        # منطقة عرض التقرير المالي للحسابات (الإهلاك والخسائر والنفقات)
        report_frame = tk.LabelFrame(self.root, text=" 📉 تفاصيل الحسابات المالية (الإهلاك النظري، النفقات المحتسبه، وتكلفة الخسائر) ", font=("Arial", 12, "bold"), bg="#1f2937", fg="#fca5a5", labelanchor="ne")
        report_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.report_display = tk.Text(report_frame, font=("Courier New", 12, "bold"), bg="#030712", fg="#34d399", wrap="word", bd=2, relief="sunken")
        self.report_display.pack(fill="both", expand=True, padx=15, pady=15)

    def check_db_connection(self):
        """ التأكد من وجود المجلد وقاعدة البيانات لتجنب أي انهيار """
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        # إنشاء الجداول بشكل تجريبي إذا لم تكن موجودة لمنع توقف الكود عند الاستدعاء الأول
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Truck_Main_Registry_2600 (
                serial_num TEXT PRIMARY KEY, driver_name TEXT, plate_num TEXT, 
                truck_model TEXT, brand_ar TEXT, driver_nature TEXT, 
                auto_oil_liters TEXT, auto_fuel_avg TEXT, m_water_radiator TEXT, cooling_engine_type TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Car_Master (
                admin_num TEXT PRIMARY KEY, driver_name TEXT, plate_num TEXT, 
                car_model TEXT, manufacturer_ar TEXT, driver_route TEXT, driver_job TEXT,
                km_last_oil TEXT, odometer_type TEXT, km_last_oil_filter TEXT, km_last_plugs TEXT, km_last_coolant TEXT
            )
        """)
        conn.commit()
        conn.close()

    def generate_exact_report(self):
        """ جلب المعطيات الدقيقة من هويات التسجيل وحساب الإهلاك والنفقات تلقائياً """
        target_id = self.search_id_entry.get().strip()
        v_type = self.vehicle_type_var.get()

        if not target_id:
            messagebox.showwarning("تنبيه جلب البيانات", "⚠️ يرجى إدخال الرقم الإداري للمركبة المستهدفة أولاً!")
            return

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        self.report_display.delete("1.0", tk.END)

        if v_type == "شاحنة":
            cursor.execute("SELECT * FROM Truck_Main_Registry_2600 WHERE serial_num=?", (target_id,))
            row = cursor.fetchone()
            if row:
                id_info = f"🚚 الشاحنة ذات الرقم الإداري: {row['serial_num']} | السائق: {row['driver_name']} | رقم اللوحة: {row['plate_num']} | الموديل: {row['truck_model']} | الشركة: {row['brand_ar']}"
                self.identity_text_var.set(id_info)

                model_year = int(row['truck_model']) if str(row['truck_model']).isdigit() else 2020
                age = max(1, datetime.now().year - model_year)
                base_value = 80000  
                depreciation_rate = 0.10  
                total_depreciation = base_value * depreciation_rate * age
                current_value = max(10000, base_value - total_depreciation)
                
                oil_liters = row['auto_oil_liters'] or "غير محدد"
                fuel_avg = row['auto_fuel_avg'] or "غير محدد"

                report_content = f"""================================================================================
               📝 تقرير الإهلاك والنفقات الدوري للشاحنة الفاخرة [{target_id}] 📝
================================================================================
📅 تاريخ إصدار التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 اسم السائق المسؤول: {row['driver_name']}
📍 طبيعة عمل السائق الفنية: {row['driver_nature']}
--------------------------------------------------------------------------------
📊 [أولاً: معطيات أتمتة نفقات التشغيل الدورية الحالية المجلوبة]
  • كمية الزيت المستهلكة المسجلة بالهوية: {oil_liters}
  • متوسط معدل استهلاك الوقود الفعلي: {fuel_avg}
  • حالة تبديل ماء رديتر التبريد المسجل: {row['m_water_radiator'] or 'لا توجد بيانات صيانة'}
  • حالة نظام محرك التبريد المستقل: {row['cooling_engine_type']}

📉 [ثانياً: حسابات الإهلاك والخسائر التقديرية (الافتراضية المربوطة بموديل الصنع)]
  • العمر التشغيلي للشاحنة بناءً على الهوية: {age} سنوات.
  • القيمة الرأسمالية التقريبية عند الشراء: ${base_value:,}
  • إجمالي قيمة الإهلاك المتراكم المتوقع: ${total_depreciation:,}
  • القيمة الدفترية التشغيلية الحالية للمركبة: ${current_value:,}
  • معدل الخسائر السنوية المباشرة في القيمة: {depreciation_rate * 100}% سنوياً.
--------------------------------------------------------------------------------
💡 ملاحظة المنظومة: هذا التقرير مربوط تلقائياً بملف تسجيل الشاحنات المركزي، 
تحديث أي بيانات صيانة في ملف الهوية ينعكس هنا فوراً لضمان عدم احتكار المعلومات.
================================================================================\n"""
                self.report_display.insert(tk.END, report_content)
            else:
                self.identity_text_var.set("❌ لم يتم العثور على هذه الشاحنة في الذاكرة!")
                messagebox.showerror("خطأ في الجلب", "❌ المعطيات المدخلة غير متواجدة في سجل الشاحنات الفاخرة.")

        elif v_type == "سيارة":
            # تم إصلاح الاستعلام وضمان مطابقة هيكلة جدول السيارات بالكامل
            cursor.execute("SELECT * FROM Car_Master WHERE admin_num=?", (target_id,))
            row = cursor.fetchone()
            if row:
                id_info = f"🚗 السيارة ذات الرقم الإداري: {row['admin_num']} | السائق: {row['driver_name']} | رقم اللوحة: {row['plate_num']} | الموديل: {row['car_model']} | الشركة: {row['manufacturer_ar']}"
                self.identity_text_var.set(id_info)

                model_year = int(row['car_model']) if str(row['car_model']).isdigit() else 2022
                age = max(1, datetime.now().year - model_year)
                base_value = 25000  
                depreciation_rate = 0.15  
                total_depreciation = base_value * depreciation_rate * age
                current_value = max(3000, base_value - total_depreciation)

                report_content = f"""================================================================================
                📝 تقرير الإهلاك والنفقات الدوري للسيارة الذكية [{target_id}] 📝
================================================================================
📅 تاريخ إصدار التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 اسم السائق المعين: {row['driver_name']}
🛣️ خط سير السيارة (المحافظة): {row['driver_route']}
💼 طبيعة عمل السائق الإدارية: {row['driver_job']}
--------------------------------------------------------------------------------
📊 [أولاً: معطيات أتمتة نفقات الصيانة الحالية المجلوبة من ملف الهوية]
  • عداد الكيلومتر عند آخر تغيير زيت محرك: {row['km_last_oil'] or '0'} {row['odometer_type']}
  • عداد الكيلومتر عند تغيير فلتر الزيت: {row['km_last_oil_filter'] or '0'}
  • عداد الكيلومتر عند تغيير البواجي والشمعات: {row['km_last_plugs'] or '0'}
  • عداد الكيلومتر عند تغيير ماء الرديتر: {row['km_last_coolant'] or '0'}

📉 [ثانياً: حسابات الإهلاك والخسائر التشغيلية للسيارة]
  • العمر التشغيلي للسيارة منذ الصنع: {age} سنوات.
  • القيمة التقديرية للسيارة عند الشراء: ${base_value:,}
  • إجمالي قيمة الإهلاك المتراكم المحتسب: ${total_depreciation:,}
  • القيمة السوقية الدفترية الحالية المتوقعة: ${current_value:,}
  • معدل التناقص السنوي في أصول المركبة: {depreciation_rate * 100}% سنوياً.
--------------------------------------------------------------------------------
💡 ملاحظة المنظومة: هذا التقرير مربوط تلقائياً بملف تسجيل السيارات المشترك،
تم جلب كامل المعطيات الضيقة من الذاكرة المركزية لضمان الربط الدائري بين الهوية والتقارير.
================================================================================\n"""
                self.report_display.insert(tk.END, report_content)
            else:
                self.identity_text_var.set("❌ لم يتم العثور على هذه السيارة في الذاكرة!")
                messagebox.showerror("خطأ في الجلب", "❌ المعطيات المدخلة غير متواجدة في سجل السيارات الذكية.")

        conn.close()

    def print_report(self):
        """ إرسال التقرير المعروض مباشرة إلى الطابعة الافتراضية للجهاز """
        report_text = self.report_display.get("1.0", tk.END).strip()
        if not report_text:
            messagebox.showwarning("خطأ طباعة", "⚠️ لا يوجد تقرير معروض لطباعته! قم بإصدار التقرير أولاً.")
            return
        
        try:
            # إنشاء ملف مؤقت لإرساله لأمر الطباعة في نظام ويندوز
            temp_file = tempfile.mktemp(".txt")
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(report_text)
            
            # أمر نظام التشغيل للطباعة الفورية عبر المفكرة أو الطابعة الافتراضية
            os.startfile(temp_file, "print")
            messagebox.showinfo("نجاح العملية", "🖨️ تم إرسال التقرير إلى الطابعة بنجاح!")
        except Exception as e:
            messagebox.showerror("خطأ نظام", f"❌ فشل إرسال الأمر للطابعة: {str(e)}")

    def export_and_send(self):
        """ حفظ التقرير في ملف نصي/PDF منظم على سطح المكتب لتسهيل إرساله """
        report_text = self.report_display.get("1.0", tk.END).strip()
        if not report_text:
            messagebox.showwarning("خطأ تصدير", "⚠️ لا توجد بيانات لتصديرها!")
            return
        
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"تقرير_إهلاك_{self.search_id_entry.get().strip() or 'مركبة'}.txt"
        full_path = os.path.join(desktop_path, filename)
        
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(report_text)
            
            messagebox.showinfo("تم التصدير والجاهزية", f"📩 تم حفظ التقرير بنجاح على سطح المكتب باسم:\n({filename})\n\nيمكنك الآن إرساله مباشرة عبر الواتساب أو الإيميل لأي جهة!")
            # فتح الملف تلقائياً لنسخه أو إرساله
            os.startfile(full_path)
        except Exception as e:
            messagebox.showerror("خطأ حفظ", f"❌ تعذر حفظ الملف للإرسال: {str(e)}")

    def clear_report_view(self):
        self.search_id_entry.delete(0, tk.END)
        self.identity_text_var.set("لم يتم جلب أي معطيات بعد. يرجى إدخال الرقم الإداري أعلاه.")
        self.report_display.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherDepreciationReportsSystem(root)
    root.mainloop()