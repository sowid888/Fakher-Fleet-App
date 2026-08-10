# مجلد: app_ui_screens / app_controller.py

import sys
import os

# إضافة المجلد الحالي للمسارات لضمان اختفاء أي تحذير برتقالي
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from login_screen import DriverLoginScreen
    from app_main_ui import AppMainUI
    from camera_odometer_ui import CameraOdometerUI
    from fault_audio_reporting_ui import FaultAndAudioReportingUI
    from messages_inbox_ui import MessagesInboxUI
except Exception:
    pass

class FleetAppController:
    def __init__(self):
        self.login_system = DriverLoginScreen()
        self.current_session = None
        self.main_ui = None
        self.camera_ui = None

    def start_app(self, driver_name, phone_pwd, vehicle_id):
        """1. تشغيل التطبيق وتسجيل الدخول"""
        login_res = self.login_system.process_login(driver_name, phone_pwd, vehicle_id)
        if login_res["success"]:
            self.current_session = login_res["session"]
            self.main_ui = AppMainUI(
                truck_id=self.current_session["assigned_vehicle_id"],
                driver_name=self.current_session["driver_name"]
            )
            self.camera_ui = CameraOdometerUI(
                truck_id=self.current_session["assigned_vehicle_id"],
                chassis_number=self.current_session["chassis_number"]
            )
            return f"✅ تم تسجيل الدخول بنجاح! مرحباً {driver_name}"
        return login_res["message"]

    def navigate_menu(self, button_number):
        """2. التنقل بين الواجهات بحسب خيارات السائق"""
        if not self.current_session:
            return "❌ يرجى تسجيل الدخول أولاً."
        
        return self.main_ui.on_button_click(button_number)

# --- تجربة الربط الشامل ---
if __name__ == "__main__":
    controller = FleetAppController()
    print(controller.start_app("محمد علي", "0501234567", "2600-001"))
    print("\n[السائق ضغط على زر الوقود]:")
    print(controller.navigate_menu(2))