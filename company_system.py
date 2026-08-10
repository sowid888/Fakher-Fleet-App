import tkinter as tk
from tkinter import messagebox, ttk
import urllib.request
import json
import threading
import time

# رابط قاعدة البيانات الخاصة بك
FIREBASE_URL = "https://algazi26-default-rtdb.firebaseio.com/"

class CompanyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام إدارة الشاحنات والرسائل - الشركة")
        self.root.geometry("600x500")

        # قسم تسجيل الشاحنات
        frame_reg = tk.LabelFrame(root, text="تسجيل/ربط شاحنة جديدة برقم السائق", padx=10, pady=10)
        frame_reg.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_reg, text="رقم/هوية الشاحنة (Truck ID):").grid(row=0, column=0, sticky="w")
        self.entry_truck = tk.Entry(frame_reg)
        self.entry_truck.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_reg, text="رقم هاتف السائق (Driver Phone):").grid(row=1, column=0, sticky="w")
        self.entry_phone = tk.Entry(frame_reg)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        btn_save = tk.Button(frame_reg, text="حفظ وربط في السيرفر", bg="#28a745", fg="white", command=self.register_truck)
        btn_save.grid(row=2, column=0, columnspan=2, pady=10)

        # قسم عرض الرسائل الواردة
        frame_msg = tk.LabelFrame(root, text="الرسائل والبيانات الواردة من السائقين", padx=10, pady=10)
        frame_msg.pack(fill="both", expand=True, padx=10, pady=5)

        self.txt_messages = tk.Text(frame_msg, state="disabled")
        self.txt_messages.pack(fill="both", expand=True)

        # بدء الاستماع للرسائل في الخلفية
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def register_truck(self):
        truck_id = self.entry_truck.get().strip()
        phone = self.entry_phone.get().strip()

        if not truck_id or not phone:
            messagebox.showerror("خطأ", "يرجى إدخال رقم الشاحنة ورقم الهاتف")
            return

        # رفع البيانات للسيرفر المباشر
        url = f"{FIREBASE_URL}registered_trucks/{phone}.json"
        data = json.dumps({"truck_id": truck_id, "phone": phone}).encode('utf-8')
        
        try:
            req = urllib.request.Request(url, data=data, method='PUT')
            with urllib.request.urlopen(req) as response:
                messagebox.showinfo("نجاح", f"تم ربط الشاحنة {truck_id} برقم الهاتف {phone} بنجاح!")
                self.entry_truck.delete(0, tk.END)
                self.entry_phone.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("خطأ في الاتصال", str(e))

    def listen_for_messages(self):
        url = f"{FIREBASE_URL}incoming_messages.json"
        last_data = ""
        while True:
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as response:
                    res = response.read().decode('utf-8')
                    if res != "null" and res != last_data:
                        last_data = res
                        messages = json.loads(res)
                        self.display_messages(messages)
            except Exception:
                pass
            time.sleep(3)

    def display_messages(self, messages):
        self.txt_messages.config(state="normal")
        selfrt(tk.END, text)
        self.txt_messages.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompanyApp(root)
    root.mainloop()