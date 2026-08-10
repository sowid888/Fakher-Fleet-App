# مجلد: app_ui_screens / login_screen.py

import json

class DriverLoginScreen:
    def __init__(self, approved_fleet_list=None):
        # قائمة المركبات المعتمدة من قائمة 2600
        self.approved_fleet = approved_fleet_list or [
            {"id": "2600-001", "type": "شاحنة", "vin": "JAAKP34H2D7P06865"},
            {"id": "2600-002", "type": "شاحنة", "vin": "JAAKP34H2D7P06866"},
            {"id": "CAR-101",   "type": "سيارة", "vin": "CARP34H2D7P01010"}
        ]

    def process_login(self, driver_name, phone_password, selected_vehicle_id):
        """
        التحقق من بيانات الدخول وتأكيد ربط السائق بالمركبة
        """
        # 1. التحقق من ملء البيانات الأساسية
        if not driver_name.strip():
            return {"success": False, "message": "❌ عفواً! يجب كتابة اسم السائق."}
            
        if not phone_password.strip() or len(phone_password) < 8:
            return {"success": False, "message": "❌ عفواً! رقم الهاتف (رمز السر) غير صحيح أو قصير جداً."}

        # 2. البحث عن المركبة المختارة في قائمة 2600
        vehicle_info = next((v for v in self.approved_fleet if v["id"] == selected_vehicle_id), None)
        
        if not vehicle_info:
            return {"success": False, "message": "❌ عفواً! المركبة المختارة غير مسجلة في القائمة المعتمدة."}

        # 3. حفظ بيانات الجلسة آلياً على هاتف السائق (Auto-Login Profile)
        session_data = {
            "driver_name": driver_name,
            "phone_password": phone_password,
            "assigned_vehicle_id": vehicle_info["id"],
            "vehicle_type": vehicle_info["type"],
            "chassis_number": vehicle_info["vin"],
            "is_logged_in": True
        }

        return {
            "success": True,
            "message": f"✅ مرحباً بك يا {driver_name}! تم ربط حسابك بـ ({vehicle_info['type']} - {vehicle_info['id']}) بنجاح.",
            "session": session_data
        }

# --- تجربة شاشة الدخول ---
if __name__ == "__main__":
    login_app = DriverLoginScreen()
    
    # تجربة تسجيل دخول جديد
    login_result = login_app.process_login(
        driver_name="محمد علي",
        phone_password="0501234567",
        selected_vehicle_id="2600-001"
    )
    
    print(login_result["message"])
    if login_result["success"]:
        print("جلسة السائق المحفوظة آلياً:", login_result["session"])