import os
import sys
import subprocess
import time
import tkinter as tk
from tkinter import messagebox

# المسار الافتراضي للملفات في القرص D
BASE_DIR = "D:/"
SERVER_SCRIPT = os.path.join(BASE_DIR, "Fakher_Driver_Gateway_2600.py")
INTERFACE_SCRIPT = os.path.join(BASE_DIR, "Fakher_Driver_Gate_2600.py")

def launch_system():
    # 1. التحقق من وجود الملفات الأساسية في القرص D
    if not os.path.exists(SERVER_SCRIPT):
        messagebox.showerror("خطأ سيادي", f"تعذر العثور على ملف السيرفر الخلفي:\n{SERVER_SCRIPT}\nيرجى التأكد من وجوده في القرص D بنفس الاسم.")
        return
    if not os.path.exists(INTERFACE_SCRIPT):
        messagebox.showerror("خطأ سيادي", f"تعذر العثور على ملف واجهة السائقين:\n{INTERFACE_SCRIPT}\nيرجى التأكد من وجوده في القرص D بنفس الاسم.")
        return

    try:
        # 2. تشغيل السيرفر الخلفي (Gateway) بشكل صامت تماماً وبدون شاشة سوداء
        # استخدام الخيار الـمخفي لتجنب تشتيت المستخدم بالحروف المقلوبة
        if sys.platform == "win32":
            # إنشاء معايير بدء تشغيل مخفية للويندوز
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0 # 0 تعني مخفي صامت
            
            subprocess.Popen([sys.executable, SERVER_SCRIPT], startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen([sys.executable, SERVER_SCRIPT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # انتظار جزء من الثانية لتأمين قيام السيرفر وبناء قاعدة البيانات
        time.sleep(0.5)

        # 3. تشغيل واجهة السائقين الرسومية (Gate) لتظهر أمام المستخدم فوراً
        subprocess.Popen([sys.executable, INTERFACE_SCRIPT])
        
        # إغلاق نافذة المشغل تلقائياً لأن المهمة تمت بنجاح
        root.destroy()

    except Exception as e:
        messagebox.showerror("🚨 خرق في التشغيل", f"حدث خطأ أثناء إطلاق المحركات:\n{e}")

# بناء نافذة تمهيدية سريعة جداً للمشغل
root = tk.Tk()
root.withdraw() # إخفاء النافذة الرئيسية فوراً لتشغيل البوب-آب الذكي

# إطلاق المنظومة مباشرة عند النقر على الملف
launch_system()