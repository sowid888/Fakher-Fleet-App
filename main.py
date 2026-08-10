import requests
import json

# بيانات الاتصال بـ Firebase
FIREBASE_DATABASE_URL = "https://algazi26-default-rtdb.firebaseio.com"

class FakherDriverApp:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.driver_vehicles = []
        self.selected_vehicle = None

    def fetch_driver_vehicles(self):
        """الاستعلام من السيرفر لمعرفة المركبات المخصصة لهذا الهاتف"""
        # استعلام محاكاة لاسترجاع بيانات السائق من قاعدة البيانات
        # في حال وجود مركبتين مرابطتين بنفس الرقم:
        if self.phone_number == "0501234567":  # مثال لسائق يملك مركبتين
            self.driver_vehicles = [
                {"code": "Truck_101", "name": "🚚 إيسوزو عادي", "plate": "أ ب ج 123"},
                {"code": "Truck_102", "name": "🚛 إيسوزو تيربو", "plate": "د هـ و 456"}
            ]
        else:
            self.driver_vehicles = [
                {"code": "Truck_201", "name": "🚚 شاحنة مرسيدس", "plate": "س ص ع 789"}
            ]
        return self.driver_vehicles

    def display_ui_doors(self):
        """تحديد شكل الواجهة بناءً على عدد المركبات"""
        vehicles = self.fetch_driver_vehicles()
        
        if len(vehicles) > 1:
            print("\n==========================================")
            print("🛑 مرحباً بك! تم العثور على أكثر من مركبة مسجلة برقمك:")
            print("يرجى اختيار الباب/المفتاح الخاص بالمركبة الحالية:")
            for idx, v in enumerate(vehicles, 1):
                print(f"  [{idx}] {v['name']} (لوحة: {v['plate']})")
            print("==========================================")
        else:
            print(f"\n✅ مرحباً بك! مركبتك المسجلة: {vehicles[0]['name']}")
            self.selected_vehicle = vehicles[0]

    def select_vehicle_door(self, choice_index):
        """اختيار الباب (المفتاح) من قبل السائق"""
        if 0 <= choice_index < len(self.driver_vehicles):
            self.selected_vehicle = self.driver_vehicles[choice_index]
            print(f"\n👉 تم اختيار: {self.selected_vehicle['name']}")

    def send_report_with_confirmation(self, odometer_reading, report_text):
        """شاشة التأكيد المنبثقة قبل رفع البلاغ لسيرفر Firebase"""
        if not self.selected_vehicle:
            print("❌ خطأ: لم يتم تحديد المركبة!")
            return

        print("\n------------------------------------------")
        print("⚠️ [شاشة تأكيد إرسال البلاغ المنبثقة]")
        print(f"• هل أنت متأكد من إرسال البلاغ لـ: {self.selected_vehicle['name']}؟")
        print(f"• رقم اللوحة: {self.selected_vehicle['plate']}")
        print(f"• قراءة العداد: {odometer_reading} كم")
        print(f"• تفاصيل البلاغ: {report_text}")
        print("------------------------------------------")
        
        confirm = input("هل تؤكد الإرسال؟ (اكتب 'نعم' للتأكيد / 'لا' للتعديل): ").strip()

        if confirm.lower() in ['نعم', 'yes', 'y']:
            payload = {
                "driver_phone": self.phone_number,
                "vehicle_code": self.selected_vehicle['code'],
                "vehicle_name": self.selected_vehicle['name'],
                "plate_number": self.selected_vehicle['plate'],
                "odometer_reading": odometer_reading,
                "report_text": report_text,
                "status": "pending"
            }
            
            # رفع البيانات إلى Firebase Realtime Database
            response = requests.post(f"{FIREBASE_DATABASE_URL}/Reports.json", json=payload)
            if response.status_code == 200:
                print("✅ تم إرسال البلاغ بنجاح إلى سيرفر Firebase!")
            else:
                print("🛑 حدث خطأ في الاتصال بالسيرفر.")
        else:
            print("🔄 تم إلغاء الإرسال، يمكنك إعادة اختيار المركبة.")

# --- تجربة النظام ---
if __name__ == "__main__":
    # تشغيل تجريبي برقم هاتف لديه شاحنتين (إيسوزو عادي / إيسوزو تيربو)
    app = FakherDriverApp(phone_number="0501234567")
    app.display_ui_doors()
    
    # السائق يختار المفتاح الثاني (إيسوزو تيربو)
    app.select_vehicle_door(1)
    
    # إدخال البلاغ وشاشة التأكيد
    app.send_report_with_confirmation(odometer_reading=85400, report_text="طلب تغيير زيت محرك")