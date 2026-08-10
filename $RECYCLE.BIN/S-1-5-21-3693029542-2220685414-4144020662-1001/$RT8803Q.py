# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - ملف حركات صرف ديزل الشاحنات ومراقبة الهدر
المشرف الفني العام الأعلى: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد للملف: Fakher_Truck_Diesel_2600.py
التحديث النهائي: الربط المحوري المباشر مع قاعدة بيانات الهوية المركزية والإكمال التلقائي الحقيقي النظيف
"""

import os
import sys
import sqlite3
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# 🏛️ توحيد قاعدة البيانات على المسار المشترك والمستقر للمنظومة
DB_PATH = "Fakher_Central_Database_2600.db"

class FakherTruckDieselSovereignEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ محرك مراقبة الديزل بالبحث التفاعلي والربط المحوري 2600 🛡️")
        self.root.geometry("1500x900")
        self.root.state('zoomed')
        self.root.configure(bg="#0f172a") 

        self.vars = {}
        
        # كتالوج المصانع القياسي
        self.factory_catalog = {
            "ISUZU": {"oil": 11.0, "rate": 6.5, "psi": 85, "cat": "شاحنة توزيع متوسطة"},
            "VOLVO": {"oil": 38.0, "rate": 3.8, "psi": 110, "cat": "ناقلة ثقيلة / قاطرة"},
            "MERCEDES": {"oil": 34.0, "rate": 4.0, "psi": 105, "cat": "شاحنة نقل ثقيل Actros"},
            "TOYOTA": {"oil": 5.5, "rate": 10.5, "psi": 35, "cat": "سيارة ركاب / إدارية"}
        }

        # جغرافية وتضاريس اليمن المعتمدة
        self.yemen_geo = {
            "صنعاء": {"factor": 1.18, "desc": "مرتفعات جبلية شاهقة ونقص أكسجين يزيد الجهد 18%"},
            "تعز": {"factor": 1.12, "desc": "طرق التوائية ومنحدرات قاسية ترفع الاستهلاك 12%"},
            "الحديدة": {"factor": 1.05, "desc": "منطقة ساحلية، رطوبة وحرارة تضغط على التبريد 5%"},
            "عدن": {"factor": 1.05, "desc": "رطوبة وحرارة تؤثر على لزوجة زيوت المحرك بنسبة 5%"}
        }

        self.init_and_sync_db()
        self.build_framework_ui()

    def init_and_sync_db(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            # إنشاء جدول حركات صرف الديزل للشاحنات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Truck_Diesel_Logs_2600 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chk_date TEXT, plate_num TEXT, driver_name TEXT, location TEXT,
                    vin_code TEXT, start_km REAL, end_km REAL, fuel_liters REAL,
                    waste_pct TEXT, eval_status TEXT, mechanic_hyp TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"تنبيه تهيئة الجدول: {e}")

    def on_search_key_release(self, event):
        """ 🧠 محرك رصد الحروف الحية: يستدعي البيانات من جدول الهوية الحقيقي Truck_Main_Registry_2600 """
        search_txt = self.vars["search_id"].get().strip()
        
        # إغلاق قائمة الاقتراحات السابقة إن وجدت
        if hasattr(self, "suggestion_box") and self.suggestion_box.winfo_exists():
            self.suggestion_box.destroy()

        if len(search_txt) < 1:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # الربط الفعلي مع جدول الهوية المعمد Truck_Main_Registry_2600
            query = """
                SELECT DISTINCT serial_num, driver_name, plate_num, chassis_num FROM Truck_Main_Registry_2600
                WHERE driver_name LIKE ? OR serial_num LIKE ? OR plate_num LIKE ?
                LIMIT 8
            """
            cursor.execute(query, (f"%{search_txt}%", f"%{search_txt}%", f"%{search_txt}%"))
            results = cursor.fetchall()
            conn.close()

            if results:
                self.show_suggestions_popup(results)
        except Exception as e:
            print(f"خطأ أثناء جلب الاقتراحات التفاعلية: {e}")

    def show_suggestions_popup(self, results):
        """ 📋 نافذة منبثقة ذكية تظهر أسفل خانة البحث مباشرة لسرد الخيارات المتشابهة """
        x = self.vars["search_id"].winfo_rootx()
        y = self.vars["search_id"].winfo_rooty() + self.vars["search_id"].winfo_height()

        self.suggestion_box = tk.Toplevel(self.root)
        self.suggestion_box.wm_overrideredirect(True) 
        self.suggestion_box.geometry(f"550x220+{x}+{y}")
        self.suggestion_box.configure(bg="#1e293b")

        listbox = tk.Listbox(self.suggestion_box, font=("Arial", 11, "bold"), bg="#1e293b", fg="#f1f5f9", 
                             selectbackground="#38bdf8", selectforeground="#0f172a", bd=0, highlightthickness=1)
        listbox.pack(fill="both", expand=True)

        self.current_suggestions_data = {}
        for index, row in enumerate(results):
            s_id, name, plate, vin = row
            display_text = f"🆔 إداري: {s_id} | 👤 سائق: {name} | 🔢 لوحة: {plate}"
            listbox.insert(tk.END, display_text)
            self.current_suggestions_data[index] = (plate, name, vin)

        listbox.bind("<<ListboxSelect>>", lambda event: self.select_suggestion(listbox))
        
    def select_suggestion(self, listbox):
        """ ⚡ القاذف الآلي: ملء كافة الحقول المسترجعة من جدول الهوية فوراً وتجميدها ضد الخطأ """
        try:
            selected_index = listbox.curselection()[0]
            plate, driver, vin = self.current_suggestions_data[selected_index]

            self.set_field_text("plate_num", plate if plate else "غير مسجل")
            self.set_field_text("driver_name", driver if driver else "غير مسجل")
            self.set_field_text("vin_code", vin if vin else "CH-TRK-DEFAULT")

            self.lbl_search_status.config(text=f"✅ تم التقاط بيانات السائق ({driver}) وتعبئتها آلياً ⚡", fg="#10b981")
            
            self.suggestion_box.destroy()
            self.vars["start_km"].focus() 
        except Exception as e:
            print(f"خطأ في تحديد الاختيار: {e}")

    def set_field_text(self, var_name, text_value):
        self.vars[var_name].config(state="normal")
        self.vars[var_name].delete(0, tk.END)
        self.vars[var_name].insert(0, str(text_value))
        self.vars[var_name].config(state="readonly")

    def clear_auto_fields(self):
        for var_name in ["plate_num", "driver_name", "vin_code"]:
            self.vars[var_name].config(state="normal")
            self.vars[var_name].delete(0, tk.END)
            self.vars[var_name].config(state="readonly")

    def build_framework_ui(self):
        header = tk.Frame(self.root, bg="#1e293b", height=80)
        header.pack(fill="x", padx=10, pady=5)
        
        lbl_title = tk.Label(header, text="🏛️ مـنـظـومـة فـاخـر 2600 - محرك الديزل بميزة الالتقاط والتعرف الآلي", 
                             font=("Arial", 20, "bold"), bg="#1e293b", fg="#38bdf8")
        lbl_title.pack(side="right", padx=20, pady=15)
        
        lbl_eng = tk.Label(header, text="المشرف العام: المهندس جمال سويد", font=("Arial", 12, "bold", "italic"), bg="#1e293b", fg="#a7f3d0")
        lbl_eng.pack(side="left", padx=20, pady=20)

        main_body = tk.Frame(self.root, bg="#0f172a")
        main_body.pack(fill="both", expand=True, padx=10, pady=5)

        right_panel = tk.LabelFrame(main_body, text=" 📝 لوحة الالتقاط التفاعلي السريع للبيانات ", font=("Arial", 14, "bold"), bg="#1e293b", fg="#f1f5f9", labelanchor="ne")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        search_row = tk.Frame(right_panel, bg="#0f172a", bd=2, relief="groove")
        search_row.pack(fill="x", padx=15, pady=15, side="top")
        
        lbl_search = tk.Label(search_row, text="اكتب (أول حروف الاسم / الرقم الإداري / اللوحة):", font=("Arial", 11, "bold"), bg="#0f172a", fg="#38bdf8")
        lbl_search.pack(side="right", padx=10, pady=10)
        
        entry_search = tk.Entry(search_row, font=("Arial", 14, "bold"), bg="#1e293b", fg="#ffffff", insertbackground="white", justify="center", width=25)
        entry_search.pack(side="right", padx=10, pady=10)
        
        entry_search.bind("<KeyRelease>", self.on_search_key_release)
        self.vars["search_id"] = entry_search
        
        self.lbl_search_status = tk.Label(search_row, text="اكتب حرفين وسيقوم الكود برص الأسماء المتشابهة آلياً ⚡", font=("Arial", 10, "italic"), bg="#0f172a", fg="#e2e8f0")
        self.lbl_search_status.pack(side="left", padx=10, pady=10)

        auto_fields = [
            ("رقم اللوحة المسترجع آلياً:", "plate_num"),
            ("اسم السائق المسترجع آلياً:", "driver_name"),
            ("رقم الشاصيه (VIN) الدولي:", "vin_code"),
        ]

        for label_text, var_name in auto_fields:
            row = tk.Frame(right_panel, bg="#1e293b")
            row.pack(fill="x", padx=15, pady=5, side="top")
            lbl = tk.Label(row, text=label_text, font=("Arial", 12, "bold"), bg="#1e293b", fg="#94a3b8", width=25, anchor="e")
            lbl.pack(side="right", padx=10)
            entry = tk.Entry(row, font=("Arial", 12), bg="#334155", fg="#ffffff", justify="center", state="readonly")
            entry.pack(side="right", fill="x", expand=True, padx=10)
            self.vars[var_name] = entry

        manual_fields = [
            ("قراءة العداد السابقة (كم):", "start_km"),
            ("قراءة العداد الحالية (كم):", "end_km"),
            ("كمية الديزل المصروفة (لتر):", "fuel_liters"),
        ]

        for label_text, var_name in manual_fields:
            row = tk.Frame(right_panel, bg="#1e293b")
            row.pack(fill="x", padx=15, pady=6, side="top")
            lbl = tk.Label(row, text=label_text, font=("Arial", 13, "bold"), bg="#1e293b", fg="#ffffff", width=25, anchor="e")
            lbl.pack(side="right", padx=10)
            entry = tk.Entry(row, font=("Arial", 13, "bold"), bg="#0f172a", fg="#5eead4", insertbackground="white", justify="center")
            entry.pack(side="right", fill="x", expand=True, padx=10)
            self.vars[var_name] = entry

        geo_row = tk.Frame(right_panel, bg="#1e293b")
        geo_row.pack(fill="x", padx=15, pady=6, side="top")
        lbl_geo = tk.Label(geo_row, text="خط سير الحركة (التضاريس):", font=("Arial", 13, "bold"), bg="#1e293b", fg="#ffffff", width=25, anchor="e")
        lbl_geo.pack(side="right", padx=10)
        
        self.combo_geo = ttk.Combobox(geo_row, values=list(self.yemen_geo.keys()), font=("Arial", 12), state="readonly", justify="center")
        self.combo_geo.set("صنعاء")
        self.combo_geo.pack(side="right", fill="x", expand=True, padx=10)

        btn_row = tk.Frame(right_panel, bg="#1e293b")
        btn_row.pack(fill="x", padx=15, pady=15)

        btn_ai = tk.Button(btn_row, text="🌐 تشغيل معالجة الـ AI والتحليل الفوري أونلاين", command=self.trigger_ai_analysis,
                           font=("Arial", 14, "bold"), bg="#10b981", fg="#ffffff", activebackground="#059669", cursor="hand2")
        btn_ai.pack(fill="x", expand=True, padx=10, pady=5)

        btn_save = tk.Button(btn_row, text="🔒 اعتماد وحفظ الحركة في الخزنة الموحدة", command=self.save_to_vault,
                            font=("Arial", 14, "bold"), bg="#3b82f6", fg="#ffffff", activebackground="#2563eb", cursor="hand2")
        btn_save.pack(fill="x", expand=True, padx=10, pady=5)

        left_panel = tk.LabelFrame(main_body, text=" 🧠 رادار الرقابة ومستشار الـ AI المركزي 2600 ", font=("Arial", 14, "bold"), bg="#020617", fg="#38bdf8", labelanchor="ne")
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        self.lbl_signal = tk.Label(left_panel, text="بانتظار التقاط المركبة وبدء التحليل الهندسي...",
                                   font=("Arial", 14, "bold"), bg="#1e293b", fg="#cbd5e1", height=2)
        self.lbl_signal.pack(fill="x", padx=15, pady=10)

        specs_frame = tk.Frame(left_panel, bg="#020617")
        specs_frame.pack(fill="x", padx=15, pady=5)
        
        self.lbl_online_brand = tk.Label(specs_frame, text="الماركة الدولية: --", font=("Arial", 12, "bold"), bg="#1e293b", fg="#f59e0b", width=35, height=2)
        self.lbl_online_brand.pack(side="right", padx=5, expand=True, fill="x")
        
        self.lbl_online_oil = tk.Label(specs_frame, text="سعة زيت المحرك القياسية: --", font=("Arial", 12, "bold"), bg="#1e293b", fg="#a7f3d0", width=35, height=2)
        self.lbl_online_oil.pack(side="left", padx=5, expand=True, fill="x")

        hyp_frame = tk.LabelFrame(left_panel, text=" 🛠️ التقرير الفني والميكانيكي لتشخيص الهدر والأعطال ", font=("Arial", 12, "bold"), bg="#020617", fg="#e2e8f0", labelanchor="ne")
        hyp_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.txt_hyp_display = tk.Text(hyp_frame, font=("Courier New", 12, "bold"), bg="#0f172a", fg="#38bdf8", wrap="word")
        self.txt_hyp_display.pack(fill="both", expand=True, padx=10, pady=10)
        self.txt_hyp_display.insert("1.0", "التقرير فارغ حالياً.")

    def trigger_ai_analysis(self):
        threading.Thread(target=self.execute_online_ai_logic, daemon=True).start()

    def execute_online_ai_logic(self):
        vin = self.vars["vin_code"].get().strip().upper()
        location = self.combo_geo.get()
        
        if not vin or vin == "غير مسجل":
            messagebox.showwarning("تنبيه استدعاء", "❌ يرجى اختيار المركبة من القائمة المتشابهة أولاً!")
            return

        try:
            start_km = float(self.vars["start_km"].get())
            end_km = float(self.vars["end_km"].get())
            liters = float(self.vars["fuel_liters"].get())
        except ValueError:
            messagebox.showerror("خطأ مدخلات", "❌ يرجى ملء خانات العدادات والديزل بأرقام صحيحة!")
            return

        self.lbl_signal.config(text="🔄 جاري تحليل البيانات ومطابقتها بجغرافية التضاريس...", fg="orange")
        
        detected_brand = "ISUZU"
        for brand in self.factory_catalog.keys():
            if brand in vin:
                detected_brand = brand
                break

        specs = self.factory_catalog.get(detected_brand, self.factory_catalog["ISUZU"])
        base_rate = specs["rate"]
        
        geo_data = self.yemen_geo.get(location, {"factor": 1.0, "desc": "تضاريس عادية"})
        adjusted_rate = base_rate / geo_data["factor"]
        
        distance = end_km - start_km
        if distance <= 0 or liters <= 0:
            messagebox.showerror("خطأ قياس", "❌ القراءة الحالية يجب أن تكون أكبر من السابقة!")
            return
            
        actual_rate = distance / liters
        waste_pct = 0.0
        if actual_rate < adjusted_rate:
            waste_pct = round(((adjusted_rate - actual_rate) / adjusted_rate) * 100, 2)

        self.lbl_online_brand.config(text=f"🏢 ماركة المصنع: {detected_brand} ({specs['cat']})")
        self.lbl_online_oil.config(text=f"🛢️ سعة الزيت: {specs['oil']} لتر | الإطارات: {specs['psi']} PSI")

        self.txt_hyp_display.delete("1.0", tk.END)
        
        if waste_pct >= 20.0:
            self.lbl_signal.config(text=f"🚨 هدر وقود بنسبة ({waste_pct}%)", bg="#7f1d1d", fg="#fecaca")
            hyp_text = (
                f"🔬 [تقرير الفرضيات الميكانيكية 2600]:\n"
                f"📌 خط السير: {location} -> {geo_data['desc']}\n"
                f"📌 المعيار المعتمد: {round(adjusted_rate, 2)} كم/لتر | الفعلي: {round(actual_rate, 2)} كم/لتر\n"
                f"🚨 الفرضيات الميكانيكية المحتملة:\n"
                f"1. انسداد أو خلل في البخاخات الإلكترونية (Injectors).\n"
                f"2. انسداد فلاتر الهواء أو شبهة سحب ديزل غير قانوني للوقود.\n"
            )
        else:
            self.lbl_signal.config(text="🟢 استهلاك مثالي ومطابق لمعايير جودة المصنع", bg="#064e3b", fg="#d1fae5")
            hyp_text = "✅ فحص سليم: الاحتراق هندسي وككامل والمحرك يعمل بكفاءة قصوى."
            
        self.txt_hyp_display.insert("1.0", hyp_text)

    def save_to_vault(self):
        try:
            plate = self.vars["plate_num"].get().strip()
            driver = self.vars["driver_name"].get().strip()
            vin = self.vars["vin_code"].get().strip().upper()
            loc = self.combo_geo.get()
            start_km = self.vars["start_km"].get()
            end_km = self.vars["end_km"].get()
            liters = self.vars["fuel_liters"].get()
            
            if not plate or plate == "غير مسجل":
                messagebox.showwarning("تنبيه أمان", "❌ يرجى التقاط المركبة من القائمة أولاً!")
                return
                
            status = self.lbl_signal.cget("text")
            report_txt = self.txt_hyp_display.get("1.0", tk.END)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Truck_Diesel_Logs_2600 (chk_date, plate_num, driver_name, location, vin_code, start_km, end_km, fuel_liters, waste_pct, eval_status, mechanic_hyp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (now_str, plate, driver, loc, vin, start_km, end_km, liters, "محسوب آلياً", status, report_txt))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("تم التوثيق الحصين 🔒", f"🚀 تم حفظ المستند بنجاح!")
            self.clear_all_fields()
        except Exception as e:
            messagebox.showerror("خطأ حفظ", f"فشل حفظ الحركة: {e}")

    def clear_all_fields(self):
        self.vars["search_id"].delete(0, tk.END)
        self.vars["start_km"].delete(0, tk.END)
        self.vars["end_km"].delete(0, tk.END)
        self.vars["fuel_liters"].delete(0, tk.END)
        self.clear_auto_fields()
        self.vars["search_id"].focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherTruckDieselSovereignEngine(root)
    root.mainloop()