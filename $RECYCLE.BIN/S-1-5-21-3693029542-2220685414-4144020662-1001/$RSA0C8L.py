import os
import time
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase

# استدعاء مكتبات لحم وتعديل الخط العربي لكي يظهر ملحوماً وصحيحاً
import arabic_reshaper
from bidi.algorithm import get_display

# محاولة استدعاء مكتبات تسجيل الصوت بشكل آمن ومنع انهيار البرنامج
try:
    import sounddevice as sd
    from scipy.io import wavfile
    AUDIO_SUPPORT = True
except Exception:
    AUDIO_SUPPORT = False

# ضبط حجم الشاشة لمحاكاة الجوال على الكمبيوتر
Window.size = (360, 640)

# 🛠️ الحل الجذري: تحديد مسار خط نظام الويندوز المباشر لضمان عدم حدوث خطأ "الملف غير موجود"
windows_font_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "arial.ttf")

if os.path.exists(windows_font_path):
    LabelBase.register(name="ArabicFont", fn_regular=windows_font_path)
else:
    # حل احتياطي إذا لم يجد خط أريال لأي سبب
    LabelBase.register(name="ArabicFont", fn_regular="")

def fix_arabic(text):
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

class GawziFleetApp(App):
    def build(self):
        self.title = "منظومة الجوزي السيادية - أسطول 2600"
        
        # قاعدة بيانات المحاكاة للباركود المتعدد المرتبط برقم واتساب السائق
        self.driver_profile = {
            "driver_name": "عبده الجوزي",
            "whatsapp": "+96777XXXXXXX",
            "vehicles": {
                "2/97500": {"type": "شاحنة", "chassis": "CH-TRUCK-9921", "plate": "2/97500"},
                "3/45100": {"type": "سيارة", "chassis": "CH-CAR-3341", "plate": "3/45100"}
            }
        }
        
        # تحديد اللوحة النشطة حالياً عند فتح البرنامج
        self.active_plate = "2/97500"
        
        self.root_layout = BoxLayout(orientation='vertical', padding=10, spacing=8)
        self.show_main_dashboard()
        return self.root_layout

    # 1️⃣ الواجهة الرئيسية المرتبة ذكياً لسهولة الاستخدام الميداني
    def show_main_dashboard(self):
        self.root_layout.clear_widgets()
        
        current_v = self.driver_profile["vehicles"][self.active_plate]
        
        # كرت الهوية السيادية المستخرج من الباركود المشفر
        id_card = f"👤 {self.driver_profile['driver_name']} | 📱 {self.driver_profile['whatsapp']}\n⚙️ {current_v['type']} | شاصيه: {current_v['chassis']}"
        header_lbl = Label(text=fix_arabic(id_card), font_name="ArabicFont", font_size='12sp', size_hint_y=None, height=45, color=get_color_from_hex('#F1C40F'), halign='center')
        self.root_layout.add_widget(header_lbl)
        
        # المفتاح الذكي لمنع التداخل والتبديل الفوري بين اللوحات المعتمدة للسائق
        switch_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        lbl_switch = Label(text=fix_arabic("🚚 اختر اللوحة المعدنية الحالية:"), font_name="ArabicFont", font_size='12sp')
        
        self.plate_spinner = Spinner(
            text=self.active_plate,
            values=list(self.driver_profile["vehicles"].keys()),
            font_name="ArabicFont",
            background_color=get_color_from_hex('#8E44AD')
        )
        self.plate_spinner.bind(text=self.on_plate_change)
        switch_box.add_widget(self.plate_spinner)
        switch_box.add_widget(lbl_switch)
        self.root_layout.add_widget(switch_box)
        
        # صندوق التمرير الرئيسي للمفاتيح العملاقة
        scroll = ScrollView()
        main_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        main_box.bind(minimum_height=main_box.setter('height'))
        
        # 👑 ترتيب المفاتيح بشكل ذكي وسهل جداً حسب طلبك الصارم
        btn_maintenance = Button(text=fix_arabic("🚨 بلاغات قائمة الأعطال الفورية"), font_name="ArabicFont", font_size='18sp', bold=True, size_hint_y=None, height=65, background_color=get_color_from_hex('#E74C3C'))
        btn_maintenance.bind(on_press=self.show_maintenance_categories)
        main_box.add_widget(btn_maintenance)
        
        btn_unregistered = Button(text=fix_arabic("📝 أعطال ليست مسجلة (صوت + كتابة)"), font_name="ArabicFont", font_size='16sp', bold=True, size_hint_y=None, height=60, background_color=get_color_from_hex('#D35400'))
        btn_unregistered.bind(on_press=self.show_unregistered_faults_screen)
        main_box.add_widget(btn_unregistered)
        
        btn_complaints = Button(text=fix_arabic("📢 قسم الشكاوى والتقييد المطور"), font_name="ArabicFont", font_size='16sp', bold=True, size_hint_y=None, height=60, background_color=get_color_from_hex('#3498DB'))
        btn_complaints.bind(on_press=self.show_complaints_screen)
        main_box.add_widget(btn_complaints)
        
        btn_replacements = Button(text=fix_arabic("🛠️ سجل استبدال القطع والزيوت والعدادات"), font_name="ArabicFont", font_size='16sp', bold=True, size_hint_y=None, height=60, background_color=get_color_from_hex('#2ECC71'))
        btn_replacements.bind(on_press=self.show_replacements_screen)
        main_box.add_widget(btn_replacements)
        
        btn_km_fuel = Button(text=fix_arabic("📊 إرسال قراءة العداد وتعبئة الوقود"), font_name="ArabicFont", font_size='16sp', bold=True, size_hint_y=None, height=60, background_color=get_color_from_hex('#16A085'))
        btn_km_fuel.bind(on_press=self.show_km_fuel_screen)
        main_box.add_widget(btn_km_fuel)
        
        btn_alerts = Button(text=fix_arabic("🔔 صندوق التنبيهات وتذكيرات الصيانة [1]"), font_name="ArabicFont", font_size='16sp', bold=True, size_hint_y=None, height=60, background_color=get_color_from_hex('#F39C12'))
        btn_alerts.bind(on_press=self.show_alerts_box_screen)
        main_box.add_widget(btn_alerts)
        
        scroll.add_widget(main_box)
        self.root_layout.add_widget(scroll)
        
        # التذييل الزمني الآلي لتوثيق تاريخ ووقت كل عملية بالثانية
        footer_lbl = Label(text=f"⏰ {time.strftime('%Y-%m-%d %H:%M:%S')}", font_size='11sp', size_hint_y=None, height=15, color=get_color_from_hex('#7F8C8D'))
        self.root_layout.add_widget(footer_lbl)

    def on_plate_change(self, spinner, text):
        self.active_plate = text
        self.show_main_dashboard()

    # 2️⃣ شاشة أقسام الأعطال (شاحنات أو سيارات تلقائياً) مع أزرار إرسال فردية لكل عطل
    def show_maintenance_categories(self, instance):
        self.root_layout.clear_widgets()
        current_v = self.driver_profile["vehicles"][self.active_plate]
        
        lbl = Label(text=fix_arabic(f"🚨 أقسام بلاغات عطل لوحة: {self.active_plate}"), font_name="ArabicFont", font_size='16sp', bold=True, size_hint_y=None, height=35)
        self.root_layout.add_widget(lbl)
        
        if current_v["type"] == "شاحنة":
            self.fault_tree = {
                "🔧 أعطال ميكانيكية": ["لايوجد عزم", "استهلاك مرتفع للديزل", "تاخير في التشغيل", "صوت في المحرك غريب", "ارتفاع حرارة المحرك", "تهريب ماء من التانكي", "تهريب زيت من الاقزوز", "تهريب زيت من تحت المحرك", "تهريب ديزل من تحت المحرك", "تهريب زيت السكان الدركسون"],
                "⚡ أعطال كهربائية": ["الشاحنه لا تعمل بسبب البطاريات ضعيفه تمامنا", "الشاحنه احيانا البطاريات ضعيفه اذا كنت في الصباح فقط", "البطاريه ضعيفة في الصباح فقط", "نور الامامي جهة السائق معطل", "نور الامامي جهة الراكب معطل", "نور الاسطبات الخلفية جهة السائق معطله", "نور الاسطبات الخلفية جهة الراكب معطل", "نور إشارة الانعطاف خلف السائق معطله", "نور إشارة الانعطاف خلف الراكب معطله", "بيت شاحن الجوال معطل", "انارة الثلاجة الداخلية معطله", "الهون كلاكس طريقة معطل"],
                "🛑 أعطال البريك": ["البريك يصطر صوت", "البريك ضعيف", "تهريب سم بريك داخل الكبينه من علبه فوق", "تهريب سم بريك من قدام جهة الراكب او السائق", "تهريب سم بريك من الخلف من جهة الراكب او السائق", "تهريب زيت الدفريشن الجرويل"],
                "❄️ أعطال الثلاجة": ["تهريب ماء من السقف", "تهريب ماء من الجوانب", "تهريب ماء من الباب الجانبي", "تهريب ماء من الابواب الخلفيه", "عند المطبات الثلاجه تصدر صوت", "تلفيه في عمود اقفال ابواب الثلاجه", "تلفيه في مفصلات ابواب الثلاجه", "تلفيه اقفال ابواب الثلاجه"]
            }
        else:
            self.fault_tree = {
                "🔧 أعطال ميكانيكية": ["لايوجد عزم", "استهلاك مرتفع للوقود", "تاخير في التشغيل", "صوت في المحرك غريب", "ارتفاع حرارة المحرك", "تهريب ماء من التانكي", "تهريب زيت من الاقزوز", "تهريب زيت من تحت المحرك", "تهريب زيت السكان الدركسون"],
                "⚡ أعطال كهربائية": ["الشاحنه لا تعمل بسبب البطاريات ضعيفه تمامنا", "الشاحنه احيانا البطاريات ضعيفه اذا كنت في الصباح فقط", "البطاريه ضعيفة في الصباح فقط", "نور الامامي جهة السائق معطل", "نور الامامي جهة الراكب معطل", "نور الاسطبات الخلفية جهة السائق معطله", "نور الاسطبات الخلفية جهة الراكب معطل", "نور إشارة الانعطاف خلف السائق معطله", "نور إشارة الانعطاف خلف الراكب معطله", "بيت شاحن الجوال معطل", "الهون كلاكس طريقة معطل"],
                "🛑 أعطال البريك": ["البريك يصطر صوت", "البريك ضعيف", "تهريب سم بريك داخل الكبينه من علبه فوق", "تهريب سم بريك من قدام جهة الراكب او السائق", "تهريب سم بريك من الخلف من جهة الراكب او السائق", "تهريب زيت البريك", "الاطارات تالفه"]
            }

        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        
        for category_name, sub_faults in self.fault_tree.items():
            cat_lbl = Label(text=fix_arabic(f"--- {category_name} ---"), font_name="ArabicFont", font_size='14sp', size_hint_y=None, height=30, color=get_color_from_hex('#F1C40F'))
            box.add_widget(cat_lbl)
            
            for fault in sub_faults:
                fault_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=5)
                
                btn_send = Button(text=fix_arabic("🚀 إرسال"), font_name="ArabicFont", font_size='12sp', size_hint_x=0.25, background_color=get_color_from_hex('#2ECC71'))
                btn_send.bind(on_press=lambda inst, f=fault: self.send_fault_action(f))
                
                lbl_fault = Label(text=fix_arabic(fault), font_name="ArabicFont", font_size='13sp', size_hint_x=0.75, halign='right')
                
                fault_row.add_widget(btn_send)
                fault_row.add_widget(lbl_fault)
                box.add_widget(fault_row)
                
        scroll.add_widget(box)
        self.root_layout.add_widget(scroll)
        
        btn_back = Button(text=fix_arabic("⬅️ عودة للرئيسية"), font_name="ArabicFont", size_hint_y=None, height=45, background_color=get_color_from_hex('#7F8C8D'))
        btn_back.bind(on_press=lambda inst: self.show_main_dashboard())
        self.root_layout.add_widget(btn_back)

    def send_fault_action(self, fault_name):
        print(f"تم إرسال بلاغ عطل: ({fault_name}) للمركبة {self.active_plate}")

    # 3️⃣ شاشة أعطال ليست مسجلة
    def show_unregistered_faults_screen(self, instance):
        self.root_layout.clear_widgets()
        
        lbl = Label(text=fix_arabic("📝 تسجيل عطل حر غير مدرج بالقائمة"), font_name="ArabicFont", font_size='16sp', bold=True, size_hint_y=None, height=40)
        self.root_layout.add_widget(lbl)
        
        self.custom_fault_input = TextInput(hint_text=fix_arabic("ادخل المشكلة يدوياً هنا..."), font_name="ArabicFont", multiline=True, size_hint_y=None, height=90)
        self.root_layout.add_widget(self.custom_fault_input)
        
        self.voice_btn = Button(text=fix_arabic("🎤 اضغط هنا للتسجيل الصوتي\n(المدة المتاحة: 60 ثانية)"), font_name="ArabicFont", halign='center', background_color=get_color_from_hex('#E67E22'), size_hint_y=None, height=80)
        self.voice_btn.bind(on_press=self.record_voice_fault)
        self.root_layout.add_widget(self.voice_btn)
        
        action_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=45)
        btn_send = Button(text=fix_arabic("🚀 إرسال البلاغ الحر"), font_name="ArabicFont", bold=True, background_color=get_color_from_hex('#2ECC71'))
        btn_send.bind(on_press=self.submit_unregistered_fault)
        btn_back = Button(text=fix_arabic("⬅️ عودة"), font_name="ArabicFont", background_color=get_color_from_hex('#7F8C8D'))
        btn_back.bind(on_press=lambda inst: self.show_main_dashboard())
        
        action_box.add_widget(btn_back)
        action_box.add_widget(btn_send)
        self.root_layout.add_widget(action_box)

    def record_voice_fault(self, instance):
        if AUDIO_SUPPORT:
            try:
                self.voice_btn.text = fix_arabic("🔴 جاري تسجيل صوتك الآن...\nتحدث لمده 60 ثانية")
                self.voice_btn.background_color = get_color_from_hex('#C0392B')
                fs = 44100
                recording = sd.rec(int(60 * fs), samplerate=fs, channels=1)
                sd.wait()
                wavfile.write("Gawzi_Custom_Fault_Audio.wav", fs, recording)
                self.voice_btn.text = fix_arabic("✅ تم حفظ وتأكيد التسجيل الصوتي")
                self.voice_btn.background_color = get_color_from_hex('#27AE60')
            except Exception:
                self.voice_btn.text = fix_arabic("⚠️ عذراً: المايك غير مدعوم على هذا الجهاز حالياً")
        else:
            self.voice_btn.text = fix_arabic("⚠️ عذراً: التسجيل مدعوم فقط على الجوال")

    def submit_unregistered_fault(self, instance):
        self.show_main_dashboard()

    # 4️⃣ قسم الشكاوى المطور والتقييد الصارم
    def show_complaints_screen(self, instance):
        self.root_layout.clear_widgets()
        
        lbl = Label(text=fix_arabic("📢 تقييد شكوى جديدة وضبط التوجيه والمكان"), font_name="ArabicFont", font_size='15sp', bold=True, size_hint_y=None, height=35)
        self.root_layout.add_widget(lbl)
        
        options = ["إدارة الحركة", "المهندس التابع للشركه", "ميكانيكي", "مهندس الكهربائي", "مهندس السمكري", "البنشر", "استبدال الزيوت", "الحارس التابع للشركه"]
        options_fixed = [fix_arabic(opt) for opt in options]
        self.comp_spinner = Spinner(text=options_fixed[0], values=options_fixed, font_name="ArabicFont", size_hint_y=None, height=40, background_color=get_color_from_hex('#2C3E50'))
        self.root_layout.add_widget(self.comp_spinner)
        
        self.comp_loc = TextInput(hint_text=fix_arabic("حدد مكان المشكلة/الحدث بدقة هنا..."), font_name="ArabicFont", size_hint_y=None, height=35, multiline=False)
        self.root_layout.add_widget(self.comp_loc)
        
        split_box = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=120)
        
        self.comp_audio_btn = Button(text=fix_arabic("🎤 تسجيل صوتي\n(60 ثانية)"), font_name="ArabicFont", font_size='12sp', size_hint_x=0.4, background_color=get_color_from_hex('#E67E22'), halign='center')
        self.comp_audio_btn.bind(on_press=self.record_complaint_audio)
        
        self.comp_text_input = TextInput(hint_text=fix_arabic("اكتب نص الشكوى هنا..."), font_name="ArabicFont", size_hint_x=0.6, multiline=True)
        
        split_box.add_widget(self.comp_audio_btn)
        split_box.add_widget(self.comp_text_input)
        self.root_layout.add_widget(split_box)
        
        action_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=45)
        btn_send = Button(text=fix_arabic("🚀 إرسال الشكوى"), font_name="ArabicFont", bold=True, background_color=get_color_from_hex('#2ECC71'))
        btn_send.bind(on_press=self.submit_complaint_action)
        btn_back = Button(text=fix_arabic("⬅️ إلغاء وعودة"), font_name="ArabicFont", background_color=get_color_from_hex('#7F8C8D'))
        btn_back.bind(on_press=lambda inst: self.show_main_dashboard())
        
        action_box.add_widget(btn_back)
        action_box.add_widget(btn_send)
        self.root_layout.add_widget(action_box)

    def record_complaint_audio(self, instance):
        if AUDIO_SUPPORT:
            try:
                self.comp_audio_btn.text = fix_arabic("🔴 تسجيل...\n60 ثانية")
                self.comp_audio_btn.background_color = get_color_from_hex('#C0392B')
                fs = 44100
                recording = sd.rec(int(60 * fs), samplerate=fs, channels=1)
                sd.wait()
                wavfile.write("Gawzi_Complaint_Audio.wav", fs, recording)
                self.comp_audio_btn.text = fix_arabic("✅ تم حفظ الصوت")
                self.comp_audio_btn.background_color = get_color_from_hex('#27AE60')
            except Exception:
                self.comp_audio_btn.text = fix_arabic("⚠️ غير مدعوم")
        else:
            self.comp_audio_btn.text = fix_arabic("⚠️ غير مدعوم")

    def submit_complaint_action(self, instance):
        self.show_main_dashboard()

    # 5️⃣ شاشة سجل استبدال القطع والزيوت
    def show_replacements_screen(self, instance):
        self.root_layout.clear_widgets()
        current_v = self.driver_profile["vehicles"][self.active_plate]
        
        lbl = Label(text=fix_arabic(f"🛠️ سجل استبدال القطع - واجهة {current_v['type']}"), font_name="ArabicFont", font_size='15sp', bold=True, size_hint_y=None, height=35)
        self.root_layout.add_widget(lbl)
        
        scroll = ScrollView()
        fields_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        fields_box.bind(minimum_height=fields_box.setter('height'))
        
        if current_v["type"] == "شاحنة":
            items = ["🛢️ استبدال زيت محرك الشاحنة (ديزل ثقيل)", "🧼 تنظيف وصيانة صندوق الشاحنة الدولي", "🛞 وزن ومعايرة الإطارات الدوري", "⛽ تغيير فلاتر وقود ديزل الشاحنة"]
        else:
            items = ["🛢️ استبدال زيت محرك السيارة (بنزين/خفيف)", "💨 تغيير فلتر زيت المحرك وفلاتر الهواء", "🔌 استبدال شمعات الاحتراق (البواجي)", "⚙️ استبدال قطع استهلاكية أخرى"]

        for item in items:
            row = BoxLayout(orientation='vertical', size_hint_y=None, height=55, spacing=2)
            item_lbl = Label(text=fix_arabic(item), font_name="ArabicFont", font_size='12sp', halign='right')
            item_inp = TextInput(hint_text=fix_arabic("أدخل قراءة العداد الحالية..."), font_name="ArabicFont", multiline=False, size_hint_y=None, height=32)
            row.add_widget(item_lbl)
            row.add_widget(item_inp)
            fields_box.add_widget(row)
            
        scroll.add_widget(fields_box)
        self.root_layout.add_widget(scroll)
        
        action_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=45)
        btn_save = Button(text=fix_arabic("💾 حفظ وتصفير الجدولة"), font_name="ArabicFont", bold=True, background_color=get_color_from_hex('#2ECC71'))
        btn_save.bind(on_press=lambda inst: self.show_main_dashboard())
        btn_back = Button(text=fix_arabic("⬅️ عودة"), font_name="ArabicFont", background_color=get_color_from_hex('#7F8C8D'))
        btn_back.bind(on_press=lambda inst: self.show_main_dashboard())
        
        action_box.add_widget(btn_back)
        action_box.add_widget(btn_save)
        self.root_layout.add_widget(action_box)

    # 6️⃣ شاشة قراءة الكيلومتر وتعبئة الوقود
    def show_km_fuel_screen(self, instance):
        self.root_layout.clear_widgets()
        
        lbl = Label(text=fix_arabic("📊 تحديث عداد الكيلومتر والوقود الدوري"), font_name="ArabicFont", font_size='15sp', bold=True, size_hint_y=None, height=35)
        self.root_layout.add_widget(lbl)
        
        km_lbl = Label(text=fix_arabic("حقل عدد الكيلومتر الحالي (إجباري):"), font_name="ArabicFont", size_hint_y=None, height=20)
        self.km_input = TextInput(hint_text=fix_arabic("أدخل قراءة العداد الحالية هنا..."), size_hint_y=None, height=35, multiline=False)
        self.root_layout.add_widget(km_lbl)
        self.root_layout.add_widget(self.km_input)
        
        fuel_lbl = Label(text=fix_arabic("⛽ كمية التعبئة بالليتر (من 1 لتر إلى 220 لتر):"), font_name="ArabicFont", size_hint_y=None, height=20)
        self.root_layout.add_widget(fuel_lbl)
        
        fuel_values = [str(i) for i in range(1, 221)]
        self.fuel_spinner = Spinner(text="1", values=fuel_values, size_hint_y=None, height=35, background_color=get_color_from_hex('#34495E'))
        self.root_layout.add_widget(self.fuel_spinner)
        
        self.station_input = TextInput(hint_text=fix_arabic("اسم المحطة (اختياري)"), font_name="ArabicFont", size_hint_y=None, height=32, multiline=False)
        self.invoice_num_input = TextInput(hint_text=fix_arabic("رقم الفاتورة"), font_name="ArabicFont", size_hint_y=None, height=32, multiline=False)
        self.root_layout.add_widget(self.station_input)
        self.root_layout.add_widget(self.invoice_num_input)
        
        invoice_types = [fix_arabic("آجل"), fix_arabic("نقداً"), fix_arabic("محطة شركة الجوزي")]
        self.invoice_type_spinner = Spinner(text=invoice_types[0], values=invoice_types, font_name="ArabicFont", size_hint_y=None, height=35, background_color=get_color_from_hex('#2C3E50'))
        self.root_layout.add_widget(self.invoice_type_spinner)
        
        action_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=45)
        btn_send = Button(text=fix_arabic("🚀 إرسال القراءة والوقود"), font_name="ArabicFont", bold=True, background_color=get_color_from_hex('#2ECC71'))
        btn_send.bind(on_press=self.submit_km_fuel_action)
        btn_back = Button(text=fix_arabic("⬅️ عودة"), font_name="ArabicFont", background_color=get_color_from_hex('#7F8C8D'))
        btn_back.bind(on_press=lambda inst: self.show_main_dashboard())
        
        action_box.add_widget(btn_back)
        action_box.add_widget(btn_send)
        self.root_layout.add_widget(action_box)

    def submit_km_fuel_action(self, instance):
        self.show_main_dashboard()

    # 7️⃣ صندوق التنبيهات المطور
    def show_alerts_box_screen(self, instance):
        self.root_layout.clear_widgets()
        
        lbl = Label(text=fix_arabic("🔔 صندوق تنبيهات ومعدلات صيانة أسطول 2600"), font_name="ArabicFont", font_size='15sp', bold=True, size_hint_y=None, height=35)
        self.root_layout.add_widget(lbl)
        
        alert_text = "⚠️ عزيزي السائق: يرجى تحديث عداد المسافة، أو التوجه لتغيير الفلاتر والزيوت المقررة فوراً."
        alert_lbl = Label(text=fix_arabic(alert_text), font_name="ArabicFont", font_size='13sp', halign='center', color=get_color_from_hex('#E74C3C'))
        self.root_layne = Button(text=fix_arabic("✅ تم تنفيذ العمل المطلوب مني"), font_name="ArabicFont", font_size='16sp', bold=True, size_hint_y=None, height=60, background_color=get_color_from_hex('#2ECC71'))
        btn_done.bind(on_press=self.clear_alerts_and_dismiss)
        self.ret(btn_done)
        
        btn_back = Button(text=fix_arabic("⬅️ عودة للرئيسية"), font_name="ArabicFont", size_hint_y=None, height=45, background_color=get_color_from_hex('#7F8C8D'))
        btn_back.bin