# مجلد: app_ui_screens / messages_inbox_ui.py

import datetime

class MessagesInboxUI:
    def __init__(self, truck_id="2600-001", chassis_number="JAAKP34H2D7P06865"):
        self.truck_id = truck_id
        self.chassis_number = chassis_number

    def render_inbox_list(self, messages_list):
        """عرض قائمة الرسائل مع الشارات الحمراء"""
        formatted_messages = []
        for msg in messages_list:
            status_icon = "🔴 (جديدة)" if msg["status"] == "UNREAD" else "✅ (تمت القراءة)"
            urgent_tag = "⚠️ [عاجل] " if msg.get("is_urgent") else ""
            
            entry = {
                "DISPLAY_TITLE": f"{status_icon} {urgent_tag}{msg['title']}",
                "DATE": msg["received_at"],
                "MSG_ID": msg["message_id"]
            }
            formatted_messages.append(entry)
            
        return formatted_messages

    def render_message_details(self, message_obj):
        """عرض تفاصيل الرسالة عند الضغط عليها مع تثبيت القراءة آلياً"""
        timestamp_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_obj["status"] = "READ"
        message_obj["read_at"] = timestamp_now

        return {
            "HEADER": f"📩 رسالة من الإدارة - شاحنة ({self.truck_id})",
            "CONTENT": message_obj["content"],
            "TIMESTAMP": f"تاريخ الاستلام: {message_obj['received_at']} | تاريخ القراءة: {timestamp_now}",
            "REPLY_ACTION": "🎙️ [ اضغط هنا للرد بالتسجيل الصوتي أو النص ]"
        }

    def send_driver_reply_action(self, message_id, reply_text="", voice_note_file=None):
        """إرسال رد السائق وتوثيقه آلياً"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "success": True,
            "message": "🚀 تم إرسال الرد وتأكيد الاطلاع بنجاح إلى غرفة التحكم والإدارة!",
            "payload": {
                "truck_id": self.truck_id,
                "reply_to": message_id,
                "reply_text": reply_text,
                "voice_status": "ATTACHED" if voice_note_file else "NONE",
                "timestamp": timestamp
            }
        }

# --- تجربة الشاشة ---
if __name__ == "__main__":
    inbox_ui = MessagesInboxUI()
    
    # رسائل افتراضية للتجربة
    sample_messages = [
        {
            "message_id": "MSG_99",
            "title": "تنبيه غسيل وتنظيف صندوق الشاحنة",
            "content": "يرجى تنظيف صندوق الشاحنة غداً وإعطاء الموزع مهلة يوم.",
            "is_urgent": True,
            "status": "UNREAD",
            "received_at": "2026-07-31 08:00:00"
        }
    ]
    
    print("--- 1. عرض الرسائل في الصندوق ---")
    inbox = inbox_ui.render_inbox_list(sample_messages)
    print(inbox[0]["DISPLAY_TITLE"])
    
    print("\n--- 2. فتح الرسالة وقراءتها ---")
    details = inbox_ui.render_message_details(sample_messages[0])
    print(details["CONTENT"])
    print(details["TIMESTAMP"])