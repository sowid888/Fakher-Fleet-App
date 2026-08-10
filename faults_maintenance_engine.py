import datetime

class FaultAndMaintenanceEngine:
    def __init__(self, truck_id="2600-001", chassis_number="JAAKP34H2D7P06865", current_odometer=150400):
        self.truck_id = truck_id                     # رقم المركبة قائمة 2600
        self.chassis_number = chassis_number         # رقم الشاصيه (VIN)
        self.current_odometer = current_odometer     # قراءة العداد الحالية

    def get_auto_timestamp(self):
        """توثيق التاريخ والوقت آلياً 100%"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def submit_report(self, category, selected_fault, odometer_reading, odometer_photo_ok, fault_photo_ok, custom_text="", voice_note_attached=False):
        """
        إرسال بلاغ عطل أو تنفيذ صيانة مع دعم الصوت والحقل الحر
        """
        # 1. التحقق الصارم من التقاط صورة العداد
        if not odometer_photo_ok:
            return {
                "status": "ERROR",
                "message": "❌ خطأ! يلزم تصوير العداد أولاً قبل إرسال البلاغ."
            }

        # 2. التحقق من منطقية قراءة العداد
        if odometer_reading < self.current_odometer:
            return {
                "status": "ERROR",
                "message": f"❌ خطأ! العداد المدخل ({odometer_reading}) أقل من المسجل بالسظام ({self.current_odometer})."
            }

        # 3. توثيق البيانات والتقرير
        self.current_odometer = odometer_reading
        timestamp = self.get_auto_timestamp()

        report_payload = {
            "truck_id": self.truck_id,
            "chassis_number": self.chassis_number,
            "category": category,                      # نوع البلاغ (ميكانيكا، كهرباء، صيانة...)
            "selected_issue": selected_fault,          # العطل المختار من القائمة
            "custom_note": custom_text,                # النص الحر للأعطال الأخرى
            "voice_note_status": "ATTACHED" if voice_note_attached else "NONE", # التسجيل الصوتي 🎙️
            "odometer_reading": self.current_odometer,
            "odometer_photo": "VERIFIED",
            "fault_photo": "ATTACHED" if fault_photo_ok else "NONE",
            "timestamp": timestamp
        }

        return {
            "status": "SUCCESS",
            "message": f"✅ تم إرسال بلاغ [{category} - {selected_fault}] بنجاح.",
            "data": report_payload
        }

# --- تجربة النظام التشغيلي ---
if __name__ == "__main__":
    report_app = FaultAndMaintenanceEngine(current_odometer=150400)

    # تجربة إرسال عطل غير مسجل باستخدام التسجيل الصوتي والنص الحر
    test_run = report_app.submit_report(
        category="أعطال ميكانيكية (سيارات)",
        selected_fault="أعطال أخرى ليست مذكورة",
        odometer_reading=150450,
        odometer_photo_ok=True,
        fault_photo_ok=True,
        custom_text="صوت طقطقة عند الدوران لليمين",
        voice_note_attached=True
    )

    print(test_run["message"])
    if test_run["status"] == "SUCCESS":
        print("تفاصيل التقرير المرفوع:", test_run["data"])