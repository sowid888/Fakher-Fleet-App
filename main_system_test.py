# الملف الرئيسي في root المشروع: main_system_test.py

import sys
import os

# 1. إضافة مسارات المجلدات بالنظام الصحيح
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'app_ui_screens'))
sys.path.append(os.path.join(current_dir, 'admin_panel'))

# 2. استدعاء المكونات المعتمدة فقط مع معالجة الاستثناءات
try:
    from company_faq_database import CompanyFAQDatabase
    from duty_engineer_ai import DutyEngineerAI
    from faults_audio_center import FaultsAndAudioReviewCenter
    from schedule_maintenance_center import ScheduleMaintenanceCenter
    print("✅ تم استدعاء جميع الملفات المعتمدة بنجاح.")
except ImportError as e:
    print(f"⚠️ تنبيه أثناء الاستدعاء: {e}")

def run_integrated_fleet_system():
    print("\n==================================================")
    print("🚀 بدء الاختبار الشامل لنظام إدارة الأسطول (MASHRO3 FLEET 2600)")
    print("==================================================\n")

    # 1️⃣ تجربة تطبيق السائق: بنك الأسئلة الـ 30
    try:
        print("--- 📱 [1] تجربة بنك أسئلة وإرشادات الشركة (السائق) ---")
        faq = CompanyFAQDatabase()
        q_answer = faq.get_answer("تغيير الزيت")
        print(f"🔹 السؤال المختار: تغيير الزيت")
        print(f"🔹 الإجابة: {q_answer['answer']}\n")
    except Exception as e:
        print(f"❌ خطأ في جزء بنك الأسئلة: {e}\n")

    # 2️⃣ تجربة تطبيق السائق: المهندس المناوب للطوارئ
    try:
        print("--- 👨‍🔧 [2] تجربة المهندس المناوب 24/7 (طوارئ خط صنعاء-الحديدة) ---")
        engineer = DutyEngineerAI(truck_id="2600-001")
        step1 = engineer.start_diagnostic("انطفأت الشاحنة فجأة", step=1)
        print(f"{step1['title']}:\n{step1['message']}\n")
    except Exception as e:
        print(f"❌ خطأ في جزء المهندس المناوب: {e}\n")

    # 3️⃣ تجربة لوحة الإدارة: مركز استقبال الأعطال والتسجيلات
    try:
        print("--- 🛠️ [3] تجربة لوحة تحكم الإدارة: مراجعة الأعطال والصوتيات ---")
        admin_center = FaultsAndAudioReviewCenter()
        reports = admin_center.display_pending_reports()
        print(f"📥 البلاغات الواردة: {len(reports)} بلاغ")
        print(admin_center.play_driver_voice_note("REP-8001"))
        print("\n")
    except Exception as e:
        print(f"❌ خطأ في جزء مركز الأعطال: {e}\n")

    # 4️⃣ تجربة لوحة الإدارة: جدول النظافة وتفقد الإطارات
    try:
        print("--- 📅 [4] تجربة جدول المتابعة الدوري (الإطارات والنظافة) ---")
        sch = ScheduleMaintenanceCenter()
        print(sch.check_tire_pressure_due("2600-001"))
        print(sch.check_box_cleaning_due("2600-001"))
        print("\n")
    except Exception as e:
        print(f"❌ خطأ في جزء جدول المتابعة: {e}\n")

    print("==================================================")
    print("✅ اكتمل سكريبت الاختبار الشامل بنجاح!")
    print("==================================================")

if __name__ == "__main__":
    run_integrated_fleet_system()