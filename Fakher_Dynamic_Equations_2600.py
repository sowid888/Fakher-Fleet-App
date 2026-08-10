# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - لوحة معادلات الصيانة والتذكيرات الموحدة
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم المعتمد: Fakher_Dynamic_Equations_2600
التعديل الإستراتيجي: دمج نظام المعادلات والتذكيرات، إضافة 15 حقل احتياطي للشاحنات و10 حقول للسيارات، وتوزيع عرضي كامل.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

DB_PATH = "Fakher_System_2026.db"

class FakherDynamicEquations2600:
    def __init__(self, root):
        self.root = root
        self.root.title("⚙️ منظومة فاخر 2600 - لوحة المعادلات والتذكيرات الموحدة والحقول المستقبلية ⚙️")
        self.root.geometry("1700x950")
        self.root.configure(bg="#0f172a")
        
        self.car_dynamic_fields = []
        self.truck_dynamic_fields = []
        
        self.setup_equations_and_alerts_table()
        self.build_ui()
        self.load_current_settings()

    def setup_equations_and_alerts_table(self):
        """ إنشاء وتأمين جدول المعادلات والتذكيرات الموحد في الخزنة المركزية لعام 2026 """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Maintenance_Rules_Config (
                part_key TEXT PRIMARY KEY,
                part_name TEXT,
                vehicle_type TEXT,
                custom_threshold INTEGER,
                unit_label TEXT
            )
        """)
        
        # مصفوفة القواعد الأساسية + الحقول الاحتياطية الجديدة المفتوحة للاستبدالات والتذكيرات
        default_rules = [
            # === سيارات (6 أساسية + 10 حقول احتياطية فارغة بالكامل للصيانة والتذكيرات) ===
            ('car_oil', 'زيت المحرك', 'Car', 5000, 'كم أو ميل'),
            ('car_oil_filter', 'فلتر الزيت', 'Car', 10000, 'كم أو ميل'),
            ('car_air_filter', 'فلتر الهواء', 'Car', 15000, 'كم أو ميل'),
            ('car_plugs', 'البلاكات (الشمعات)', 'Car', 30000, 'كم أو ميل'),
            ('car_gear_oil', 'زيت الجير', 'Car', 40000, 'كم أو ميل'),
            ('car_coolant', 'ماء التبريد (الرديتر)', 'Car', 50000, 'كم أو ميل'),
            ('car_future_1', '[تذكير/صيانة سيارات فارغ 1]', 'Car', 0, 'كم أو ميل'),
            ('car_future_2', '[تذكير/صيانة سيارات فارغ 2]', 'Car', 0, 'كم أو ميل'),
            ('car_future_3', '[تذكير/صيانة سيارات فارغ 3]', 'Car', 0, 'كم أو ميل'),
            ('car_future_4', '[تذكير/صيانة سيارات فارغ 4]', 'Car', 0, 'كم أو ميل'),
            ('car_future_5', '[تذكير/صيانة سيارات فارغ 5]', 'Car', 0, 'كم أو ميل'),
            ('car_future_6', '[تذكير/صيانة سيارات فارغ 6]', 'Car', 0, 'كم أو ميل'),
            ('car_future_7', '[تذكير/صيانة سيارات فارغ 7]', 'Car', 0, 'كم أو ميل'),
            ('car_future_8', '[تذكير/صيانة سيارات فارغ 8]', 'Car', 0, 'كم أو ميل'),
            ('car_future_9', '[تذكير/صيانة سيارات فارغ 9]', 'Car', 0, 'كم أو ميل'),
            ('car_future_10', '[تذكير/صيانة سيارات فارغ 10]', 'Car', 0, 'كم أو ميل'),
            
            # === شاحنات (11 أساسية بنظام KM وتواقيت دورية + 15 حقل احتياطي فارغ بالكامل للصيانة والتذكيرات) ===
            ('trk_oil', 'زيت المحرك (الديزل)', 'Truck', 5000, 'كيلومتر (KM)'),
            ('trk_oil_filter', 'فلتر الزيت الثقيل', 'Truck', 10000, 'كيلومتر (KM)'),
            ('trk_air_filter', 'فلتر الهواء العملاق', 'Truck', 15000, 'كيلومتر (KM)'),
            ('trk_gear_oil', 'زيت الجير الكبير', 'Truck', 40000, 'كيلومتر (KM)'),
            ('trk_coolant', 'ماء الرديتر الضخم', 'Truck', 50000, 'كيلومتر (KM)'),
            ('trk_diff_oil', 'زيت الكارونة (الدفرنش)', 'Truck', 40000, 'كيلومتر (KM)'),
            ('trk_fuel_filter', 'فلتر الوقود (الديزل) الرئيسي', 'Truck', 15000, 'كيلومتر (KM)'),
            ('trk_water_sep', 'فلتر فصل الماء عن الديزل', 'Truck', 15000, 'كيلومتر (KM)'),
            ('trk_brake_sys', 'صيانة نظام هواء الفرامل', 'Truck', 30000, 'كيلومتر (KM)'),
            ('trk_tyres_check', 'وزنية ومراجعة الإطارات دورياً', 'Truck', 2, 'يوم (كل يومين)'),
            ('trk_box_clean', 'تنظيف صندوق الشاحنة الفني', 'Truck', 7, 'يوم (كل أسبوع)'),
            ('trk_future_1', '[تذكير/صيانة شاحنات فارغ 1]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_2', '[تذكير/صيانة شاحنات فارغ 2]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_3', '[تذكير/صيانة شاحنات فارغ 3]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_4', '[تذكير/صيانة شاحنات فارغ 4]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_5', '[تذكير/صيانة شاحنات فارغ 5]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_6', '[تذكير/صيانة شاحنات فارغ 6]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_7', '[تذكير/صيانة شاحنات فارغ 7]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_8', '[تذكير/صيانة شاحنات فارغ 8]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_9', '[تذكير/صيانة شاحنات فارغ 9]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_10', '[تذكير/صيانة شاحنات فارغ 10]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_11', '[تذكير/صيانة شاحنات فارغ 11]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_12', '[تذكير/صيانة شاحنات فارغ 12]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_13', '[تذكير/صيانة شاحنات فارغ 13]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_14', '[تذكير/صيانة شاحنات فارغ 14]', 'Truck', 0, 'كيلومتر (KM)'),
            ('trk_future_15', '[تذكير/صيانة شاحنات فارغ 15]', 'Truck', 0, 'كيلومتر (KM)')
        ]
        
        for rule in default_rules:
            cursor.execute("INSERT OR IGNORE INTO Maintenance_Rules_Config VALUES (?, ?, ?, ?, ?)", rule)
            
        conn.commit()
        conn.close()

    def build_ui(self):
        # 1. شريط العنوان الإستراتيجي الفخم
        top_bar = tk.Frame(self.root, bg="#1e293b", bd=1, relief="solid")
        top_bar.pack(fill="x", padx=15, pady=10)
        
        tk.Label(top_bar, text="⚙️ لوحة التذكيرات والمعادلات الموحدة لأسطول الـ 100 مركبة - الحقول الحرة لعام 2026 ⚙️", 
                 font=("Arial", 12, "bold"), bg="#1e293b", fg="#38bdf8").pack(side="right", padx=15, pady=12)

        # زر الحفظ الموحد أسفل الشاشة
        btn_save_panel = tk.Frame(self.root, bg="#0f172a")
        btn_save_panel.pack(side="bottom", fill="x", padx=15, pady=15)
        
        tk.Button(btn_save_panel, text="💾 اعتماد وحفظ كافة معادلات الصيانة والتذكيرات الجديدة فوراً في الخزنة المركزية 2600", 
                  font=("Arial", 12, "bold"), bg="#10b981", fg="white", height=2, cursor="hand2",
                  command=self.save_all_settings_to_db).pack(fill="x", padx=10)

        # حاوية رئيسية قابلة للتمرير (Scrollable) لضمان رؤية كافة الحقول الـ 42 دون تكدس أو اختفاء
        outer_frame = tk.Frame(self.root, bg="#0f172a")
        outer_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        canvas = tk.Canvas(outer_frame, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0f172a")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ================= قسم السيارات الصغيرة (طوابير عرضية متناسقة) =================
        self.car_panel = tk.LabelFrame(scrollable_frame, text=" 🚗 حقول صيانة وتذكيرات السيارات الصغيرة المفتوحة (توزيع 3 طوابير) ", 
                                   font=("Arial", 11, "bold"), bg="#1e293b", fg="#a7f3d0", labelanchor="ne")
        self.car_panel.pack(fill="x", padx=10, pady=10)

        # ================= قسم الشاحنات الكبيرة (طوابير عرضية متناسقة - كيلومتر فقط) =================
        self.truck_panel = tk.LabelFrame(scrollable_frame, text=" 🚚 حقول صيانة وتذكيرات الشاحنات الثقيلة والموزعين (توزيع 3 طوابير - نظام KM حتمي) ", 
                                     font=("Arial", 11, "bold"), bg="#1e293b", fg="#fbbf24", labelanchor="ne")
        self.truck_panel.pack(fill="x", padx=10, pady=5)

    def load_current_settings(self):
        """ سحب المسافات والأيام وتوزيعها في طوابير ثلاثية محصنة هندسياً """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT part_key, part_name, vehicle_type, custom_threshold, unit_label FROM Maintenance_Rules_Config")
        rows = cursor.fetchall()
        conn.close()

        car_col, car_row = 0, 0
        truck_col, truck_row = 0, 0

        for row in rows:
            key, name, v_type, val, unit = row
            
            if v_type == 'Car':
                # بناء خلية العرض للسيارات
                cell_frame = tk.Frame(self.car_panel, bg="#1e293b", bd=1, relief="groove")
                cell_frame.grid(row=car_row, column=car_col, padx=15, pady=8, sticky="ew")
                
                ent_name = tk.Entry(cell_frame, font=("Arial", 10, "bold"), width=24, justify="right", bg="#1e293b", fg="white", bd=0)
                ent_name.insert(0, name)
                ent_name.pack(side="right", padx=5, pady=5)
                
                ent_val = tk.Entry(cell_frame, font=("Arial", 10, "bold"), width=9, justify="center", bg="#334155", fg="#38bdf8", bd=1)
                ent_val.insert(0, str(val))
                ent_val.pack(side="right", padx=5, pady=5)
                
                lbl_unit = tk.Label(cell_frame, text="كم/ميل" if "فارغ" in name or "[" in name else unit, font=("Arial", 9), bg="#1e293b", fg="#94a3b8")
                lbl_unit.pack(side="right", padx=3)

                self.car_dynamic_fields.append((key, ent_name, ent_val))
                
                car_col += 1
                if car_col > 2: # تنظيم الحقول لتقف في 3 طوابير عرضية
                    car_col = 0
                    car_row += 1

            elif v_type == 'Truck':
                # بناء خلية العرض للشاحنات والموزعين
                cell_frame = tk.Frame(self.truck_panel, bg="#1e293b", bd=1, relief="groove")
                cell_frame.grid(row=truck_row, column=truck_col, padx=15, pady=8, sticky="ew")
                
                ent_name = tk.Entry(cell_frame, font=("Arial", 10, "bold"), width=24, justify="right", bg="#1e293b", fg="white", bd=0)
                ent_name.insert(0, name)
                ent_name.pack(side="right", padx=5, pady=5)
                
                entry_fg = "#f43f5e" if "يوم" in unit else "#fbbf24"
                
                ent_val = tk.Entry(cell_frame, font=("Arial", 10, "bold"), width=9, justify="center", bg="#334155", fg=entry_fg, bd=1)
                ent_val.insert(0, str(val))
                ent_val.pack(side="right", padx=5, pady=5)
                
                lbl_unit = tk.Label(cell_frame, text="يوم" if "يوم" in unit else "KM", font=("Arial", 9), bg="#1e293b", fg="#94a3b8")
                lbl_unit.pack(side="right", padx=3)

                self.truck_dynamic_fields.append((key, ent_name, ent_val))
                
                truck_col += 1
                if truck_col > 2: # تنظيم الحقول لتقف في 3 طوابير عرضية
                    truck_col = 0
                    truck_row += 1

        # تأمين التمدد العرضي المتساوي لكافة الطوابير
        for i in range(3):
            self.car_panel.columnconfigure(i, weight=1)
            self.truck_panel.columnconfigure(i, weight=1)

    def save_all_settings_to_db(self):
        """ التقاط كافة الأسماء المعدلة والتذكيرات المدخلة وحقنها دفعة واحدة في الخزنة 2600 """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            # 1. حفظ تحديثات السيارات (16 حقل)
            for key, ent_name, ent_val in self.car_dynamic_fields:
                updated_name = ent_name.get().strip()
                updated_val = int(ent_val.get().strip())
                cursor.execute("UPDATE Maintenance_Rules_Config SET part_name=?, custom_threshold=? WHERE part_key=?", 
                               (updated_name, updated_val, key))
                
            # 2. حفظ تحديثات الشاحنات (26 حقل)
            for key, ent_name, ent_val in self.truck_dynamic_fields:
                updated_name = ent_name.get().strip()
                updated_val = int(ent_val.get().strip())
                cursor.execute("UPDATE Maintenance_Rules_Config SET part_name=?, custom_threshold=? WHERE part_key=?", 
                               (updated_name, updated_val, key))
                
            conn.commit()
            messagebox.showinfo("تم الحفظ السيادي الموحد", "✅ تم بنجاح دمج وحفظ كافة معادلات الصيانة والتذكيرات، وتسمية كافة الحقول الاحتياطية للسيارات (10 حقول) وللشاحنات (15 حقل) بنجاح تام!")
        
        except ValueError:
            messagebox.showerror("خطأ في المدخلات", "❌ يرجى التأكد من كتابة أرقام صحيحة فقط في خانات المسافات (ضع 0 إذا كانت غير مستخدمة حالياً، ولا تترك أي خانة فارغة)!")
        except Exception as e:
            messagebox.showerror("خطأ في قاعدة البيانات", f"تعذر حفظ التعديلات: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherDynamicEquations2600(root)
    root.mainloop()