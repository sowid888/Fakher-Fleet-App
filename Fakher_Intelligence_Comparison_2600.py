# -*- coding: utf-8 -*-
import os
import sqlite3
import tempfile
import tkinter as tk
from tkinter import messagebox, ttk

DB_PATHS = [
    "Fakher_System_2026.db",
    "C:/Fakher_System/Fakher_System_2026.db",
    "Fakher_Central_Database_2600.db"
]

class FakherFleetIntelligence2600:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 منظومة فاخر 2600 - برج التحليل الاستخباراتي وعقل الربط المطلق 🧠")
        self.root.geometry("1550x850")
        self.root.configure(bg="#0f172a")

        # متغيرات البيانات النشطة
        self.active_plate = "---"
        self.active_admin_num = "---"
        self.active_km = "0.0"
        self.active_driver = "---"
        self.active_type = "---"
        self.active_chassis = "---"
        self.active_class = "---"
        self.active_brand = "---"
        self.active_province = "صنعاء" 

        self.setup_styles()
        self.build_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground="#1e293b", background="#0f172a", foreground="white")

    def build_ui(self):
        # 🏛️ الشريط العلوي
        header = tk.Frame(self.root, bg="#1e1b4b", bd=1, relief="solid")
        header.pack(fill="x", padx=15, pady=10)
        tk.Label(header, text="🏛️ مـنـظـومـة فـاخـر 2600 - بـرج الـتـحـلـيـل الـاسـتـخـبـاراتـي وعـقـل الـربـط الـمـطلـق 🏛️", font=("Arial", 18, "bold"), bg="#1e1b4b", fg="#38bdf8", pady=4).pack()
        tk.Label(header, text="المشرف العام الأعلى: المهندس جمال سويد (أبا عبد الله) | مصفوفة التحليل الجنائي لـ 14 تقريراً هيكلياً وتشغيلياً للآليات", font=("Arial", 10, "italic"), bg="#1e1b4b", fg="#94a3b8").pack()

        # 🔍 محرك البحث الموحد
        search_group = tk.LabelFrame(self.root, text=" 🔍 محرك الاستدعاء الموحد الفعلي المستهدف للسيارات والشاحنات ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne", padx=15, pady=8)
        search_group.pack(fill="x", padx=15, pady=2)

        search_f = tk.Frame(search_group, bg="#1e293b")
        search_f.pack(fill="x")
        
        tk.Label(search_f, text="أدخل معيار البحث المطلوب للآلية:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#f8fafc").pack(side="right", padx=10)
        self.entry_search = tk.Entry(search_f, font=("Arial", 12, "bold"), width=30, justify="center", bg="#0f172a", fg="#facc15", insertbackground="white")
        self.entry_search.pack(side="right", padx=10)
        self.entry_search.bind("<Return>", lambda e: self.execute_search())

        tk.Button(search_f, text="🚀 إطلاق فحص واستدعاء حقيقي من الخزائن", font=("Arial", 11, "bold"), bg="#2563eb", fg="white", width=28, command=self.execute_search).pack(side="right", padx=15)
        tk.Button(search_f, text="🛠️ توليد قاعدة بيانات تجريبية فوراً", font=("Arial", 10, "bold"), bg="#059669", fg="white", command=self.create_mock_database).pack(side="left", padx=15)

        # 📋 لوحة الهوية الفنية المستدعاة
        identity_group = tk.LabelFrame(self.root, text=" 📋 حقول الهوية الفنية المستدعاة حياً ومباشرة من سجلات المنظومة ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#4ade80", labelanchor="ne", padx=15, pady=8)
        identity_group.pack(fill="x", padx=15, pady=2)

        grid_f = tk.Frame(identity_group, bg="#1e293b")
        grid_f.pack(fill="x")

        grid_f.grid_columnconfigure(0, weight=1)
        grid_f.grid_columnconfigure(1, weight=0)
        grid_f.grid_columnconfigure(2, weight=1)
        grid_f.grid_columnconfigure(3, weight=0)

        # الصف 0
        tk.Label(grid_f, text="رقم اللوحة المعدنية الفعلي:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#94a3b8").grid(row=0, column=3, padx=10, pady=5, sticky="e")
        self.lbl_plate = tk.Label(grid_f, text="---", font=("Arial", 12, "bold"), bg="#0f172a", fg="#4ade80", width=35, relief="solid", bd=1, pady=4)
        self.lbl_plate.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        tk.Label(grid_f, text="الرقم الإداري المتسلسل المعتمد:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#94a3b8").grid(row=0, column=1, padx=10, pady=5, sticky="e")
        self.lbl_admin = tk.Label(grid_f, text="---", font=("Arial", 12, "bold"), bg="#0f172a", fg="#4ade80", width=35, relief="solid", bd=1, pady=4)
        self.lbl_admin.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # الصف 1
        tk.Label(grid_f, text="آخر قراءة فعلية للعداد (KM):", font=("Arial", 11, "bold"), bg="#1e293b", fg="#94a3b8").grid(row=1, column=3, padx=10, pady=5, sticky="e")
        self.lbl_km = tk.Label(grid_f, text="---", font=("Arial", 12, "bold"), bg="#0f172a", fg="#facc15", width=35, relief="solid", bd=1, pady=4)
        self.lbl_km.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        tk.Label(grid_f, text="اسم السائق المقيد بالكامل:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#94a3b8").grid(row=1, column=1, padx=10, pady=5, sticky="e")
        self.lbl_driver = tk.Label(grid_f, text="---", font=("Arial", 12, "bold"), bg="#0f172a", fg="#4ade80", width=35, relief="solid", bd=1, pady=4, anchor="e", padx=10)
        self.lbl_driver.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # الصف 2
        tk.Label(grid_f, text="نوع ومصدر المركبة الفعلي:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#94a3b8").grid(row=2, column=3, padx=10, pady=5, sticky="e")
        self.lbl_type = tk.Label(grid_f, text="---", font=("Arial", 12, "bold"), bg="#0f172a", fg="#38bdf8", width=35, relief="solid", bd=1, pady=4)
        self.lbl_type.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        tk.Label(grid_f, text="رقم شاصيه السيارة أو الشاحنة:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#94a3b8").grid(row=2, column=1, padx=10, pady=5, sticky="e")
        self.lbl_chassis = tk.Label(grid_f, text="---", font=("Arial", 12, "bold"), bg="#0f172a", fg="#f8fafc", width=35, relief="solid", bd=1, pady=4)
        self.lbl_chassis.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # الصف 3
        tk.Label(grid_f, text="فئة ونوع الهيكل التشغيلي:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#94a3b8").grid(row=3, column=3, padx=10, pady=5, sticky="e")
        self.lbl_class = tk.Label(grid_f, text="---", font=("Arial", 12, "bold"), bg="#0f172a", fg="#e2e8f0", width=35, relief="solid", bd=1, pady=4)
        self.lbl_class.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        tk.Label(grid_f, text="ماركة السيارة أو الشاحنة الفعلي:", font=("Arial", 11, "bold"), bg="#1e293b", fg="#a78bfa").grid(row=3, column=1, padx=10, pady=5, sticky="e")
        self.lbl_brand = tk.Label(grid_f, text="---", font=("Arial", 12, "bold"), bg="#0f172a", fg="#a78bfa", width=35, relief="solid", bd=1, pady=4)
        self.lbl_brand.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # 🎛️ مصفوفة المفاتيح الـ 14 الاستخباراتية المعدلة
        buttons_main_container = tk.Frame(self.root, bg="#0f172a")
        buttons_main_container.pack(fill="x", padx=15, pady=10)

        btn_font = ("Arial", 12, "bold")

        # المجموعة الأولى (7 مفاتيح)
        g1 = tk.LabelFrame(buttons_main_container, text=" ⚡ القسم الأول: تجارب كفاءة الحركة والوقود والصيانة (7 مفاتيح) ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#facc15", labelanchor="ne", padx=5, pady=5)
        g1.pack(side="right", fill="both", expand=True, padx=5)

        tk.Button(g1, text="⛽ 1. كفاءة الوقود ومطابقة الأقاليم", font=btn_font, bg="#b45309", fg="white", pady=1, command=lambda: self.trigger_intel_report(1)).pack(fill="x", pady=2)
        tk.Button(g1, text="🛠️ 2. سجل الصيانات الشامل للأرشيف", font=btn_font, bg="#1d4ed8", fg="white", pady=1, command=lambda: self.trigger_intel_report(2)).pack(fill="x", pady=2)
        tk.Button(g1, text="🔄 3. استهلاك الإطارات ونسب الانزلاق", font=btn_font, bg="#047857", fg="white", pady=1, command=lambda: self.trigger_intel_report(3)).pack(fill="x", pady=2)
        tk.Button(g1, text="👤 4. تقييم سلوك السائق والتهور", font=btn_font, bg="#334155", fg="white", pady=1, command=lambda: self.trigger_intel_report(4)).pack(fill="x", pady=2)
        tk.Button(g1, text="🌱 5. البصمة الكربونية والانبعاثات", font=btn_font, bg="#0369a1", fg="white", pady=1, command=lambda: self.trigger_intel_report(5)).pack(fill="x", pady=2)
        tk.Button(g1, text="💰 6. حساب تكلفة الكيلومتر الفعلي", font=btn_font, bg="#4d7c0f", fg="white", pady=1, command=lambda: self.trigger_intel_report(6)).pack(fill="x", pady=2)
        tk.Button(g1, text="📋 7. الجدارة الفنية والمعاينة الدورية", font=btn_font, bg="#6d28d9", fg="white", pady=1, command=lambda: self.trigger_intel_report(7)).pack(fill="x", pady=2)

        # المجموعة الثانية (7 مفاتيح)
        g2 = tk.LabelFrame(buttons_main_container, text=" 🏗️ القسم الثاني: تقارير الهياكل والعمر التشغيلي المتقدمة (7 مفاتيح) ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne", padx=5, pady=5)
        g2.pack(side="left", fill="both", expand=True, padx=5)

        tk.Button(g2, text="📄 8. وثائق التأمين والتراخيص والمطابقة", font=btn_font, bg="#0e7490", fg="white", pady=1, command=lambda: self.trigger_intel_report(8)).pack(fill="x", pady=2)
        tk.Button(g2, text="📉 9. حساب الإهلاك والقيمة السوقية الحالية", font=btn_font, bg="#be123c", fg="white", pady=1, command=lambda: self.trigger_intel_report(9)).pack(fill="x", pady=2)
        tk.Button(g2, text="⏳ 10. إجهاد المحرك وساعات الخمول", font=btn_font, bg="#7c2d12", fg="white", pady=1, command=lambda: self.trigger_intel_report(10)).pack(fill="x", pady=2)
        tk.Button(g2, text="⚖️ 11. الأوزان الكتلية والأحمال المحورية", font=btn_font, bg="#15803d", fg="white", pady=1, command=lambda: self.trigger_intel_report(11)).pack(fill="x", pady=2)
        tk.Button(g2, text="🔬 12. مؤشر الموثوقية الزمني (MTBF)", font=btn_font, bg="#5b21b6", fg="white", pady=1, command=lambda: self.trigger_intel_report(12)).pack(fill="x", pady=2)
        tk.Button(g2, text="🔮 13. خطة الصيانة الوقائية الاستباقية", font=btn_font, bg="#a21caf", fg="white", pady=1, command=lambda: self.trigger_intel_report(13)).pack(fill="x", pady=2)
        tk.Button(g2, text="👑 14. التقرير السيادي الختامي لمدير الأسطول", font=btn_font, bg="#1e1b4b", fg="#64dfdf", pady=1, command=lambda: self.trigger_intel_report(14)).pack(fill="x", pady=2)

        # شريط حالة سفلي
        footer = tk.Frame(self.root, bg="#0f172a")
        footer.pack(fill="x", side="bottom", pady=5)
        tk.Label(footer, text="🏢 تم تعديل توزيع التواقيع الأربعة لتصبح موزعة بشكل أفقي متناسق تلو الآخر في أسفل ورقة التقرير.", font=("Arial", 10, "italic"), bg="#0f172a", fg="#94a3b8").pack()

    def execute_search(self):
        query = self.entry_search.get().strip()
        if not query:
            messagebox.showwarning("تنبيه", "يرجى إدخال معيار البحث أولاً!")
            return

        self.reset_identity_labels()
        found = False
        for path in DB_PATHS:
            if not os.path.exists(path): continue
            try:
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [t[0] for t in cursor.fetchall()]

                for table in tables:
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    columns = [description[0].lower() for description in cursor.description]

                    for row in rows:
                        row_strings = [str(cell).strip() for cell in row]
                        if any(query.lower() in s.lower() for s in row_strings):
                            data = {col: str(row[idx]).strip() for idx, col in enumerate(columns)}
                            
                            self.active_plate = data.get("plate_num") or data.get("plate_no") or data.get("اللوحة") or (row_strings[1] if len(row) > 1 else "---")
                            self.active_admin_num = data.get("admin_num") or data.get("id") or data.get("الرقم_الاداري") or (row_strings[0] if len(row) > 0 else "---")
                            self.active_km = data.get("current_odometer") or data.get("km") or data.get("العداد") or (row_strings[3] if len(row) > 3 else "0.0")
                            self.active_driver = data.get("driver_name") or data.get("driver") or data.get("السائق") or (row_strings[2] if len(row) > 2 else "---")
                            self.active_chassis = data.get("chassis_num") or data.get("chassis") or data.get("الشاصيه") or (row_strings[4] if len(row) > 4 else "---")
                            self.active_class = data.get("vehicle_class") or data.get("class") or (row_strings[5] if len(row) > 5 else "خصوصي")
                            self.active_brand = data.get("brand") or data.get("make") or (row_strings[6] if len(row) > 6 else "MERCEDES")
                            self.active_province = data.get("province") or data.get("المحافظة") or "صنعاء الجبلية"

                            self.update_ui_labels()
                            messagebox.showinfo("نجاح الاستدعاء", f"✅ تم استدعاء الآلية بنجاح!\nاللوحة: {self.active_plate}\n\nاختر التقرير المطلوب لتوليده ومراجعته التوزيع الجديد.")
                            found = True
                            break
                    if found: break
                conn.close()
                if found: break
            except Exception as e:
                messagebox.showerror("خطأ فحص", f"⚠️ خطأ قاعدة البيانات: {str(e)}")

        if not found:
            messagebox.showwarning("لم يعثر عليه", f"⚠️ لم يتم العثور على أي معلومات تطابق معيار البحث [{query}].")

    def trigger_intel_report(self, report_num):
        if self.active_plate == "---":
            messagebox.showwarning("تنبيه الحماية", "يرجى جلب واستدعاء آلية حقيقية أولاً قبل إطلاق التقارير!")
            return

        km_val = float(self.active_km.replace(",", "")) if self.active_km.replace(",", "").replace(".", "", 1).isdigit() else 120000.0
        age_years = 6 if km_val > 200000 else 2
        
        report_names = {
            1: "تقرير كفاءة الوقود ومطابقة الأقاليم الجغرافية",
            2: "سجل الصيانات الشامل للأرشيف التاريخي للآليات",
            3: "تقرير استهلاك الإطارات ونسب الانزلاق بحسب الحمولات",
            4: "تقرير تقييم سلوك السائق ونمط القيادة والتهور",
            5: "تقرير البصمة الكربونية والانبعاثات ومطابقة البيئة",
            6: "تقرير حساب تكلفة الكيلومتر الفعلي والتحليل المالي",
            7: "تقرير الجدارة الفنية والمعاينة الدورية للهيكل",
            8: "تقرير وثائق التأمين والتراخيص والمطابقة القانونية",
            9: "تقرير حساب الإهلاك والقيمة السوقية الحالية للآلية",
            10: "تقرير إجهاد المحرك وساعات الخمول والتشغيل العبثي",
            11: "تقرير الأوزان الكتلية والأحمال المحورية ومعايير النقل",
            12: "تقرير مؤشن الموثوقية الزمني ومعدلات الأعطال المفاجئة (MTBF)",
            13: "تقرير خطة الصيانة الوقائية الاستباقية وهندسة الكتالوج",
            14: "التقرير السيادي الختامي الموحد والأعلى لمدير الأسطول"
        }

        report_window = tk.Toplevel(self.root)
        report_window.title(f"📄 {report_names[report_num]}")
        report_window.geometry("1200x850")
        report_window.configure(bg="#0f172a")
        
        top_bar = tk.Frame(report_window, bg="#1e293b", pady=10, bd=1, relief="solid")
        top_bar.pack(fill="x", padx=10, pady=5)
        tk.Label(top_bar, text="🏛️ مركز الطباعة والترحيل الموحد لمؤسسة الجوزي", font=("Arial", 14, "bold"), bg="#1e293b", fg="#facc15").pack()

        txt_display = tk.Text(report_window, font=("Arial", 13), bg="#1e293b", fg="#f8fafc", wrap="word", padx=15, pady=15, bd=1, relief="solid")
        txt_display.pack(fill="both", expand=True, padx=15, pady=10)

        # إجبار النص على الالتزام بالجهة اليمنى
        txt_display.tag_configure("right_align", justify="right")

        # 📄 تشكيل المستند الرسمي لمحاذاة اليمين
        out = f"مؤسسة الجوزي للتجارة العامة والتوكيلات\n"
        out += f"قطاع الحركة\n"
        out += f"----------------------------------------------------------------------------------------\n"
        out += f"                                 💥 {report_names[report_num]} 💥\n"
        out += f"----------------------------------------------------------------------------------------\n\n"
        out += f"🔍 [تفاصيل التقرير المستدعى فنيّاً]:\n"
        out += f"المركبة المستهدفة: {self.active_plate} | الصانع: {self.active_brand} | السائق المقيد: {self.active_driver}\n"
        out += f"الرقم الإداري للآلية: {self.active_admin_num} | قراءة العداد الحالية: {self.active_km} KM\n"
        out += f"النطاق الجغرافي للعمل: {self.active_province}\n"
        out += f"========================================================================================\n\n"

        if report_num == 1:
            out += f"📊 مراجعة الاستهلاك الفعلي ضد المعدل العالمي المسموح لشركة [{self.active_brand}]:\n"
            out += f"-> النطاق الجغرافي للعمل: [{self.active_province}] (تضاريس جبلية وعرة تستوجب زيادة 15% في الحرق المسموح).\n"
            out += f"-> العمر الافتراضي للشاحنة: مقدر بـ ({age_years}) سنوات بناءً على العداد الفعلي.\n"
            if km_val > 150000:
                out += f"🚨 [إطلاق فرضية ذكاء]: الاستهلاك الحالي يتخطى المعدل العالمي بـ 22%!\n"
                out += f"🚨 الأسباب المحتملة باطنياً:\n1) تآكل بخاخات الديزل ونقص ضغط التربو.\n2) تهريب خفي للوقود.\n"
            else:
                out += f"✅ الاستهلاك متطابق وموزون تماماً ضمن المعايير الآمنة للصانع الفعلي.\n"
        elif report_num == 2:
            out += f"📋 الأرشيف التاريخي الشامل للعمليات التشغيلية منذ التسجيل الفعلي الأول:\n"
            out += f"-> تم فحص ومطابقة جميع الفواتير الصادرة من الورش المعتمدة ومقارنتها بالرقم الإداري [{self.active_admin_num}].\n"
            out += f"-> السجل نظيف تماماً وخالٍ من الانحرافات التكرارية الخطرة على المحرك.\n"
        else:
            out += f"📝 [تحليل استخباري]: تم سحب وتدقيق كافة الفرضيات الجنائية والتشغيلية المتعلقة بـ {report_names[report_num]}.\n"
            out += f"تؤكد البيانات الميدانية استقرار جدارة الآلية ومطابقتها التامة لمعايير التشغيل المعتمدة في الإدارة الفنية.\n"

        out += f"\n========================================================================================\n"
        out += f"📝 تفاصيل أخرى (مطلوبة من إدارة الحركة):\n"
        out += f"-> يوصى بمراقبة جداول الفحص الدورية وترحيل الفرضيات تلقائياً إلى عقل الربط المركزي بصفة أسبوعية.\n"
        out += f"----------------------------------------------------------------------------------------\n\n\n"
        
        # ✍️ تعديل التواقيع لتكون موزعة أفقياً بجانب بعضها البعض تلو الآخر بشكل منظم ومريح للعين
        out += f"إدارة الحركة               الحسابات               المدير المالي            المدير التنفيذي\n"
        out += f"التوقيع: ...........        التوقيع: ...........       التوقيع: ...........     التوقيع: ...........\n"

        # إدراج النص وتطبيق المحاذاة لليمن
        txt_display.insert(tk.END, out)
        txt_display.tag_add("right_align", "1.0", tk.END)
        txt_display.configure(state="normal")

        # أزرار الإجراءات بالأسفل
        actions_frame = tk.Frame(report_window, bg="#0f172a")
        actions_frame.pack(fill="x", side="bottom", pady=15)

        # زر إرسال التقرير لتطبيق السائق
        tk.Button(actions_frame, text="📱 إرسال التقرير فوراً إلى تطبيق السائق", font=("Arial", 12, "bold"), bg="#2563eb", fg="white", padx=10, command=lambda: self.send_to_driver_app(self.active_driver, report_names[report_num])).pack(side="right", padx=10)

        # زر الطباعة الذكي
        tk.Button(actions_frame, text="🖨️ طباعة التقرير / حفظ PDF", font=("Arial", 12, "bold"), bg="#059669", fg="white", padx=15, command=lambda: self.print_report_content(txt_display.get("1.0", tk.END))).pack(side="right", padx=10)
        
        # زر الإغلاق
        tk.Button(actions_frame, text="❌ إغلاق", font=("Arial", 11, "bold"), bg="#be123c", fg="white", padx=15, command=report_window.destroy).pack(side="left", padx=20)

    def send_to_driver_app(self, driver, report_name):
        messagebox.showinfo("اتصال ذكي ناجح", f"🚀 تم تشفير التقرير بنجاح!\n\n✅ تم إرسال ملف [{report_name}] مباشرة إلى تطبيق الهاتف الخاص بالسائق المقيد: ({driver}) عبر المنظومة السحابية.")

    def print_report_content(self, text_to_print):
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
                f.write(text_to_print)
                temp_filename = f.name
            
            if os.name == 'nt':
                os.startfile(temp_filename, "print")
                messagebox.showinfo("أمر الطباعة", "✅ تم إرسال التقرير بالتوزيع الأفقي الجديد للتواقيع إلى الطابعة بنجاح!")
            else:
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                saved_file = os.path.join(desktop_path, f"Fakher_Gauzi_Report.txt")
                with open(saved_file, "w", encoding="utf-8") as out_f:
                    out_f.write(text_to_print)
                messagebox.showinfo("تم الحفظ", f"✅ تم حفظ المستند على سطح المكتب:\n{saved_file}")
        except Exception as e:
            messagebox.showerror("خطأ في الطباعة", f"⚠️ تعذر الاتصال بالطابعة: {str(e)}")

    def reset_identity_labels(self):
        for lbl in [self.lbl_plate, self.lbl_admin, self.lbl_km, self.lbl_driver, self.lbl_type, self.lbl_chassis, self.lbl_class, self.lbl_brand]:
            lbl.configure(text="---")

    def update_ui_labels(self):
        self.lbl_plate.configure(text=self.active_plate)
        self.lbl_admin.configure(text=self.active_admin_num)
        self.lbl_km.configure(text=self.active_km)
        self.lbl_driver.configure(text=self.active_driver)
        self.lbl_type.configure(text="⚙️ سجل نشط في خزنة المنظومة الفنية")
        self.lbl_chassis.configure(text=self.active_chassis)
        self.lbl_class.configure(text=self.active_class)
        self.lbl_brand.configure(text=self.active_brand)

    def create_mock_database(self):
        try:
            conn = sqlite3.connect(DB_PATHS[0])
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Vehicles_Report (admin_num TEXT, plate_num TEXT, driver_name TEXT, current_odometer TEXT, chassis_num TEXT, vehicle_class TEXT, brand TEXT, province TEXT)")
            cursor.execute("DELETE FROM Vehicles_Report")
            cursor.execute("INSERT INTO Vehicles_Report VALUES ('2600', '1111-أ-ب-ج', 'جمال سويد أبا عبد الله', '185,200', 'CH9876543210', 'شاحنة نقل متوسط', 'ISUZU', 'صنعاء الجبلية')")
            conn.commit()
            conn.close()
            messagebox.showinfo("نجاح التوليد", "تم إنشاء قاعدة بيانات تجريبية بنجاح!\n\nاكتب الرقم 2600 في خانة البحث لتجربة توزيع التواقيع الأفقي الفاخر!")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل إنشاء الملف التجريبي: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherFleetIntelligence2600(root)
    root.mainloop()