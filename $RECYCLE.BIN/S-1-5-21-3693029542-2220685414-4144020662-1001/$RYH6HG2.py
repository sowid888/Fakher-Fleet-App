import os
import webbrowser
from datetime import datetime

def calculate_running_depreciation(purchase_price, start_date_str, end_date_str, lifespan_years=5):
    try:
        rep_start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        rep_end = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        daily_depreciation = purchase_price / (lifespan_years * 365.25)
        days_in_period = (rep_end - rep_start).days
        return max(0.0, min(purchase_price, daily_depreciation * days_in_period))
    except:
        return 0.0

def generate_html_report(vehicle_id, start_date, end_date):
    # معدلات الحساب التشغيلية السيادية
    rates = {
        1: {"type": "شاحنة نقل ثقيل", "plate": "ش ح ن 999", "price": 85000.0, "fuel": 45.50, "tyres": 8.25, "oil": 4.10, "filters": 2.20, "overhaul": 12.00},
        2: {"type": "سيارة خدمات", "plate": "س ي ر 111", "price": 24000.0, "fuel": 15.00, "tyres": 2.50, "oil": 1.80, "filters": 0.90, "overhaul": 4.00}
    }
    
    v_data = rates.get(vehicle_id, rates[1])
    
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
        days = max(1, (end_dt - start_dt).days)
    except:
        days = 30
        start_date = "2026-06-12"
        end_date = "2026-07-12"

    asset_dep = calculate_running_depreciation(v_data["price"], start_date, end_date)
    
    # تفكيك البنود والمجاميع
    items = [
        {"name": "🚀 استهلاك الوقود المباشر", "total": v_data["fuel"] * days, "daily": v_data["fuel"]},
        {"name": "🛞 إهلاك وتآكل الإطارات الحاد", "total": v_data["tyres"] * days, "daily": v_data["tyres"]},
        {"name": "🛢️ استهلاك وتغيير الزيوت الدورية", "total": v_data["oil"] * days, "daily": v_data["oil"]},
        {"name": "🌪️ منظومة الفلاتر والمنقيات وهلاكها", "total": v_data["filters"] * days, "daily": v_data["filters"]},
        {"name": "🔧 حصة ومخصص العمرة الهيكلية المؤجلة", "total": v_data["overhaul"] * days, "daily": v_data["overhaul"]},
        {"name": "📉 إهلاك القيمة الدفترية للأصل المالي", "total": asset_dep, "daily": asset_dep / days}
    ]
    
    total_cost = sum(i["total"] for i in items)

    # بناء هيكل وتصميم المستند المالي للخلفية (HTML + CSS) للطباعة الفورية
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>كشف برج التقارير المالية والهلاك 2026</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; color: #333; background-color: #fafafa; }}
            .report-card {{ max-width: 850px; margin: 0 auto; background: white; padding: 40px; border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .header {{ text-align: center; border-bottom: 3px double #1a237e; padding-bottom: 20px; margin-bottom: 25px; }}
            .header h1 {{ color: #1a237e; margin: 0 0 10px 0; font-size: 24px; }}
            .header p {{ color: #666; margin: 5px 0; font-size: 14px; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; background: #f5f7fa; padding: 15px; border-radius: 6px; margin-bottom: 30px; border-right: 5px solid #1a237e; }}
            .info-item {{ font-size: 14px; }}
            .info-item strong {{ color: #1a237e; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px 15px; text-align: right; border-bottom: 1px solid #e0e0e0; }}
            th {{ background-color: #1a237e; color: white; font-weight: 600; font-size: 15px; }}
            tr:nth-child(even) {{ background-color: #f8f9fa; }}
            .total-row {{ background-color: #e8f5e9 !important; font-weight: bold; color: #2e7d32; font-size: 16px; }}
            .total-row td {{ border-top: 2px solid #2e7d32; border-bottom: 2px double #2e7d32; }}
            .print-btn {{ display: block; width: 200px; margin: 30px auto 0 auto; padding: 12px; background: #2e7d32; color: white; text-align: center; border: none; border-radius: 25px; font-weight: bold; cursor: pointer; font-size: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            @media print {{
                .print-btn {{ display: none; }}
                body {{ background: white; margin: 0; }}
                .report-card {{ border: none; box-shadow: none; padding: 0; }}
            }}
        </style>
    </head>
    <body>

    <div class="report-card">
        <div class="header">
            <h1>🏰 برج التقارير المالية والهلاك المالي المشدد</h1>
            <p>كشف جنائي موزع للأصول والمصاريف التشغيلية للمركبات والأساطيل</p>
        </div>

        <div class="info-grid">
            <div class="info-item"><strong>نوع المركبة المستعلمة:</strong> {v_data["type"]}</div>
            <div class="info-item"><strong>رقم لوحة التشغيل:</strong> {v_data["plate"]}</div>
            <div class="info-item"><strong>القيمة الدفترية للأصل:</strong> ${v_data["price"]:,.2f}</div>
            <div class="info-item"><strong>فترة تقرير النطاق المالي:</strong> من {start_date} إلى {end_date}</div>
            <div class="info-item"><strong>المدة التشغيلية المستخرجة:</strong> {days} يوماً تشغيلياً كاملاً</div>
            <div class="info-item"><strong>تاريخ وساعة الطباعة الفورية:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>طبيعة البند ومصدر الاستهلاك المالي للمركبة</th>
                    <th>إجمالي المصروف للفترة المحددة</th>
                    <th>المعدل اليومي الدقيق</th>
                </tr>
            </thead>
            <tbody>
    """

    for item in items:
        html_content += f"""
                <tr>
                    <td>{item["name"]}</td>
                    <td>${item["total"]:,.2f}</td>
                    <td>${item["daily"]:,.2f}</td>
                </tr>
        """

    html_content += f"""
                <tr class="total-row">
                    <td>💰 إجمالي الهلاك والخسائر التشغيلية المحققة</td>
                    <td>${total_cost:,.2f}</td>
                    <td>${total_cost/days:,.2f}</td>
                </tr>
            </tbody>
        </table>

        <button class="print-btn" onclick="window.print()">🖨️ امر طباعة المستند الفوري</button>
    </div>

    </body>
    </html>
    """

    filename = "Financial_Sovereign_Report.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    # فتح الملف تلقائياً في المتصفح الافتراضي للمستخدم فوراً وبشكل مرئي
    webbrowser.open('file://' + os.path.realpath(filename))
    print(f"✅ نجاح باهر! تم فتح مستند التقرير المحاسبي في متصفحك الافتراضي باسم {filename}")

if __name__ == "__main__":
    # استعلام تلقائي وفوري لمعاينة الجداول عند التشغيل
    generate_html_report(1, "2026-01-01", "2026-07-12")