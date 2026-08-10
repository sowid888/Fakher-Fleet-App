import datetime

class FuelTransactionEngine:
    def __init__(self, truck_id="2600-001", chassis_number="JAAKP34H2D7P06865", previous_odometer=150000):
        self.truck_id = truck_id                     # رقم الشاحنة المعتمد قائمة 2600
        self.chassis_number = chassis_number         # رقم الشاصيه (VIN)
        self.previous_odometer = previous_odometer   # قراءة العداد السابقة
        
    def get_auto_timestamp(self):
        """توثيق آلي 100% للتاريخ والوقت من النظام"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def record_fuel_transaction(self, current_odometer, liters_added, total_cost, odometer_photo_ok, receipt_photo_ok, fuel_type="Diesel"):
        """
        تسجيل عملية الوقود وتطبيق خوارزمية الاستهلاك مع الضوابط الصارمة
        """
        # 1. فحص وجود الصور (صورة العداد + صورة الفاتورة)
        if not odometer_photo_ok or not receipt_photo_ok:
            return {
                "status": "FAILED",
                "error": "MISSING_ATTACHMENTS",
                "message": "❌ خطأ! يجب التقاط صورة العداد وصورة فاتورة الوقود لإكمال الإرسال."
            }

        # 2. فحص منطقية العداد
        if current_odometer <= self.previous_odometer:
            return {
                "status": "FAILED",
                "error": "INVALID_ODOMETER",
                "message": f"❌ خطأ! العداد الحالي ({current_odometer}) يجب أن يكون أكبر من السابق ({self.previous_odometer})."
            }

        # 3. حساب المسافة المقطوعة ومعدل الاستهلاك
        distance_traveled = current_odometer - self.previous_odometer
        
        # خوارزمية معدل الاستهلاك (لتر لكل 100 كم)
        consumption_rate = (liters_added / distance_traveled) * 100 if distance_traveled > 0 else 0

        # 4. تحديث القراءة وتجهيز البيانات
        timestamp = self.get_auto_timestamp()
        self.previous_odometer = current_odometer

        return {
            "status": "SUCCESS",
            "message": f"✅ تم تسجيل تعبئة الوقود ({liters_added} لتر) بنجاح.",
            "fuel_record": {
                "truck_id": self.truck_id,
                "chassis_number": self.chassis_number,
                "timestamp": timestamp,
                "fuel_type": fuel_type,
                "liters_added": liters_added,
                "total_cost": total_cost,
                "current_odometer": current_odometer,
                "distance_traveled_km": distance_traveled,
                "consumption_rate_l_per_100km": round(consumption_rate, 2),
                "odometer_photo": "VERIFIED",
                "receipt_photo": "VERIFIED"
            }
        }

# --- تجربة النظام التشغيلي ---
if __name__ == "__main__":
    fuel_app = FuelTransactionEngine(previous_odometer=150000)
    
    # تجربة تعبئة وقود بعد قطع مسافة 400 كم (تعبئة 120 لتر ديزل)
    result = fuel_app.record_fuel_transaction(
        current_odometer=150400,
        liters_added=120.0,
        total_cost=360.0,
        odometer_photo_ok=True,
        receipt_photo_ok=True,
        fuel_type="Diesel"
    )
    
    print(result["message"])
    if result["status"] == "SUCCESS":
        print("معدل الاستهلاك المحسوب آلياً:", result["fuel_record"]["consumption_rate_l_per_100km"], "لتر / 100 كم")