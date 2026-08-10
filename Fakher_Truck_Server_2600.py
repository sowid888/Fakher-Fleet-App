l# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - سيرفر الاستقبال الخلفي
الاسم الفني المعتمد: Fakher_Truck_Server_2600.py
"""

import sqlite3
from datetime import datetime
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)
DB_PATH = "Fakher_System_2026.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Truck_Fault_Logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_num TEXT,
            driver_name TEXT,
            fault_category TEXT,
            fault_detail TEXT,
            log_date TEXT
        )
    """)
    conn.commit()
    conn.close()

TRUCK_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة سائق الشاحنة 2600</title>
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #0f172a; color: #ffffff; text-align: center; padding: 15px; }
        .header { background-color: #1e1b4b; padding: 12px; border-radius: 10px; border: 2px solid #10b981; }
        .section-title { color: #38bdf8; font-size: 16px; font-weight: bold; margin-top: 15px; text-align: right; }
        .btn-fault { background-color: #1e293b; color: #f1f5f9; border: 1px solid #475569; padding: 12px; border-radius: 6px; width: 100%; text-align: right; margin-bottom: 5px; font-weight: bold;}
    </style>
</head>
<body>
    <div class="header">
        <h3>🚚 بوابة سائق الشاحنة الرقمية 2600 🚚</h3>
        <p style="color: #10b981; margin: 0;">المشرف الفني العام: المهندس جمال سويد</p>
    </div>
    <div class="section-title">👤 [ هوية الشاحنة والسائق ]</div>
    <input type="text" id="driver_name" value="عبده محمد الجوزي" style="width:100%; padding:10px; margin:5px 0; background:#1e293b; color:white; text-align:center;">
    <input type="text" id="plate_num" value="ط ص 100" style="width:100%; padding:10px; margin:5px 0; background:#1e293b; color:white; text-align:center;">
    
    <div class="section-title">🛠️ [ اضغط لإرسال العطل فوراً ]</div>
    <button class="btn-fault" onclick="sendFault('أعطال ميكانيكية', 'لايوجد عزم')">⚠️ لايوجد عزم</button>
    <button class="btn-fault" onclick="sendFault('أعطال ميكانيكية', 'ارتفاع حراره المحرك')">⚠️ ارتفاع حراره المحرك</button>
    <button class="btn-fault" onclick="sendFault('أعطال كهربائية', 'مكيف الشاحنة لا يبرد')">⚡ مكيف الشاحنة لا يبرد</button>
    
    <script>
        function sendFault(category, detail) {
            fetch('/api/truck/fault', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    driver_name: document.getElementById('driver_name').value,
                    plate_num: document.getElementById('plate_num').value,
                    fault_category: category,
                    fault_detail: detail
                })
            }).then(res => res.json()).then(data => { if(data.success) alert("✅ تم إرسال البلاغ لبرنامج المهندس جمال بنجاح!"); });
        }
    </script>
</body>
</html>"""

@app.route('/truck')
def truck_gateway():
    return render_template_string(TRUCK_HTML_TEMPLATE)

@app.route('/api/truck/fault', methods=['POST'])
def save_fault():
    data = request.json
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Truck_Fault_Logs (plate_num, driver_name, fault_category, fault_detail, log_date) VALUES (?, ?, ?, ?, ?)",
                       (data['plate_num'], data['driver_name'], data['fault_category'], data['fault_detail'], datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)