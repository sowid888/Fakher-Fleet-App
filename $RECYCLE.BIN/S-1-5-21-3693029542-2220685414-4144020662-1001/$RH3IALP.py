# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - المركز الرئيسي لإدارة الحركة وبوابة السائقين الذكية للواتساب
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
الاسم الفني المعتمد: Fakher_System_Core_2600.py
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

DB_PATH = "Fakher_System_2026.db"
HTML_FILENAME = "Fakher_Driver_2600.html"

# ⚠️ اكتب رقم هاتف الواتساب الخاص بك هنا بالصيغة الدولية بدلاً من الاكسات (مثال: 96777XXXXXXX)
MANAGER_PHONE = "967770000000" 

def init_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Driver_Central_Alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_text TEXT,
                is_done INTEGER DEFAULT 0
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM Driver_Central_Alerts WHERE is_done = 0")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Driver_Central_Alerts (alert_text, is_done) VALUES ('تذكير أمن وسلامة الشاحنات: يرجى فحص وزن الإطارات الشامل وضغط الهواء كل يومين.', 0)")
            cursor.execute("INSERT INTO Driver_Central_Alerts (alert_text, is_done) VALUES ('تنبيه الصيانة الدوري: موعد غسيل وتنظيف صندوق الشاحنة نهاية الأسبوع (يوم مهلة للموزع).', 0)")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error Database: {e}")

