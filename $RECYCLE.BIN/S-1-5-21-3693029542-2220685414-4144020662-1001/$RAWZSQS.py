import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import webbrowser

DB_PATH = "system_vault.db"

def fetch_filtered_vehicles(search_query=""):
    """
    سحب الشاحنات الحقيقية فقط من الخزنة بناءً على فلتر البحث.
    لا توجد هنا أي بيانات افتراضية أو أسماء مصطنعة!
    """
    vehicles_list = []
    if not os.path.exists(DB_PATH):
        return vehicles_list

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # استعلام مرن للبحث في جدول الشاحنات (تأكد من مطابقة اسم الجدول fleet_cars أو تعديله بناءً على نتيجة كود الفحص)
        # سنبحث برقم الشاحنة، اسم السائق، أو الرقم الإداري
        sql = """
            SELECT car_id, plate_number, driver_name, admin_number, purchase_price 
            FROM fleet_cars
            WHERE plate_number LIKE ? OR driver_name LIKE ? OR admin_number LIKE ?
        """
        q = f"%{search_query}%"
        cursor.execute(sql, (q, q, q))
        rows = cursor.fetchall()
        
        for row in rows:
            vehicles_list.append({
                "id": row[0],
                "plate": row[1],
                "driver": row[2],
                "admin_no": row[3],
                "price": float(row[4]) if row[5] else 0.0
            })
            
        conn.close()
    except sqlite3.Error as e:
        print(f"خطأ أثناء القراءة الحقيقية من الخزنة: {e}")
        
    return vehicles_list

def get_financial_summary(vehicle_id, start_date, end_date):
    """حساب الخسائر والمبالغ المصروفة الفردية الحقيقية من جداول الحسابات"""
    fuel = 0.0
    maintenance = 0.0
    
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # حساب وقود الشاحنة الحقيقي للفترة
            cursor.execute("SELECT SUM(amount) FROM fuel_logs WHERE car_id = ? AND log_date BETWEEN ? AND ?", (vehicle_id, start_date, end_date))
            res_fuel = cursor.fetchone()[0]
            fuel = float(res_fuel) if res_fuel else 0.0
            
            # حساب صيانات الشاحنة الحقيقية للفترة
            cursor.execute("SELECT SUM(cost) FROM maintenance_logs WHERE car_id = ? AND maintenance_date BETWEEN ? AND ?", (vehicle_id, start_date, end_date))
            res_maint = cursor.fetchone()[0]
            maintenance = float(res_maint) if res_maint else 0.0
            
            conn.close()
        except sqlite3.Error:
            pass
            
    return fuel, maintenance

