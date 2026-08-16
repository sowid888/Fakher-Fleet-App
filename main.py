# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - واجهة الـ 40 مفتاحاً للأندرويد (Kivy)
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
تاريخ الإصدار: 2026
"""

import os
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle

class FakherFleetAndroidApp(App):
    def build(self):
        self.title = "🛡️ منظومة فاخر السيادية 2600"
        
        # المسار الآمن لحفظ الإعدادات على نظام الأندرويد
        self.config_path = os.path.join(App.get_running_app().user_data_dir, "Fakher_40_Keys.json")
        self.buttons_data = self.load_or_create_settings()

        # التخطيط الرئيسي للتطبيق
        main_layout = BoxLayout(orientation='vertical', spacing=5, padding=5)

        # شريط العنوان العلوي (Header)
        header = BoxLayout(size_hint_y=0.1, padding=5)
        with header.canvas.before:
            Color(0.17, 0.03, 0.05, 1) # اللون العنابي السيادي
            self.rect_header = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(
            text="🛡️ منظومة فاخر السيادية 2600 — أندرويد\n👨‍💻 م. جمال سويد (أبا عبد الله)",
            font_size='16sp',
            bold=True,
            color=(1, 0.92, 0, 1), # اللون الذهبي
            halign='center'
        )
        header.add_widget(title_label)
        main_layout.add_widget(header)

        # شبكة الـ 40 مفتاحاً مع إمكانية التمرير للأسفل
        scroll = ScrollView(size_hint=(1, 0.9))
        grid = GridLayout(cols=4, spacing=8, size_hint_y=None, padding=5)
        grid.bind(minimum_height=grid.setter('height'))

        for btn_info in self.buttons_data:
            btn = Button(
                text=btn_info["title"],
                font_size='11sp',
                bold=True,
                background_normal='',
                background_color=(0.1, 0.26, 0.2, 1), # اللون الأخضر الزيتي
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=110,
                halign='center',
                valign='middle'
            )
            btn.bind(size=btn.setter('text_size'))
            btn.bind(on_release=lambda instance, b=btn_info: self.on_key_click(b))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        return main_layout

    def _update_rect(self, instance, value):
        self.rect_header.pos = instance.pos
        self.rect_header.size = instance.size

    def generate_default_40_buttons(self):
        defaults = [
            {"id": 1, "title": "🚚 هوية الشاحنات\n(100 شاحنة)"},
            {"id": 2, "title": "🚗 هوية السيارات\n(100 سيارة)"},
            {"id": 3, "title": "⛽ وقود الشاحنات"},
            {"id": 4, "title": "⛽ وقود السيارات"},
            {"id": 5, "title": "🛠️ صيانة الشاحنات"},
            {"id": 6, "title": "🛠️ صيانة السيارات"},
            {"id": 7, "title": "📡 البلاغات الحية"},
            {"id": 8, "title": "📩 التنبيهات"},
            {"id": 9, "title": "🛞 فحص الإطارات"},
            {"id": 10, "title": "🚛 نظافة الشاحنات"},
            {"id": 11, "title": "🤖 مستشار AI"},
            {"id": 12, "title": "⚙️ خادم الربط"},
            {"id": 13, "title": "📊 التقارير المالية"}
        ]
        for i in range(14, 41):
            defaults.append({"id": i, "title": f"➕ مفتاح {i}"})
        return defaults

    def load_or_create_settings(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        defaults = self.generate_default_40_buttons()
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(defaults, f, ensure_ascii=False, indent=4)
        except Exception:
            pass
        return defaults

    def on_key_click(self, btn_info):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        lbl = Label(
            text=f"تم الضغط على:\n{btn_info['title']}\n\nالقسم جاهز للربط بقاعدة البيانات أو خادم Firebase.",
            halign='center'
        )
        close_btn = Button(
            text="إغلاق",
            size_hint_y=0.3,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        
        content.add_widget(lbl)
        content.add_widget(close_btn)

        popup = Popup(
            title=f"مفتاح رقم {btn_info['id']}",
            content=content,
            size_hint=(0.85, 0.45)
        )
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

if __name__ == "__main__":
    FakherFleetAndroidApp().run()
