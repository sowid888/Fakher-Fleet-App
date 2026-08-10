# -*- coding: utf-8 -*-
import os
import urllib.request
import sys
import subprocess

kite_file = "pagekite.py"
PORT = "5000"
DOMAIN = "fakher2600.pagekite.me"

print("==================================================")
print("   مرحباً بك في منظومة فاخر السيادية الكبرى 2600   ")
print("==================================================")

if not os.path.exists(kite_file):
    print("🔄 جاري تهيئة النفق العالمي الفاخر للمهندس جمال... يرجى الانتظار...")
    url = "https://pagekite.net/pk/pagekite.py"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(kite_file, 'wb') as out_file:
            out_file.write(response.read())
        print("✅ تم تحميل أداة النفق بنجاح!")
    except Exception as e:
        print(f"❌ تعذر تحميل الأداة: {e}")
        sys.exit()

print(f"🚀 انطلق النفق بنجاح! جاري فتح المنفذ {PORT}...")
try:
    # فتح الملفات بشكل مستقل لضمان بقائها نشطة في الخلفية
    out_log = open("tunnel_output.log", "a")
    err_log = open("tunnel_errors.log", "a")
    
    process = subprocess.Popen([sys.executable, kite_file, PORT, DOMAIN], 
                               stdout=out_log, 
                               stderr=err_log, 
                               text=True)
    print(f"✅ النفق يعمل الآن في الخلفية بأمان.")
    print(f"🔗 الرابط العالمي الخاص بك: http://{DOMAIN}")
except Exception as e:
    print(f"❌ فشل تشغيل النفق: {e}")