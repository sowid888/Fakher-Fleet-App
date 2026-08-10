# مجلد: app_ui_screens / ai_driver_assistant.py

import datetime

class HybridAIDriverAssistant:
    def __init__(self, truck_id="2600-001"):
        self.truck_id = truck_id
        
        # 🏢 الطبقة الأولى: جدول الأسئلة والأجوبة المعتمدة الخاصة بالشركة
        self.company_knowledge_base = {
            "مستودع الزيت": "تستلم الزيت من مستودع الفرع الرئيسي - المسؤول: أبو فهد (0501112233).",
            "استلام قطع الغيار": "من كاونتر الصيانة المركزي بجانب الورشة الرئيسية - ساعات العمل 8 ص إلى 5 م.",
            "الورشة المعتمدة": "ورشة الخليج المعتمدة - المهندس أحمد (0504445566) - حي الصناعية.",
            "مستحقات الوقود": "تعبئة الوقود من محطات التسهيلات المعتمدة عبر بطاقة الشاحنة الرقمية.",
            "غسيل ونظافة الصندوق": "يتم الغسيل أسبوعياً في مغسلة الأسطول المركزية ويُعطى الموزع مهلة يوم واحد."
        }

    def ask_ai_assistant(self, driver_question, is_technical_fault=False):
        """
        محرك الإجابة المزدوج:
        1. يفحص أولاً الأسئلة الخاصة بالشركة.
        2. إذا لم يجدها وكانت المشكلة ميكانيكية، يجري بحثاً ذكياً في النت.
        """
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # 1. البحث في قاعدة بيانات الشركة الداخلية (Local Knowledge)
        for key_phrase, company_answer in self.company_knowledge_base.items():
            if key_phrase in driver_question:
                return {
                    "source": "🏢 [بيانات الشركة الداخلية]",
                    "ai_response": f"📌 إجابة مخصصة من إدارة الأسطول:\n{company_answer}",
                    "time": timestamp
                }

        # 2. إذا كان سؤالاً فنياً أو عطل ميكانيكي -> البحث عبر الإنترنت (Web Search)
        if is_technical_fault or "عطل" in driver_question or "رمز" in driver_question or "حرارة" in driver_question:
            return {
                "source": "🌐 [بحث الذكاء الاصطناعي في النت]",
                "ai_response": f"🤖 بناءً على التحليل الفني والبحث المباشر لمشكلة ({driver_question}):\n"
                               f"• السبب المرجح: افحص طلمبة الديزل أو فلتر الهواء.\n"
                               f"• التوجيه: يمكنك الذهاب لأقرب ورشة صيانة أو التواصل مع مهندس الورشة المعتمد.",
                "time": timestamp
            }

        # 3. إجابة عامة وترحيب
        return {
            "source": "💡 [إرشادات المساعد الذكي]",
            "ai_response": "مرحباً بك! يمكنك سؤالي عن أماكن استلام الزيت، الورش المعتمدة، أو البحث عن حلول لأي عطل في الشاحنة.",
            "time": timestamp
        }

# --- تجربة المساعد الذكي المطور ---
if __name__ == "__main__":
    ai = HybridAIDriverAssistant()

    print("=== 🧠 تجربة الذكاء الاصطناعي المزدوج (شركة + بحث نت) ===")

    print("\n--- 1. السائق يسأل سؤالاً خاصاً بالشركة (استلام الزيت) ---")
    res1 = ai.ask_ai_assistant("من أين أستلم الزيت؟")
    print(res1["source"])
    print(res1["ai_response"])

    print("\n--- 2. السائق يسأل عن الورشة المعتمدة ---")
    res2 = ai.ask_ai_assistant("ما هي الورشة المعتمدة للشركة؟")
    print(res2["source"])
    print(res2["ai_response"])

    print("\n--- 3. السائق يواجه عطلاً غريباً (بحث في النت) ---")
    res3 = ai.ask_ai_assistant("الشاحنة تتوقف عند الضغط على دواسة البنزين", is_technical_fault=True)
    print(res3["source"])
    print(res3["ai_response"])