# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - واجهة المستخدم الرئيسية المباشرة (Kivy UI)
تاريخ التحديث: 2026
"""

import os
import sys

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase

# -------------------------------------------------------------
# 1. دعم الخط العربي والتحقق من وجوده
# -------------------------------------------------------------
local_font = os.path.join(os.path.dirname(__file__), "arial.ttf")
win_system_font = r"C:\Windows\Fonts\arial.ttf"

if os.path.exists(local_font):
    LabelBase.register(name="ArabicFont", fn_regular=local_font)
    DEFAULT_FONT = "ArabicFont"
elif os.path.exists(win_system_font):
    LabelBase.register(name="ArabicFont", fn_regular=win_system_font)
    DEFAULT_FONT = "ArabicFont"
else:
    DEFAULT_FONT = "Roboto"

def ar(text):
    """دالة معالجة وتشكيل النصوص العربية"""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)

# -------------------------------------------------------------
# 2. بناء الواجهة الرئيسية بالأزرار الستة الكبيرة
# -------------------------------------------------------------
class AppMainUI(BoxLayout):
    def __init__(self, truck_id="2600-001", driver_name="سائق الميدان", **kwargs):
        super().__init__(orientation='vertical', spacing=12, padding=15, **kwargs)
        self.truck_id = truck_id
        self.driver_name = driver_name

        # الشريط العلوي (رأس الشاشة)
        header_text = ar(f"شاحنة: {self.truck_id} | السائق: {self.driver_name}")
        header = Label(
            text=header_text,
            font_size='18sp',
            font_name=DEFAULT_FONT,
            size_hint_y=0.12,
            color=(0.1, 0.9, 0.5, 1)
        )
        self.add_widget(header)

        # شبكة المفاتيح الستة الكبيرة (2 أعمدة × 3 صفوف)
        grid = GridLayout(cols=2, spacing=12, size_hint_y=0.88)

        # قائمة الأزرار بالنصوص النظيفة بدون إيموجي لتجنب أشكال المربعات المكسورة
        self.buttons_config = [
            (1, "1. قراءة العداد والتنبيهات", (0.1, 0.4, 0.6, 1)),
            (2, "2. التزود بالوقود والإيصال", (0.2, 0.6, 0.3, 1)),
            (3, "3. الصيانة وغسيل الشاحنة", (0.5, 0.4, 0.2, 1)),
            (4, "4. أعطال الشاحنات", (0.8, 0.3, 0.2, 1)),
            (5, "5. أعطال السيارات الصغرى", (0.7, 0.2, 0.5, 1)),
            (6, "6. صندوق الرسائل", (0.3, 0.3, 0.7, 1)),
        ]

        for btn_id, title, color in self.buttons_config:
            btn = Button(
                text=ar(title),
                font_name=DEFAULT_FONT,
                font_size='16sp',
                background_color=color,
                color=(1, 1, 1, 1)
            )
            # ربط الزر التفاعلي بالدالة عند الضغط
            btn.bind(on_press=lambda instance, b_id=btn_id: self.on_button_click(b_id))
            grid.add_widget(btn)

        self.add_widget(grid)

    def on_button_click(self, button_number):
        """التوجيه للواجهة والخدمة عند الضغط على أزرار القائمة"""
        screens_map = {
            1: "شاشة قراءة العداد والتنبيهات الحالية (odometer_engine.py)",
            2: "شاشة التزود بالوقود وإرفاق الإيصال (fuel_engine.py)",
            3: "شاشة جدول الصيانة والغسيل (faults_maintenance_engine.py)",
            4: "شاشة بلاغات أعطال الشاحنات (faults_maintenance_engine.py)",
            5: "شاشة بلاغات أعطال السيارات (faults_maintenance_engine.py)",
            6: "صندوق الرسائل والتوجيهات (messages_notifications_engine.py)"
        }
        
        target = screens_map.get(button_number, "صفحة غير معروفة")

        # إنشاء نافذة تفاعلية حقيقية تظهر للمستخدم
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        msg_label = Label(
            text=ar(f"جاري فتح:\n{target}"),
            font_name=DEFAULT_FONT,
            font_size='15sp',
            halign='center'
        )
        content.add_widget(msg_label)

        close_btn = Button(
            text=ar("موافق / إغلاق"),
            font_name=DEFAULT_FONT,
            size_hint_y=0.4,
            background_color=(0.2, 0.7, 0.4, 1)
        )
        content.add_widget(close_btn)

        popup = Popup(
            title=ar(f"خيار رقم {button_number}"),
            title_font=DEFAULT_FONT,
            content=content,
            size_hint=(0.8, 0.45)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

# -------------------------------------------------------------
# 3. مشغل الواجهة الرئيسي
# -------------------------------------------------------------
class MainUIApp(App):
    def build(self):
        return AppMainUI()

if __name__ == "__main__":
    MainUIApp().run()