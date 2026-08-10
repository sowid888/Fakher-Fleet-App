import datetime

class OdometerVerificationEngine:
    def __init__(self, truck_id="2600-001", chassis_number="JAAKP34H2D7P06865", last_known_odometer=150000):
        self.truck_id = truck_id                     # رقم الشاحنة المعتمد في قائمة 2600
        self.chassis_number = chassis_number         # رقم الشاصيه (VIN)
        self.last_known_odometer = last_known_odometer # أخر قراءة مسجلة للعداد
        self.unread_notifications = 0                # عداد الشارات الحمراء 🔴

    def get_auto_timestamp(self):
        """توثيق التاريخ والوقت آلياً 100% من سيرفر النظام"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_odometer_entry(self, input_odometer, photo_attached, action_name):
        """
        الشرط الصارم: التحقق من وجود صورة العداد + منطقية القراءة 
        قبل تنفيذ أي عطل، صيانة، أو وقود
        """
        # 1. فحص وجود الصورة
        if not photo_attached:
            return {
                "success": False,
                "error_code": "MISSING_PHOTO",
                "message": "❌ عفواً! يلزم التقاط صورة للعداد أولاً لتأكيد الإجراء."
            }

        # 2. فحص منطقية القراءة (عدم إمكانية إدخال عداد أقل من السابق)
        if input_odometer < self.last_known_odometer:
            return {
                "success": False,
                "error_code": "INVALID_ODOMETER_VALUE",
                "message": f"❌ خطأ! القراءة المدخلة ({input_odometer}) أقل من السابقة ({self.last_known_odometer})."
            }

        # 3. توثيق وقبول الإجراء
        self.last_known_odometer = input_odometer
        timestamp = self.get_auto_timestamp()

        return {
            "success": True,
            "message": f"✅ تم اعتماد إجراء [{action_name}] وقراءة العداد ({input_odometer}) بنجاح.",
            "payload": {
                "truck_id": self.truck_id,
                "chassis_number": self.chassis_number,
                "odometer": self.last_known_odometer,
                "photo_status": "VERIFIED",
                "timestamp": timestamp,
                "action": action_name
            }
        }

    def set_unread_badge_count(self, count):
        """تحديث عداد الشارات الحمراء لرسائل الإدارة 🔴"""
        self.unread_notifications = count
        return f"🔴 لديك ({self.unread_notifications}) رسائل جديدة غير مقروءة."

# --- نقطة الاختبار المباشر ---
if __name__ == "__main__":
    app = OdometerVerificationEngine()
    print(app.set_unread_badge_count(3))