from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# اسم الملف الذي ستُحفظ فيه بيانات هويات الشاحنات
DATA_FILE = "trucks_identity.json"

@app.route('/add_truck', methods=['POST'])
def add_truck():
    try:
        # استقبال البيانات القادمة من تطبيق App Inventor
        data = request.form
        
        # استخراج الحقول المرسلة من التطبيق
        truck_data = {
            "driver_name": data.get("driver_name"),
            "plate_number": data.get("plate_number"),
            "admin_number": data.get("admin_number"),
            "password": data.get("password")
        }
        
        # التأكد من أن البيانات ليست فارغة
        if not truck_data["admin_number"] or not truck_data["plate_number"]:
            return "Error: Missing Data", 400

        # قراءة البيانات القديمة المخزنة إن وجدت
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                all_trucks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_trucks = []

        # إضافة الشاحنة الجديدة إلى القائمة
        all_trucks.append(truck_data)

        # حفظ القائمة المحدثة في ملف JSON
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(all_trucks, f, ensure_ascii=False, indent=4)

        print(f" Successfully registered truck: {truck_data['admin_number']}")
        return "Success", 200

    except Exception as e:
        print(f"Error: {e}")
        return "Server Error", 500

if __name__ == '__main__':
    # تشغيل السيرفر على الشبكة المحلية ليتصل به الهاتف
    # المنفذ الافتراضي هو 5000
    app.run(host='0.0.0.0', port=5000, debug=True)