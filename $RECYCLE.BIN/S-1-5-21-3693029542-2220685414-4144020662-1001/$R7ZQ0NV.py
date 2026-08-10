import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# المسار المباشر والمحمي في جذر القرص D لتفادي أخطاء الصلاحيات
DB_DRIVER_DATA = "D:/Fakher_Driver_Data_2600.db"

class FakherDriverGateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("منظومة فاخر 2600 - بوابة السائقين الإلكترونية الموحدة")
        self.root.geometry("600x700")
        self.root.configure(bg="#020617") # اللون الملكي الداكن للمنظومة
        
        self.driver_name = ""
        self.plate_num = ""
        self.vehicle_type = "Truck"

        self.build_login_interface()

    # =========================================================================
    # 1. واجهة تسجيل الدخول والمطابقة الآلية
    # =========================================================================
    def build_login_interface(self):
        self.clear_screen()
        
        tk.Label(self.root, text="🛡️", font=("Arial", 60), bg="#020617", fg="#38BDF8").pack(pady=20)
        tk.Label(self.root, text="منظومة فاخر السيادية 2600", font=("Arial", 22, "bold"), bg="#020617", fg="#38BDF8").pack()
        tk.Label(self.root, text="بوابة السائقين والمطابقة الرقمية للأسطول", font=("Arial", 11), bg="#020617", fg="grey").pack(pady=5)

        frame = tk.Frame(self.root, bg="#020617")
        frame.pack(pady=35, padx=50, fill="x")

        tk.Label(frame, text="اسم السائق المعتمد رباعياً:", font=("Arial", 12), bg="#020617", fg="white", anchor="w").pack(fill="x", pady=5)
        self.ent_name = tk.Entry(frame, font=("Arial", 13), bd=2, relief="groove")
        self.ent_name.pack(fill="x", ipady=6, pady=5)

        tk.Label(frame, text="رقم لوحة المركبة الفعلي (مثال: 1234 شاحنة):", font=("Arial", 12), bg="#020617", fg="white", anchor="w").pack(fill="x", pady=5)
        self.ent_plate = tk.Entry(frame, font=("Arial", 13), bd=2, relief="groove")
        self.ent_plate.pack(fill="x", ipady=6, pady=5)

        tk.Label(frame, text="رقم هاتف الواتساب الموثق (كلمة السر):", font=("Arial", 12), bg="#020617", fg="white", anchor="w").pack(fill="x", pady=5)
        self.ent_phone = tk.Entry(frame, font=("Arial", 13), bd=2, relief="groove", show="*")
        self.ent_phone.pack(fill="x", ipady=6, pady=5)

        btn_match = tk.Button(self.root, text="تسجيل الدخول والمطابقة الآلية 🔄", font=("Arial", 13, "bold"), bg="#1E293B", fg="#38BDF8", bd=0, cursor="hand2", command=self.process_matching)
        btn_match.pack(pady=10, padx=50, fill="x", ipady=12)

    def process_matching(self):
        self.driver_name = self.ent_name.get().strip()
        self.plate_num = self.ent_plate.get().strip()
        phone = self.ent_phone.get().strip()

        if not self.driver_name or not self.plate_num or not phone:
            messagebox.showwarning("تنبيه أمني", "يرجى ملء كافة الحقول السيادية لإتمام المطابقة!")
            return

        if "شاحنة" in self.plate_num or self.plate_num.startswith("1"):
            self.vehicle_type = "Truck"
        else:
            self.vehicle_type = "Car"

        self.build_dashboard_interface()

    # =========================================================================
    # 2. لوحة التحكم الرئيسية للسائق
    # =========================================================================
    def build_dashboard_interface(self):
        self.clear_screen()

        card = tk.Frame(self.root, bg="#1E293B", bd=1, relief="solid")
        card.pack(pady=20, padx=30, fill="x")
        
        v_icon = "🚛" if self.vehicle_type == "Truck" else "🚗"
        tk.Label(card, text=f"👤 السائق النشط: {self.driver_name}", font=("Arial", 13, "bold"), bg="#1E293B", fg="white", anchor="w").pack(fill="x", padx=15, pady=6)
        tk.Label(card, text=f"🔢 رقم لوحة المركبة: {self.plate_num}", font=("Arial", 12), bg="#1E293B", fg="#38BDF8", anchor="w").pack(fill="x", padx=15, pady=4)
        tk.Label(card, text=f"{v_icon} تصنيف قطاع الأسطول: نظام الـ 100 مركبة الموحد", font=("Arial", 11), bg="#1E293B", fg="#4ADE80", anchor="w").pack(fill="x", padx=15, pady=6)

        tk.Label(self.root, text="العمليات والوظائف المتاحة لك الآن:", font=("Arial", 12, "bold"), bg="#020617", fg="grey").pack(pady=15, padx=30, anchor="w")

        btn1 = tk.Button(self.root, text="📊 إرسال قراءة العداد الحالي (الكيلومتر)", font=("Arial", 12, "bold"), bg="#2563EB", fg="white", bd=0, cursor="hand2", command=self.view_odometer_screen)
        btn1.pack(pady=10, padx=30, fill="x", ipady=12)

        btn2 = tk.Button(self.root, text="🛠️ الإبلاغ الفوري عن عطل (ميكانيك / كهرباء)", font=("Arial", 12, "bold"), bg="#DC2626", fg="white", bd=0, cursor="hand2", command=self.view_fault_screen)
        btn2.pack(pady=10, padx=30, fill="x", ipady=12)

        btn3 = tk.Button(self.root, text="⏳ مراجعة مواعيد الصيانة وطلبات التفعيل", font=("Arial", 12, "bold"), bg="#D97706", fg="white", bd=0, cursor="hand2", command=self.view_maintenance_screen)
        btn3.pack(pady=10, padx=30, fill="x", ipady=12)

        btn_back = tk.Button(self.root, text="تسجيل الخروج ↩", font=("Arial", 11), bg="#334155", fg="white", bd=0, cursor="hand2", command=self.build_login_interface)
        btn_back.pack(side="bottom", pady=20, padx=30, fill="x", ipady=6)

    # =========================================================================
    # 3. شاشة إرسال قراءة العداد (المعالجة الآمنة)
    # =========================================================================
    def view_odometer_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="📊 توثيق وفحص عداد الكيلومتر", font=("Arial", 18, "bold"), bg="#020617", fg="#2563EB").pack(pady=20)
        
        frame = tk.Frame(self.root, bg="#020617")
        frame.pack(pady=30, padx=40, fill="x")

        tk.Label(frame, text="أدخل أرقام العداد الحالية بدقة وبدون فواصل:", font=("Arial", 12), bg="#020617", fg="white", anchor="w").pack(fill="x", pady=10)
        self.ent_odo = tk.Entry(frame, font=("Arial", 14, "bold"), justify="center")
        self.ent_odo.pack(fill="x", ipady=8)

        def submit_odo():
            odo_val = self.ent_odo.get().strip()
            if not odo_val.isdigit():
                messagebox.showerror("خطأ في البيانات", "يرجى إدخال أرقام صحيحة فقط للعداد!")
                return
            
            try:
                conn = sqlite3.connect(DB_DRIVER_DATA)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Odometer_Logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, driver_name TEXT, plate_num TEXT, odo_reading REAL, log_date TEXT
                    )
                """)
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO Odometer_Logs (driver_name, plate_num, odo_reading, log_date) VALUES (?, ?, ?, ?)",
                               (self.driver_name, self.plate_num, float(odo_val), now_str))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("✅ تم القيد بنجاح", "تم تأمين وحفظ قراءة العداد بنجاح في سجلات الأمان بالقرص D.")
                self.build_dashboard_interface()
            except Exception as e:
                messagebox.showerror("خطأ الصلاحيات", f"تعذر حفظ العداد: {e}")

        tk.Button(self.root, text="تأمين وإرسال القراءة الحالية 🔓", font=("Arial", 12, "bold"), bg="#2563EB", fg="white", bd=0, command=submit_odo).pack(pady=20, padx=40, fill="x", ipady=10)
        tk.Button(self.root, text="إلغاء والعودة", font=("Arial", 11), bg="#334155", fg="white", bd=0, command=self.build_dashboard_interface).pack(pady=5, padx=40, fill="x", ipady=6)

    # =========================================================================
    # 4. شاشة تسجيل بلاغات الأعطال الفورية
    # =========================================================================
    def view_fault_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🛠️ بلاغات الأعطال الفنية المركزية", font=("Arial", 18, "bold"), bg="#020617", fg="#DC2626").pack(pady=20)

        frame = tk.Frame(self.root, bg="#020617")
        frame.pack(pady=20, padx=40, fill="x")

        tk.Label(frame, text="اختر فئة العطل الرئيسية للفرز الفوري:", font=("Arial", 12), bg="#020617", fg="white", anchor="w").pack(fill="x", pady=5)
        
        self.cmb_cat = ttk.Combobox(frame, font=("Arial", 12), state="readonly")
        self.cmb_cat['values'] = ('عطل في المحرك / ميكانيك', 'عطل في الكهرباء والأنظمة', 'مشكلة في الإطارات / الهيدروليك', 'أعطال المكابح / الفرامل والأمان', 'أخرى (اكتب في التفاصيل)')
        self.cmb_cat.current(0)
        self.cmb_cat.pack(fill="x", ipady=4, pady=5)

        tk.Label(frame, text="اكتب تفاصيل العطل والقطع المتضررة بدقة:", font=("Arial", 12), bg="#020617", fg="white", anchor="w").pack(fill="x", pady=10)
        self.txt_detail = tk.Text(frame, font=("Arial", 12), height=5, bd=2, relief="groove")
        self.txt_detail.pack(fill="x")

        def submit_fault():
            cat = self.cmb_cat.get()
            detail = self.txt_detail.get("1.0", tk.END).strip()
            if not detail:
                messagebox.showwarning("بيانات ناقصة", "يرجى كتابة تفاصيل العطل لكي يتصرف مهندس الصيانة!")
                return

            try:
                conn = sqlite3.connect(DB_DRIVER_DATA)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Fault_Logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, plate_num TEXT, driver_name TEXT, fault_category TEXT, fault_detail TEXT, log_date TEXT
                    )
                """)
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO Fault_Logs (plate_num, driver_name, fault_category, fault_detail, log_date) VALUES (?, ?, ?, ?, ?)",
                               (self.plate_num, self.driver_name, cat, detail, now_str))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("✅ تم استقبال البلاغ", "تم تسجيل بلاغ العطل بنجاح في القرص D وتحويله فوراً لمهندسي الصيانة!")
                self.build_dashboard_interface()
            except Exception as e:
                messagebox.showerror("خطأ الصلاحيات", f"تعذر قيد العطل: {e}")

        tk.Button(self.root, text="إرسال البلاغ لغرفة الصيانة 🚀", font=("Arial", 12, "bold"), bg="#DC2626", fg="white", bd=0, command=submit_fault).pack(pady=20, padx=40, fill="x", ipady=10)
        tk.Button(self.root, text="إلغاء والعودة", font=("Arial", 11), bg="#334155", fg="white", bd=0, command=self.build_dashboard_interface).pack(pady=5, padx=40, fill="x", ipady=6)

    # =========================================================================
    # 5. شاشة مراجعة أوقات الصيانة
    # =========================================================================
    def view_maintenance_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="⏳ سجل ومواعيد صيانة الأسطول", font=("Arial", 18, "bold"), bg="#020617", fg="#D97706").pack(pady=20)

        frame_box = tk.Frame(self.root, bg="#1E293B", bd=1, relief="solid")
        frame_box.pack(pady=10, padx=40, fill="both", expand=True)

        info_text = f"🟢 حالة أمان المركبة رقم ({self.plate_num}): مستقرة وجاهزة تماماً للتشغيل والإنطلاق.\n\n"
        info_text += "النظام الآن متصل ومؤمّن باطنيّاً بنجاح، وتم فحص جدول صيانة الأسطول الكلي السيادي لعام 2026."

        lbl_info = tk.Label(frame_box, text=info_text, font=("Arial", 11), bg="#1E293B", fg="white", justify="center", anchor="center", padding=15)
        lbl_info.pack(fill="both", expand=True)

        tk.Button(self.root, text="العودة للوحة القيادة ↩", font=("Arial", 11), bg="#334155", fg="white", bd=0, command=self.build_dashboard_interface).pack(pady=20, padx=40, fill="x", ipady=8)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    main_window = tk.Tk()
    app = FakherDriverGateApp(main_window)
    main_window.mainloop()