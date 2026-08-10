# مجلد: app_ui_screens / fault_audio_reporting_ui.py

import datetime

class FaultAndAudioReportingUI:
    def __init__(self, truck_id="2600-001", chassis_number="JAAKP34H2D7P06865"):
        self.truck_id = truck_id
        self.chassis_number = chassis_number
        self.recorded_audio_file = None   # ملف التسجيل الصوتي المرفق
        self.attached_fault_photo = None  # صورة العطل المرفقة

    def get_fault_categories(self, vehicle_type="TRUCK"):
        """قوائم الأعطال الجاهزة بمفاتيح كبيرة"""
        if vehicle_type == "TRUCK":
            return [
                "1. أعطال المحرك والميكانيكا",
                "2. أعطال الكهرباء والإنارة",
                "3. أعطال الفرامل والمكابح",
                "4. أعطال الثلاجة والتبريد",
                "5. أعطال الإطارات والجنوط",
                "6. غسيل ونظافة صندوق الشاحنة",
                "7. عطل آخر (استخدم الصوت أو النص)"
            ]
        else: # سيارات صغرى
            return [
                "1. صيانة دورية (زيت/فلتر)",
                "2. أعطال الميكانيكا والحرارة",
                "3. أعطال الكهرباء والتكييف",
                "4. الفرامل والإطارات",
                "5. عطل آخر (استخدم الصوت أو النص)"
            ]

    def record_voice_note(self, mock_audio_path):
        """محاكاة زر تسجيل الصوت 🎙️"""
        self.recorded_audio_file = mock_audio_path
        return "🎙️ تم تسجيل الملاحظة الصوتية بنجاح واقترانها بالبلاغ."

    def submit_fault_report(self, selected_category, free_text_description="", odometer_verified=True):
        """إرسال البلاغ المكتمل للإدارة"""
        if not odometer_verified:
            return {
                "success": False,
                "message": "❌ عفواً! يجب تأكيد وتصوير قراءة العداد أولاً."
            }

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "success": True,
            "message": "🚀 تم إرسال بلاغ العطل والتسجيل الصوتي بنجاح إلى الإدارة!",
            "report_details": {
                "truck_id": self.truck_id,
                "chassis_number": self.chassis_number,
                "category": selected_category,
                "text_note": free_text_description,
                "audio_attachment": "ATTACHED" if self.recorded_audio_file else "NONE",
                "timestamp": timestamp
            }
        }

# --- تجربة الشاشة ---
if __name__ == "__main__":
    ui = FaultAndAudioReportingUI()
    print("--- 1. تسجيل صوتي للسائق ---")
    print(ui.record_voice_note("voice_note_1001.mp3"))
    
    print("\n--- 2. إرسال البلاغ ---")
    res = ui.submit_fault_report(
        selected_category="1. أعطال المحرك والميكانيكا",
        free_text_description="صوت طقطقة عند بداية التشغيل"
    )
    print(res["message"])
    print("تفاصيل البلاغ:", res["report_details"])