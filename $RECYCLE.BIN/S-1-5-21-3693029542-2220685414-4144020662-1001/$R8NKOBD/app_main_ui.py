# UI Design & Screen Routing Module (واجهة المستخدم المباشرة)

class AppMainUI:
    def __init__(self, truck_id="2600-001", driver_name="سائق الميدان"):
        self.truck_id = truck_id
        self.driver_name = driver_name
        
        # إعدادات المظهر والتباين للرؤية العالية
        self.style = {
            "background_color": "#1A0000",   # خلفية كبدية/داكنة مريحة للعين
            "button_color": "#00E676",       # مفاتيح باللون الأخضر البارز
            "text_color": "#FFFFFF",         # خطوط بيضاء مكبرة
            "button_size": "LARGE"           # أزرار كبيرة جداً سهلة الضغط
        }

    def render_home_screen(self, unread_messages_count=0):
        """عرض الشاشة الرئيسية بالمفاتيح الستة الكبيرة"""
        badge_text = f" 🔴 ({unread_messages_count})" if unread_messages_count > 0 else ""
        
        menu = {
            "HEADER": f"🚛 شاحنة: {self.truck_id} | السائق: {self.driver_name}",
            "BUTTON_1": "📟 1. قراءة العداد والتنبيهات الحالية",
            "BUTTON_2": "⛽ 2. التزود بالوقود وإرفاق الإيصال",
            "BUTTON_3": "🛠️ 3. تنفيذ الصيانة وغسيل الشاحنة",
            "BUTTON_4": "⚠️ 4. بلاغات أعطال الشاحنات (ميكانيكا/كهرباء)",
            "BUTTON_5": "🚗 5. بلاغات أعطال السيارات الصغرى",
            "BUTTON_6": f"📥 6. صندوق الرسائل والتوجيهات{badge_text}"
        }
        return menu

    def on_button_click(self, button_number):
        """توجيه السائق للشاشة المناسبة عند الضغط على أي مفتاح"""
        screens = {
            1: "فتح شاشة العداد الإجباري -> (مرتبط بـ odometer_engine.py)",
            2: "فتح شاشة تعبئة الوقود -> (مرتبط بـ fuel_engine.py)",
            3: "فتح شاشة جدول الصيانة النظافة -> (مرتبط بـ faults_maintenance_engine.py)",
            4: "فتح شاشة بلاغات أعطال الشاحنات -> (مرتبط بـ faults_maintenance_engine.py)",
            5: "فتح شاشة بلاغات أعطال السيارات -> (مرتبط بـ faults_maintenance_engine.py)",
            6: "فتح صندوق الرسائل والإشعارات -> (مرتبط بـ messages_notifications_engine.py)"
        }
        return screens.get(button_number, "صفحة غير موجودة")

# --- تجربة الشاشة الرئيسية ---
if __name__ == "__main__":
    ui = AppMainUI()
    home = ui.render_home_screen(unread_messages_count=2)
    
    print("=== الواجهة الرئيسية للتطبيق ===")
    print(home["HEADER"])
    print("-" * 35)
    for key, button_name in list(home.items())[1:]:
        print(f"[{button_name}]")