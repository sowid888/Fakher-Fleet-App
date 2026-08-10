import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class WhatsAppManager:
    def __init__(self, root):
        self.root = root
        self.root.title("إدارة الحركة - شركة الجوزي للتجارة العامة والتوكيلات")
        self.driver = None
        
        # إطار رئيسي فخم لشركة الجوزي
        self.main_frame = ttk.LabelFrame(root, text=" 💬 إعدادات وربط الواتساب المركزي (منظومة 2600) ", padding=20)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # نص توضيحي هيبة
        self.info_label = ttk.Label(
            self.main_frame, 
            text="لربط النظام برقم الواتساب السري الخاص بإدارة حركة شركة الجوزي، اضغط على زر توليد الرمز أدناه. سيفتح لك متصفحاً يحتوي على كود الـ QR، قم بمسحه بجوالك لمرة واحدة فقط.",
            font=("Arial", 11, "bold"),
            wraplength=450,
            justify="right"
        )
        self.info_label.pack(pady=10)
        
        # زر الربط السيادي
        self.btn_connect = ttk.Button(self.main_frame, text="🔗 توليد كود الـ QR للربط الفوري", command=self.start_whatsapp_thread)
        self.btn_connect.pack(pady=15)
        
        # مكان عرض حالة الاتصال
        self.status_label = ttk.Label(self.main_frame, text="حالة النظام: غير متصل ❌", foreground="red", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=5)

    def start_whatsapp_thread(self):
        # تشغيل المتصفح في خلفية منفصلة لكي لا تتجمد واجهة البرنامج
        threading.Thread(target=self.generate_qr_real, daemon=True).start()

    def generate_qr_real(self):
        self.status_label.config(text="جاري تشغيل المحرك السري وتوليد الرمز... 🔄", foreground="orange")
        self.btn_connect.config(state="disabled")
        self.root.update()
        
        try:
            # تشغيل متصفح كروم تلقائياً لفتح واتساب ويب الرسمي
            options = webdriver.ChromeOptions()
            options.add_argument("--user-data-dir=selenium_whatsapp_session") # لحفظ التسجيل لكي لا يطلب الكود مرة أخرى
            
            # تثبيت المحرك وتشغيله
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # التوجه لواتساب ويب الفعلي
            self.driver.get("https://web.whatsapp.com")
            self.status_label.config(text="حالة النظام: كود الـ QR جاهز في المتصفح، امسحه الآن بجوالك 📱", foreground="blue")
            
        except Exception as e:
            messagebox.showerror("خطأ في المنظومة", f"فشل تشغيل المحرك. تأكد من وجود متصفح جوجل كروم واتصال بالإنترنت.\nالخطأ: {str(e)}")
            self.status_label.config(text="حالة النظام: فشل الاتصال ❌", foreground="red")
            self.btn_connect.config(state="normal")

if __name__ == "__main__":
    main_window = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    app = WhatsAppManager(main_window)
    main_window.mainloop()