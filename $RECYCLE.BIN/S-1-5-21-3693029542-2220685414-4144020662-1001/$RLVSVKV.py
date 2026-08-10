import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# تحسين الخطوط لعرض اللغة العربية بشكل سليم في الرسم البياني والتقرير
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'

def calculate_running_depreciation(purchase_price, start_date_str, end_date_str, lifespan_years=5):
    try:
        rep_start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        rep_end = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        daily_depreciation = purchase_price / (lifespan_years * 365.25)
        days_in_period = (rep_end - rep_start).days
        return max(0.0, min(purchase_price, daily_depreciation * days_in_period))
    except:
        return 0.0

def generate_pdf_report(vehicle_id, start_date, end_date):
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
        days = max(1, (end_dt - start_dt).days)
    except ValueError:
        messagebox.showerror("خطأ", "صيغة التاريخ غير صحيحة! استخدم YYYY-MM-DD")
        return

    # معدلات الحساب السيادية
    rates = {
        1: {"type": "شاحنة نقل ثقيل", "plate": "ش ح ن 999", "price": 85000.0, "fuel": 45.50, "tyres": 8.25, "oil": 4.10, "filters": 2.20, "overhaul": 12.00},
        2: {"type": "سيارة خدمات", "plate": "س ي ر 111", "price": 24000.0, "fuel": 15.00, "tyres": 2.50, "oil": 1.80, "filters": 0.90, "overhaul": 4.00}
    }
    
    v_data = rates.get(vehicle_id, rates[1])
    asset_dep = calculate_running_depreciation(v_data["price"], start_date, end_date)
    
    # تفكيك البنود والمجاميع
    labels = ['الوقود المباشر', 'الإطارات', 'الزيوت', 'الفلاتر', 'العمرة الهيكلية', 'إهلاك الأصل الدفتري']
    values = [
        v_data["fuel"] * days,
        v_data["tyres"] * days,
        v_data["oil"] * days,
        v_data["filters"] * days,
        v_data["overhaul"] * days,
        asset_dep
    ]
    total_cost = sum(values)

    # 🏗️ إنشاء خلفية صفحة التقرير الرسمية (A4 بمقاسات إنش)
    fig, (ax_table, ax_pie) = plt.subplots(2, 1, figsize=(8.5, 11), gridspec_kw={'height_ratios': [1.2, 1]})
    fig.patch.set_facecolor('#ffffff')
    
    # ─── الترويسة العلوية للتقرير ───
    fig.suptitle(f"🏰 كشف استقصائي موزع للأصول والمصاريف التشغيلية\n🏰 برج التقارير المالية والهلاك المالي 2026", 
                 fontsize=16, fontweight='bold', color='#1a237e', y=0.96)
    
    # نص معلومات المركبة والفترة
    info_text = (
        f"نوع المركبة: {v_data['type']}   |   رقم اللوحة: {v_data['plate']}   |   قيمة الشراء: ${v_data['price']:,.2f}\n"
        f"الفترة المستعلمة: من {start_date} إلى {end_date} ({days} يوماً تشغيلياً)\n"
        f"تاريخ استخراج التقرير الفوري: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    fig.text(0.5, 0.88, info_text, ha='center', fontsize=11, color='#37474f', bbox=dict(boxstyle='round,pad=0.5', facecolor='#f5f5f5', edgecolor='#cfd8dc'))

    # ─── بناء الجدول المحاسبي ───
    ax_table.axis('off')
    table_data = [["طبيعة البند ومصدر الاستهلاك", "إجمالي المصروف للفترة", "المعدل اليومي"]]
    for l, v in zip(labels, values):
        table_data.append([l, f"${v:,.2f}", f"${v/days:,.2f}"])
    table_data.append(["إجمالي الهلاك والخسائر", f"${total_cost:,.2f}", f"${total_cost/days:,.2f}"])
    
    # رسم الجدول وتنسيقه كأنظمة الطباعة العالمية
    tab = ax_table.table(cellText=table_data, loc='center', cellLoc='center')
    tab.auto_set_font_size(False)
    tab.set_fontsize(11)
    tab.scale(1, 2)
    
    # تلوين خلايا الجدول
    for i in range(len(table_data)):
        for j in range(3):
            cell = tab[(i, j)]
            if i == 0:
                cell.set_facecolor('#1a237e')
                cell.get_text().set_color('white')
                cell.get_text().set_weight('bold')
            elif i == len(table_data) - 1:
                cell.set_facecolor('#e8f5e9')
                cell.get_text().set_weight('bold')
                cell.get_text().set_color('#2e7d32')
            else:
                cell.set_facecolor('#ffffff' if i % 2 == 0 else '#f8f9fa')

    # ─── رسم الدائرة البيانية لتوزيع النسب ───
    ax_pie.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, 
               colors=['#29b6f6', '#ab47bc', '#ffee58', '#26a69a', '#ffa726', '#ef5350'],
               textprops={'fontsize': 10})
    ax_pie.set_title("📊 التوزيع المئوي الجنائي لمصادر الخسائر والإهلاك المالي", fontsize=12, fontweight='bold', color='#1a237e', pad=20)

    # 💾 حفظ المستند كملف PDF جاهز للطباعة فوراً
    pdf_filename = f"Financial_Report_{v_data['plate']}_{start_date}.pdf"
    plt.tight_layout(rect=[0, 0.03, 1, 0.86])
    
    # عرض النافذة للمعاينة والطباعة الفورية
    plt.show()
    
    # حفظ نسخة صامتة في المجلد للطباعة
    fig.savefig(pdf_filename, dpi=300, bbox_inches='tight')
    messagebox.showinfo("نجاح العملية", f"✅ تم توليد تقرير الخلفية المتكامل بنجاح!\nتم حفظ ملف PDF للطباعة المباشرة باسم:\n{pdf_filename}")

