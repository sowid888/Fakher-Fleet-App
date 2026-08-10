# مجلد: app_ui_screens / camera_odometer_ui.py

import datetime

class CameraOdometerUI:
    def __init__(self, truck_id="2600-001", chassis_number="JAAKP34H2D7P06865"):
        self.truck_id = truck_id
        self.chassis_number = chassis_number
        
        # حالة المرفقات الحالية في الشاشة
        self.captured_odometer_photo = None
        self.captured_receipt_photo = None

    def render_camera_screen(self, action_title="تأكيد الإجراء"):
        """عرض واجهة الكاميرا مع الأزرار الضخمة"""
        return {
            "TITLE": f"📸 {action_title} - الشاحنة ({self.truck_id})",
            "ODOMETER_INPUT": "🔢 أدخل قراءة العداد الحالية (كم / ميل):",
            "BTN_CAPTURE_ODOMETER": "📷 [ 1. اضغط هنا لالتقاط صورة العداد ]",
            "BTN_CAPTURE_RECEIPT": "🧾 [ 2. اضغط هنا لالتقاط صورة الفاتورة (إن وجدت) ]",
            "BTN_SUBMIT": "🟢 [ 3. إرسال وتأكيد الإجراء ]"
        }

    def process_capture(self, photo_type, image_data_mock):
        """محاكاة التقاط الصورة من كاميرا الجوال"""
        if photo_type == "ODOMETER":
            self.captured_odometer_photo = image_data_mock
            return "✅ تم التقاط صورة العداد بنجاح وربطها بالتاريخ والوقت."
        elif photo_type == "RECEIPT":
            self.captured_receipt_photo = image_data_mock
            return "✅ تم التقاط صورة الفاتورة بنجاح."

    def validate_and_submit(self, input_odometer_val, require_receipt=False):
        """
        زر التأكيد الصارم: يمنع الإرسال بدون التقاط صورة العداد
        """
        # 1. الشرط الإجباري: صورة العداد
        if not self.captured_odometer_photo:
            return {
                "success": False,
                "message": "❌ عفواً! لا يمكنك الإرسال بدون التقاط صورة العداد أولاً 📸."
            }

        # 2. الشرط الإجباري للفواتير (في حالة الوقود)
        if require_receipt and not self.captured_receipt_photo:
            return {
                "success": False,
                "message": "❌ عفواً! يلزم تصوير فاتورة/إيصال التعبئة لإكمال الإرسال 🧾."
            }

        # 3. نجاح العملية وتجهيز الحزمة للسيرفر
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "success": True,
            "message": "🚀 تم توثيق وإرسال البيانات والصور بنجاح إلى فايربيس!",
            "data_package": {
                "truck_id": self.truck_id,
                "chassis_number": self.chassis_number,
                "odometer_value": input_odometer_val,
                "odometer_photo_status": "ATTACHED",
                "receipt_photo_status": "ATTACHED" if require_receipt else "NOT_REQUIRED",
                "timestamp": timestamp
            }
        }

# --- تجربة الشاشة ---
if __name__ == "__main__":
    cam_ui = CameraOdometerUI()
    
    print("--- 1. محاولة الإرسال بدون تصوير ---")
    res1 = cam_ui.validate_and_submit(150600)
    print(res1["message"])
    
    print("\n--- 2. التقاط صورة العداد ثم إعادة الإرسال ---")
    cam_ui.process_capture("ODOMETER", "data:image/jpeg;base64_mock_data...")
    res2 = cam_ui.validate_and_submit(150600)
    print(res2["message"])