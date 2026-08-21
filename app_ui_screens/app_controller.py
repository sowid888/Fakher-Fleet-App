# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - المحرك التنفيذي التفاعلي للأندرويد
تاريخ التحديث: أغسطس 2026
"""

import sys
import os

# إضافة المسار الحالي لضمان استيراد الوحدات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase

# -------------------------------------------------------------
# 1. إعداد الخط العربي ومعالجة الاتجاهات
# -------------------------------------------------------------
# البحث عن ملف الخط العربي في المجلد المباشر للمشروع
FONT_NAME = "arial.ttf"
FONT_PATH = os.path.join(os.path.dirname(__file__), FONT_NAME)

if os.path.exists(FONT_PATH):
    LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)
    DEFAULT_FONT = "ArabicFont"
else:
    DEFAULT_FONT = "Roboto"  # خط افتراضي في حال عدم وجود الملف

def ar(text):
    """ دالة معالجة النصوص العربية وتشكيل الحروف """
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)

# -------------------------------------------------------------
# 2. الواجهة الرسومية التفاعلية لمنظومة 2600
# -------------------------------------------------------------
class FakherFleetUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        
        # الشريط العلوي الرئيسي
        header = Label(
            text=ar("منظومة فاخر 2600 - الأسطول الموحد"),
            font_size='20sp',
            font_name=DEFAULT_FONT,
            size_hint_y=0.1,
            color=(0.2, 0.7, 1, 1)
        )
        self.add_widget(header)

        # شبكة الأزرار للشاحنات والسيارات (40 مربع تفاعلي)
        grid = GridLayout(cols=4, spacing=8, size_hint_y=0.9)
        
        for i in range(1, 41):
            btn_text = ar(f"مركبة {i}")
            btn = Button(
                text=f"{btn_text}\n{i}",
                font_name=DEFAULT_FONT,
                font_size='14sp',
                background_color=(0.1, 0.4, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            # ربط الحدث عند الضغط على المربع لتنفيذ أمر حقيقي
            btn.bind(on_press=lambda instance, vehicle_num=i: self.on_vehicle_click(vehicle_num))
            grid.add_widget(btn)

        self.add_widget(grid)

    def on_vehicle_click(self, vehicle_id):
        """ الدالة التنفيذية التي تعمل فور الضغط على أي مربع """
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # نصوص وتفاصيل داخل النافذة المنبثقة
        info_label = Label(
            text=ar(f"بيانات المركبة رقم: {vehicle_id}\nالحالة: جاهزة للعمل\nالعداد: 125,400 كم"),
            font_name=DEFAULT_FONT,
            font_size='16sp',
            halign='center'
        )
        content.add_widget(info_label)

        # زر إدخال وقود / ديزل
        btn_fuel = Button(
            text=ar("⛽ تسجيل صرف ديزل"),
            font_name=DEFAULT_FONT,
            size_hint_y=0.3,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        btn_fuel.bind(on_press=lambda x: self.process_action(vehicle_id, "تسجيل وقود"))
        content.add_widget(btn_fuel)

        # زر توثيق صيانة
        btn_maint = Button(
            text=ar("🛠️ طلب صيانة عاجلة"),
            font_name=DEFAULT_FONT,
            size_hint_y=0.3,
            background_color=(0.9, 0.4, 0.2, 1)
        )
        btn_maint.bind(on_press=lambda x: self.process_action(vehicle_id, "طلب صيانة"))
        content.add_widget(btn_maint)

        # إغلاق النافذة
        popup = Popup(
            title=ar(f"إدارة المركبة {vehicle_id}"),
            title_font=DEFAULT_FONT,
            content=content,
            size_hint=(0.85, 0.6)
        )
        popup.open()

    def process_action(self, vehicle_id, action_type):
        """ تنفيذ الإجراء وتحويله للبيانات """
        print(f"تم تنفيذ إجراء ({action_type}) للمركبة {vehicle_id}")

# -------------------------------------------------------------
# 3. مشغل التطبيق الأساسي
# -------------------------------------------------------------
class FakherFleetApp(App):
    def build(self):
        return FakherFleetUI()

if __name__ == "__main__":
    FakherFleetApp().run()