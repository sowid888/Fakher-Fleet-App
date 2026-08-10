import datetime

class MessagesAndNotificationEngine:
    def __init__(self, truck_id="2600-001", chassis_number="JAAKP34H2D7P06865"):
        self.truck_id = truck_id                     # رقم الشاحنة المعتمد قائمة 2600
        self.chassis_number = chassis_number         # رقم الشاصيه (VIN)
        self.inbox = []                              # قائمة الرسائل الواردة
        self.unread_badge_count = 0                  # عداد الشارة الحمراء 🔴

    def get_auto_timestamp(self):
        """توثيق آلي 100% للتاريخ والوقت من سيرفر النظام"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def receive_admin_message(self, message_id, content, is_urgent=False):
        """استقبال توجيه جديد من الإدارة وتحديث الشارة الحمراء فوراً"""
        new_msg = {
            "message_id": message_id,
            "content": content,
            "is_urgent": is_urgent,
            "status": "UNREAD",                       # غير مقروءة
            "received_at": self.get_auto_timestamp(),
            "read_at": None
        }
        self.inbox.append(new_msg)
        self.unread_badge_count += 1
        return f"🔴 إشعار جديد! لديك ({self.unread_badge_count}) رسائل غير مقروءة."

    def mark_message_as_read(self, message_id):
        """تثبيت قراءة الرسالة وتخفيض العداد آلياً وتأكيد القراءة للسيرفر"""
        for msg in self.inbox:
            if msg["message_id"] == message_id and msg["status"] == "UNREAD":
                msg["status"] = "READ"
                msg["read_at"] = self.get_auto_timestamp()
                self.unread_badge_count = max(0, self.unread_badge_count - 1)
                return {
                    "status": "SUCCESS",
                    "message": f"✅ تمت قراءة الرسالة وتوثيق الوقت آلياً ({msg['read_at']}).",
                    "remaining_unread_badges": self.unread_badge_count
                }
        return {"status": "NOT_FOUND", "message": "الرسالة غير موجودة أو قُرئت سابقاً."}

    def send_driver_reply(self, message_id, reply_text, current_odometer, voice_note_attached=False):
        """إرسال رد السائق للإدارة مع توثيق العداد والتسجيل الصوتي"""
        timestamp = self.get_auto_timestamp()
        reply_payload = {
            "truck_id": self.truck_id,
            "chassis_number": self.chassis_number,
            "reply_to_msg_id": message_id,
            "reply_text": reply_text,
            "voice_note": "ATTACHED" if voice_note_attached else "NONE",
            "odometer_at_reply": current_odometer,
            "timestamp": timestamp
        }
        return {
            "status": "SUCCESS",
            "message": "📤 تم إرسال الرد إلى الإدارة بنجاح.",
            "data": reply_payload
        }

# --- تجربة النظام التشغيلي ---
if __name__ == "__main__":
    msg_engine = MessagesAndNotificationEngine()

    print("--- 1. إرسال توجيهين من الإدارة ---")
    msg_engine.receive_admin_message("MSG_101", "يرجى التوجه لموقع التوزيع الجديد بالحي المالي.")
    badge_info = msg_engine.receive_admin_message("MSG_102", "تنبيه: موعد غسيل ونظافة صندوق الشاحنة غداً.", is_urgent=True)
    print(badge_info) # يظهر العداد: 2 🔴

    print("\n--- 2. السائق يفتح الرسالة الأولى ويقرأها ---")
    read_result = msg_engine.mark_message_as_read("MSG_101")
    print(read_result["message"])
    print("الشارات الحمراء المتبقية 🔴:", read_result["remaining_unread_badges"]) # ينخفض لـ 1 🔴

    print("\n--- 3. السائق يرسل رداً صوتاً ونشاً للإدارة ---")
    reply_res = msg_engine.send_driver_reply(
        message_id="MSG_102",
        reply_text="تم الاستلام وجاري التنفيذ فور الوصول.",
        current_odometer=150500,
        voice_note_attached=True
    )
    print(reply_res["message"])