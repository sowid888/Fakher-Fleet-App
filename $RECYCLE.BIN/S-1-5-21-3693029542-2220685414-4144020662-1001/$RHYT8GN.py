import sqlite3
from datetime import datetime

DB_PATH = "system_vault.db"

def calculate_running_depreciation(purchase_price, start_date_str, end_date_str, lifespan_years=5):
    try:
        rep_start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        rep_end = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        daily_depreciation = purchase_price / (lifespan_years * 365.25)
        days_in_period = (rep_end - rep_start).days
        return max(0.0, min(purchase_price, daily_depreciation * days_in_period))
    except Exception:
        return 0.0

def fetch_financial_metrics(vehicle_id, start_date_str, end_date_str):
    """حساب وتجميع البيانات التشغيلية بدقة حديدية"""
    try:
        start_dt = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        days = max(1, (end_dt - start_dt).days)
    except ValueError:
        return None

    # معدلات التشغيل اليومي الدقيقة (محاكاة ذكية قابلة للربط بالجداول)
    rates = {
        1: {"type": "شاحنة نقل ثقيل", "plate": "ش ح ن 999", "price": 85000.0, "fuel": 45.50, "tyres": 8.25, "oil": 4.10, "filters": 2.20, "overhaul": 12.00},
        2: {"type": "سيارة خدمات", "plate": "س ي ر 111", "price": 24000.0, "fuel": 15.00, "tyres": 2.50, "oil": 1.80, "filters": 0.90, "overhaul": 4.00}
    }
    
    v_data = rates.get(vehicle_id, rates[1])
    asset_dep = calculate_running_depreciation(v_data["price"], start_date_str, end_date_str)
    
    metrics = [
        ("🚀 استهلاك الوقود المباشر", v_data["fuel"] * days, (v_data["fuel"] * days) / days),
        ("🛞 إهلاك وتآكل الإطارات", v_data["tyres"] * days, (v_data["tyres"] * days) / days),
        ("🛢️ استهلاك وتغيير الزيوت", v_data["oil"] * days, (v_data["oil"] * days) / days),
        ("🌪️ منظومة الفلاتر والمنقيات", v_data["filters"] * days, (v_data["filters"] * days) / days),
        ("🔧 حصة العمرة الهيكلية المؤجلة", v_data["overhaul"] * days, (v_data["overhaul"] * days) / days),
        ("📉 إهلاك قيمة الأصل (الدفتري)", asset_dep, asset_dep / days),
    ]
    
    total_cost = sum(m[1] for m in metrics)
    return v_data, metrics, total_cost, days

def display_tabular_report(vehicle_id, start_date, end_date):
    result = fetch_financial_metrics(vehicle_id, start_date, end_date)
    if not result:
        print("❌ صيغة التاريخ غير صحيحة.")
        return
        
    v_data, metrics, total_cost, days = result
    
    # ─── رأس التقرير المالي ───
    print("\n" + "═"*79)
    print(f"🏰 برج التقارير المالي - كشف جنائي موزع للأصول والمصاريف التشغيلية".center(75))
    print("═"*79)
    print(f" المركبة: {v_data['type']} | اللوحة: {v_data['plate']} | القيمة الدفترية للأصل: ${v_data['price']:,.2f}")
    print(f" النطاق الزمني للبحث: من [{start_date}] إلى [{end_date}] ({days} يوماً تشغيلياً)")
    print("─"*79)
    
    # ─── رسم الجدول والأعمدة الحقيقية ───
    # تعيين مسافات الأعمدة: البيان (32 حرف)، التكلفة الإجمالية (20 حرف)، المعدل اليومي (20 حرف)
    header = f"│ {'طبيعة البند ومصدر الاستهلاك':<30} │ {'إجمالي المصروف للفترة':<18} │ {'المعدل اليومي للفترة':<18} │"
    print(header)
    print(f"├{'─'*32}┼{'─'*20}┼{'─'*20}┤")
    
    for row in metrics:
        name, total, daily = row
        print(f"│ {name:<28} │ ${total:<17,.2f} │ ${daily:<17,.2f} │")
        
    print(f"├{'─'*32}┼{'─'*20}┼{'─'*20}┤")
    print(f"│ {'💰 إجمالي الهلاك والخسائر المحققة':<27} │ ${total_cost:<17,.2f} │ ${total_cost/days:<17,.2f} │")
    print("═"*79 + "\n")

def main_hub():
    while True:
        print("🎛️ لوحة استعلام برج التقارير المالي المرئي")
        print("1. استعلام وجدولة فورية بين تاريخين محددين")
        print("2. خروج")
        choice = input("👉 اختر رقم العملية: ").strip()
        
        if choice == "1":
            try:
                v_id = int(input("🆔 أدخل رقم المركبة (1 للشاحنة، 2 للسيارة): "))
                start_str = input("🛫 من تاريخ (السنة-الشهر-اليوم مثال 2026-01-01): ").strip()
                end_str = input("🛬 إلى تاريخ (السنة-الشهر-اليوم مثال 2026-07-12): ").strip()
                display_tabular_report(v_id, start_str, end_str)
            except ValueError:
                print("❌ يرجى إدخال البيانات بصيغة صحيحة.")
        elif choice == "2":
            print("🔒 تم إغلاق البرج المالي بأمان.")
            break

if __name__ == "__main__":
    main_hub()