# ==========================================
# 📊 محرك توليد التقرير بناءً على الاختيار الحقيقي
# ==========================================
def generate_real_report(selected_item, start_date, end_date):
    if not selected_item:
        messagebox.showwarning("تنبيه", "الرجاء تحديد مركبة من الجدول أولاً!")
        return
        
    # استخراج البيانات الحقيقية للمركبة المحددة من الجدول
    v_id = selected_item['values'][0]
    plate = selected_item['values'][1]
    driver = selected_item['values'][2]
    admin_no = selected_item['values'][3]
    
    # حساب المدة
    try:
        days = (datetime.strptime(end_date, "%Y-%m-%d").date() - datetime.strptime(start_date, "%Y-%m-%d").date()).days
        if days <= 0: days = 1
    except:
        days = 1
        
    fuel, maint = get_financial_summary(v_id, start_date, end_date)
    total = fuel + maint # إجمالي المبالغ المصروفة فعلياً

    # بناء كشف الحساب الحقيقي كاملاً بدون أي فرضيات
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تقرير مالي حقيقي للمركبة</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fafafa; margin: 30px; }}
            .report-box {{ max-width: 850px; margin: auto; background: #fff; padding: 30px; border: 1px solid #ccc; border-top: 10px solid #1a237e; }}
            .title {{ text-align: center; color: #1a237e; font-size: 24px; margin-bottom: 20px; }}
            .meta-table, .data-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            .meta-table td {{ padding: 8px; border: 1px solid #eee; }}
            .meta-table td.heading {{ background: #f5f5f5; font-weight: bold; width: 20%; }}
            .data-table th {{ background: #1a237e; color: white; padding: 10px; text-align: right; }}
            .data-table td {{ padding: 12px; border-bottom: 1px solid #eee; }}
            .total {{ font-weight: bold; background: #e8eaf6; color: #1a237e; }}
        </style>
    </head>
    <body>
        <div class="report-box">
            <div class="title">📋 تقرير النفقات والخسائر الفعلي للمركبة</div>
            
            <table class="meta-table">
                <tr>
                    <td class="heading">الرقم الإداري</td><td>{admin_no}</td>
                    <td class="heading">رقم لوحة الشاحنة</td><td>{plate}</td>
                </tr>
                <tr>
                    <td class="heading">اسم السائق الحالي</td><td>{driver}</td>
                    <td class="heading">الفترة الزمنية للتقرير</td><td>من {start_date} إلى {end_date} ({days} يوم)</td>
                </tr>
            </table>

            <table class="data-table">
                <thead>
                    <tr>
                        <th>بيان بند الصرف الفعلي (من واقع الخزنة المركزية)</th>
                        <th>المبالغ المسجلة والمصروفة</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>⛽ محروقات ووقود حقيقي مسجل</td><td>{fuel:,.2f} ريال/دولار</td></tr>
                    <tr><td>🛠️ فواتير صيانة وإصلاحات وقطع غيار حقيقية</td><td>{maint:,.2f} ريال/دولار</td></tr>
                    <tr class="total">
                        <td>💰 إجمالي الخسائر والمبالغ المصروفة على المركبة</td>
                        <td>{total:,.2f} ريال/دولار</td>
                    </tr>
                </tbody>
            </table>
            <br>
            <center><button onclick="window.print()" style="padding: 10px 20px; font-weight:bold; cursor:pointer;">🖨️ طباعة أو حفظ التقرير الحقيقي</button></center>
        </div>
    </body>
    </html>
    """
    
    with open("Real_Vault_Report.html", "w", encoding="utf-8") as f:
        f.write(html)
    webbrowser.open('file://' + os.path.realpath("Real_Vault_Report.html"))

# ==========================================
# 🎛️ بناء لوحة التحكم وحقول الاستعلام والبحث
# ==========================================
def run_real_system():
    root = tk.Tk()
    root.title("🏰 نظام الاستعلام الفعلي عن أسطول المركبات")
    root.geometry("750x550")
    root.configure(bg="#f5f5f5")
    
    # عنوان البرنامج
    tk.Label(root, text="🏰 محرك التقارير الحقيقية للمركبات والشاحنات", font=("Segoe UI", 14, "bold"), bg="#1a237e", fg="white", pady=10).pack(fill="x")
    
    top_frame = tk.Frame(root, bg="#f5f5f5", padx=15, pady=10)
    top_frame.pack(fill="x")
    
    # 🔍 حقل البحث الحر
    tk.Label(top_frame, text="🔍 ابحث هنا بـ (اسم السائق / رقم الشاحنة / الرقم الإداري):", font=("Segoe UI", 10, "bold"), bg="#f5f5f5").pack(anchor="w")
    search_entry = tk.Entry(top_frame, font=("Segoe UI", 11))
    search_entry.pack(fill="x", pady=5)
    
    # جدول عرض البيانات الحقيقية القادم من الخزنة
    tree_frame = tk.Frame(root, padx=15)
    tree_frame.pack(fill="both", expand=True)
    
    columns = ("id", "plate", "driver", "admin_no")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
    tree.heading("id", text="معرف الخزنة")
    tree.heading("plate", text="رقم الشاحنة / السيارة")
    tree.heading("driver", text="اسم السائق")
    tree.heading("admin_no", text="الرقم الإداري")
    
    tree.column("id", width=80, anchor="center")
    tree.column("plate", width=150, anchor="center")
    tree.column("driver", width=200, anchor="center")
    tree.column("admin_no", width=120, anchor="center")
    tree.pack(fill="both", expand=True)
    
    # دالة تحديث الجدول بناءً على البيانات الحقيقية المخزنة فقط
    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)
        query = search_entry.get()
        data = fetch_filtered_vehicles(query)
        for v in data:
            tree.insert("", "end", values=(v["id"], v["plate"], v["driver"], v["admin_no"]))
            
    search_entry.bind("<KeyRelease>", lambda e: refresh_table())
    
    # قسم التواريخ والفترة الزمنية
    date_frame = tk.Frame(root, bg="#f5f5f5", padx=15, pady=10)
    date_frame.pack(fill="x")
    
    tk.Label(date_frame, text="🛫 من تاريخ (YYYY-MM-DD):", bg="#f5f5f5").grid(row=0, column=0, padx=5, sticky="w")
    ent_start = tk.Entry(date_frame, font=("Segoe UI", 10), width=15)
    ent_start.insert(0, "2026-01-01")
    ent_start.grid(row=0, column=1, padx=5)
    
    tk.Label(date_frame, text="🛬 إلى تاريخ (YYYY-MM-DD):", bg="#f5f5f5").grid(row=0, column=2, padx=5, sticky="w")
    ent_end = tk.Entry(date_frame, font=("Segoe UI", 10), width=15)
    ent_end.insert(0, "2026-07-12")
    ent_end.grid(row=0, column=3, padx=5)
    
    # 🚀 زر استخراج التقرير الحقيقي للمركبة المحددة
    def on_submit():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "الرجاء الضغط على المركبة المطلوبة من الجدول أولاً!")
            return
        item = tree.item(selected[0])
        generate_real_report(item, ent_start.get(), ent_end.get())

    btn_action = tk.Button(root, text="📊 توليد التقرير المالي والوقود الحقيقي للمركبة المحددة", font=("Segoe UI", 12, "bold"), bg="#1a237e", fg="white", pady=10, command=on_submit)
    btn_action.pack(fill="x", padx=15, pady=15)
    
    # تشغيل الجدول وتعبئته عند فتح البرنامج
    refresh_table()
    root.mainloop()

if __name__ == "__main__":
    run_real_system()