# ─── واجهة البرنامج الرسومية للتحكم المستقل ───
def start_interface():
    root = tk.Tk()
    root.title("🏰 بوابة التقارير المالية والطباعة السيادية")
    root.geometry("450x320")
    root.configure(bg='#eceff1')
    
    tk.Label(root, text="🏰 نظام استخراج التقارير المطبوعة المباشرة", font=("Segoe UI", 13, "bold"), bg='#1a237e', fg='white', pady=10).pack(fill='x')
    
    frame = tk.Frame(root, bg='#eceff1', pady=15)
    frame.pack()
    
    tk.Label(frame, text="رقم المركبة (1 للشاحنة، 2 للسيارة):", bg='#eceff1', font=("Segoe UI", 10)).grid(row=0, column=0, sticky='w', pady=5)
    entry_id = tk.Entry(frame, font=("Segoe UI", 10))
    entry_id.insert(0, "1")
    entry_id.grid(row=0, column=1, pady=5)
    
    tk.Label(frame, text="🛫 من تاريخ (YYYY-MM-DD):", bg='#eceff1', font=("Segoe UI", 10)).grid(row=1, column=0, sticky='w', pady=5)
    entry_start = tk.Entry(frame, font=("Segoe UI", 10))
    entry_start.insert(0, "2026-01-01")
    entry_start.grid(row=1, column=1, pady=5)
    
    tk.Label(frame, text="🛬 إلى تاريخ (YYYY-MM-DD):", bg='#eceff1', font=("Segoe UI", 10)).grid(row=2, column=0, sticky='w', pady=5)
    entry_end = tk.Entry(frame, font=("Segoe UI", 10))
    entry_end.insert(0, "2026-07-12")
    entry_end.grid(row=2, column=1, pady=5)
    
    btn = tk.Button(root, text="🖨️ عرض خلفية التقرير والطباعة الفورية", font=("Segoe UI", 11, "bold"), bg='#2e7d32', fg='white', padx=10, pady=5,
                    command=lambda: generate_pdf_report(int(entry_id.get()), entry_start.get(), entry_end.get()))
    btn.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    start_interface()