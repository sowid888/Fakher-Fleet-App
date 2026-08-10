# مجلد: app_ui_screens / duty_engineer_ai.py

import datetime

class DutyEngineerAI:
    def __init__(self, truck_id="2600-001"):
        self.truck_id = truck_id
        self.engineer_title = "👨‍🔧 المهندس المناوب (طوارئ 24/7)"

    def start_diagnostic(self, driver_problem_description, step=1):
        """
        محرك التشخيص الميداني التفاعلي مع السائق أثناء السفر وفي أوقات الإجازات
        """
        timestamp = datetime.datetime.now().strftime("%H:%M")

        if step == 1:
            return {
                "title": self.engineer_title,
                "message": f"أهلاً بك. أنا {self.engineer_title}.\n"
                           f"سمعتُ أن لديك مشكلة في الشاحنة ({self.truck_id}). لنشخص العطل الميكانيكي/الكهربائي معاً:\n"
                           f"السؤال الأول: هل إضاءة التابلوه والأنوار الأمامية تعمل بشكل طبيعي؟ (أجب: نعم / لا)",
                "next_step": 2,
                "time": timestamp
            }

        elif step == 2:
            if "نعم" in driver_problem_description:
                return {
                    "title": self.engineer_title,
                    "message": f"ممتاز، البطارية والكهرباء سليمة.\n"
                               f"السؤال الثاني: هل توقفت الشاحنة بشكل تدريجي وتقطّع أم انطفأت فجأة دفعة واحدة؟",
                    "next_step": 3,
                    "time": timestamp
                }
            else:
                return {
                    "title": self.engineer_title,
                    "message": f"🔴 [عطل كهربائي]: المشكلة في توصيلات البطارية أو الدينامو.\n"
                               f"التوجيه: افحص ثبات أصابع البطارية، أو اتصل بمسؤول الصيانة فوراً.",
                    "next_step": None,
                    "time": timestamp
                }

        elif step == 3:
            return {
                "title": self.engineer_title,
                "message": f"🟢 [التشخيص الميداني عبر المهندس المناوب]:\n"
                           f"• العطل المرجح: انسداد فلاتر الديزل أو وجود هواية في طلمبة الوقود.\n"
                           f"• الإجراء الموصى به: قم بعملية الضخ اليدوي (تحضير الديزل) 10 مرات ثم جرب التشغيل.\n"
                           f"• في حال عدم الاستجابة: اتصل بمسؤول السطحات أبو فهد (0503334444).",
                "next_step": None,
                "time": timestamp
            }

# --- تجربة المهندس المناوب ---
if __name__ == "__main__":
    engineer = DutyEngineerAI()
    print("=== 👨‍🔧 تجربة المهندس المناوب للطوارئ الميدانية ===")
    p1 = engineer.start_diagnostic("الشاحنة ترفض التشغيل في خط السفر", step=1)
    print(p1["message"])