def generate_driver_html():
    html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 منظومة فاخر 2600 - بوابة السائق الذكية الخفيفة 📱</title>
    <style>
        body {{ font-family: 'Arial', sans-serif; background-color: #0f172a; color: #ffffff; text-align: center; padding: 12px; margin: 0; }}
        .header {{ background-color: #1e1b4b; padding: 12px; border-radius: 10px; margin-bottom: 15px; border: 2px solid #10b981; }}
        .section-title {{ color: #38bdf8; font-size: 16px; font-weight: bold; margin-top: 15px; text-align: right; border-bottom: 2px solid #334155; padding-bottom: 4px; }}
        .cat-title {{ font-size: 14px; font-weight: bold; margin: 10px 0 5px 0; text-align: right; padding-right: 5px; }}
        .mechanical-title {{ color: #f87171; }}
        .electrical-title {{ color: #facc15; }}
        .brakes-title {{ color: #60a5fa; }}
        .fridge-title {{ color: #2dd4bf; }}
        input, select, textarea {{ width: 96%; padding: 10px; margin: 6px 0; border-radius: 6px; border: 1px solid #475569; background-color: #1e293b; color: white; font-size: 15px; font-weight: bold; text-align: center; }}
        .btn {{ width: 100%; padding: 12px; color: white; border: none; border-radius: 6px; font-size: 15px; font-weight: bold; cursor: pointer; margin-top: 5px; }}
        .btn-km {{ background-color: #e11d48; }}
        .btn-fuel {{ background-color: #ca8a04; color: black; }}
        .fault-grid {{ display: grid; grid-template-columns: 1fr; gap: 6px; margin-bottom: 10px; }}
        .btn-fault {{ background-color: #1e293b; color: #f1f5f9; border: 1px solid #475569; padding: 10px; border-radius: 6px; font-size: 14px; font-weight: bold; text-align: right; cursor: pointer; width: 100%; }}
        .manager-msg-box {{ background-color: #1c1917; border: 1px dashed #ef4444; padding: 10px; border-radius: 6px; margin-top: 15px; text-align: right; }}
    </style>
</head>
<body>
    <div class="header">
        <h3 style="margin: 5px 0;">📱 بوابة سائق الشاحنة الرقمية الموحدة 2600 📱</h3>
        <p style="color: #10b981; margin: 0; font-weight: bold; font-size: 13px;">المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)</p>
    </div>

    <input type="hidden" id="manager_phone" value="{MANAGER_PHONE}">

    <div class="section-title">👤 [ 1. هوية الشاحنة والسائق الثابتة ]</div>
    <input type="text" id="driver_name" value="عبده محمد الجوزي" placeholder="اسم السائق الحركي">
    <input type="text" id="plate_num" value="ط ص 100" placeholder="رقم اللوحة المعدنية">

    <div class="section-title">📟 [ 2. قطاع قراءات العداد الحركية اليومية ]</div>
    <input type="number" id="current_km" placeholder="ادخل قراءة العداد الحالية هنا (كم / ميل)">
    <button class="btn btn-km" onclick="sendOdometer()">🚀 إرسال قراءة العداد وتلقي التذكيرات</button>

    <div class="section-title">⛽ [ 3. قطاع مراقبة وقود الديزل وحساب السندات ]</div>
    <input type="number" id="fuel_liters" placeholder="الكمية المعبأة (لتر)">
    <input type="text" id="bill_num" placeholder="رقم الفاتورة / السند المالي">
    <select id="payment_type">
        <option value="اتفاق شركة (بالآجل)">اتفاق شركة (بالآجل)</option>
        <option value="كاش (مسترد عند الوصول)">كاش (مسترد عند الوصول)</option>
    </select>
    <input type="text" id="station_name" placeholder="اسم المحطة / الموقع الحركي">
    <button class="btn btn-fuel" onclick="sendFuel()">⛽ إرسال وقود الديزل وتلقي التذكيرات</button>

    <div class="section-title">🛠️ [ 4. قائمة تسجيل أعطال الشاحنة المعتمدة ]</div>

    <div class="cat-title mechanical-title">⚙️ التصنيف: أعطال ميكانيكية</div>
    <div class="fault-grid">
        <button class="btn-fault" onclick="sendFault('لايوجد عزم', 'أعطال ميكانيكية')">⚠️ لايوجد عزم</button>
        <button class="btn-fault" onclick="sendFault('استهلاك مرتفع للديزل', 'أعطال ميكانيكية')">⚠️ استهلاك مرتفع للديزل</button>
        <button class="btn-fault" onclick="sendFault('تاخير في التشغيل', 'أعطال ميكانيكية')">⚠️ تاخير في التشغيل</button>
        <button class="btn-fault" onclick="sendFault('صوت في المحرك غريب', 'أعطال ميكانيكية')">⚠️ صوت في المحرك غريب</button>
        <button class="btn-fault" onclick="sendFault('ارتفاع حراره المحرك', 'أعطال ميكانيكية')">⚠️ ارتفاع حراره المحرك</button>
    </div>

    <div class="cat-title electrical-title">⚡ التصنيف: أعطال كهربائية</div>
    <div class="fault-grid">
        <button class="btn-fault" onclick="sendFault('البطاريات ضعيفه تمامنا', 'أعطال كهربائية')">⚡ البطاريات ضعيفه تماماً</button>
        <button class="btn-fault" onclick="sendFault('مكيف الشاحنة لا يبرد', 'أعطال كهربائية')">⚡ مكيف الشاحنة لا يبرد</button>
        <button class="btn-fault" onclick="sendFault('نور الامامي معطل', 'أعطال كهربائية')">⚡ نور الامامي معطل</button>
    </div>

    <div class="section-title">🎙️ [ بلاغ أعطال وملاحظات حرة والشكاوى ]</div>
    <textarea id="manual_fault" rows="3" placeholder="اكتب هنا أي تفاصيل أخرى أو شكاوى..."></textarea>
    <button class="btn" style="background-color: #7c3aed;" onclick="sendManualFault()">🚀 إرسال البلاغ اليدوي والشكاوى</button>

    <div class="manager-msg-box">
        <h4 style="margin: 0 0 5px 0; color: #ef4444;">🔔 إشعارات إدارة الحركة المركزية:</h4>
        <p style="margin: 0; font-size: 13px; color: #fca5a5; font-weight: bold; line-height: 1.5;">
            1. فحص وزن الإطارات الشامل وضغط الهواء كل يومين.<br>
            2. موعد غسيل وتنظيف صندوق الشاحنة نهاية الأسبوع.
        </p>
    </div>

    <script>
        function getBasicInfo() {{
            return {{
                name: document.getElementById('driver_name').value || "سائق غير مسجل",
                plate: document.getElementById('plate_num').value || "بدون لوحة",
                phone: document.getElementById('manager_phone').value
            }};
        }}
        function fireWhatsApp(phone, text) {{
            var url = "https://api.whatsapp.com/send?phone=" + phone + "&text=" + encodeURIComponent(text);
            window.open(url, '_blank');
        }}
        function sendOdometer() {{
            var info = getBasicInfo();
            var km = document.getElementById('current_km').value;
            if(!km) {{ alert('الرجاء إدخال قراءة العداد الحالية أولاً!'); return; }}
            var msg = "📟 *تقرير قراءة العداد الحركي - منظومة 2600*\\n\\n🚚 *رقم اللوحة:* " + info.plate + "\\n👤 *السائق:* " + info.name + "\\n🛣️ *العداد:* " + km + " كم/ميل";
            fireWhatsApp(info.phone, msg);
        }}
        function sendFuel() {{
            var info = getBasicInfo();
            var liters = document.getElementById('fuel_liters').value;
            var bill = document.getElementById('bill_num').value;
            if(!liters || !bill) {{ alert('الرجاء إدخال اللترات والفاتورة!'); return; }}
            var msg = "⛽ *بلاغ تعبئة ديزل - منظومة 2600*\\n\\n🚚 *اللوحة:* " + info.plate + "\\n📥 *الكمية:* " + liters + " لتر\\n🧾 *الفاتورة:* " + bill;
            fireWhatsApp(info.phone, msg);
        }}
        function sendFault(faultText, category) {{
            var info = getBasicInfo();
            var msg = "🚨 *بلاغ عطل شاحنة طارئ - منظومة 2600*\\n\\n🚚 *رقم اللوحة:* " + info.plate + "\\n👤 *السائق:* " + info.name + "\\n🛠️ *العطل:* " + faultText;
            fireWhatsApp(info.phone, msg);
        }}
        function sendManualFault() {{
            var info = getBasicInfo();
            var manualTxt = document.getElementById('manual_fault').value;
            if(!manualTxt) {{ alert('الرجاء كتابة تفاصيل الشكوى أولاً!'); return; }}
            var msg = "🚨 *بلاغ شكاوى وملاحظات حرة - منظومة 2600*\\n\\n🚚 *اللوحة:* " + info.plate + "\\n📝 *الشكوى:* " + manualTxt;
            fireWhatsApp(info.phone, msg);
            document.getElementById('manual_fault').value = "";
        }}
    </script>
</body>
</html>
"""
    with open(HTML_FILENAME, "w", encoding="utf-8") as f:
        f.write(html_content)

class FakherManagerSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("غرفة إدارة الحركة والسيطرة المركزية - منظومة فاخر 2600")
        self.root.geometry("600x350")
        self.root.configure(bg="#0f172a")
        
        tk.Label(root, text="⚙️ منظومة فاخر 2600 - السيطرة المركزية ⚙️", font=("Arial", 13, "bold"), bg="#1e1b4b", fg="#10b981", pady=10).pack(fill="x", padx=10, pady=10)
        
        init_database()
        generate_driver_html()
        
        success_frame = tk.LabelFrame(root, text=" حالة النظام ", font=("Arial", 11, "bold"), bg="#1e293b", fg="#38bdf8", labelanchor="ne")
        success_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        lbl_msg = (
            f"✅ تم تحديث النظام ورقم الهاتف بنجاح.\n\n"
            f"✅ تم إنشاء الملف السحري باسم: ({HTML_FILENAME})\n\n"
            f"⚠️ طريقة العمل الصحيحة للغد:\n"
            f"أرسل ملف الـ HTML للسائق عبر الواتساب واطلب منه أن يفتح الملف نفسه!\n"
            f"ستظهر له كافة الحقول والأعطال فورا، وعند الضغط على أي عطل سيتكفل الملف\n"
            f"بنقله إلى الواتساب وإرسال البلاغ إليك فوراً مكتوباً وجاهزاً!"
        )
        tk.Label(success_
if __name__ == "__main__":
    root = tk.Tk()
    app = FakherManagerSystem(root)
    root.mainloop()