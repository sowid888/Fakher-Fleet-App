import customtkinter as ctk
import subprocess
import os
import sys

# إعدادات المظهر
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FakherMasterDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("منظومة فاخر 2600 - مركز القيادة الموحد")
        self.geometry("1100x700")

        # العنوان الرئيسي
        self.label = ctk.CTkLabel(self, text="مركز القيادة السيادي لأسطول فاخر 2600", font=("Roboto", 28, "bold"))
        self.label.pack(pady=20)

        # الإطار الرئيسي للأزرار (شبكة)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # قائمة الأدوات مع التصنيف (الاسم، الملف، النوع: 'truck' أو 'car' أو 'shared')
        self.tools = [
            ("هوية الشاحنات", "Fakher_Truck_Identity_2600.PY", "truck"),
            ("صيانة الشاحنات", "Truck_Maintenance_2600.py", "truck"),
            ("هوية السيارات", "Fakher_Car_Identity_2600.py", "car"),
            ("صيانة السيارات", "Car_Maintenance_2600.py", "car"),
            ("الدرع السيادي", "Fakher_Automation_Shield_2600.py", "shared"),
            ("محرك الذكاء", "Fakher_Intelligence_Comparison_2600.py", "shared"),
            ("تحليل الوقود", "Fakher_Car_Fuel_Consumption_2600.py", "shared"),
            ("محرك الطباعة", "Fakher_Print_Report_Engine_2600.py", "shared"),
            ("مركز التراخيص", "code_generator.py", "shared"),
            ("فحص الخزنة", "inspect_db.py", "shared")
        ]

        # توزيع الأزرار في 3 أعمدة
        for i, (name, script, t_type) in enumerate(self.tools):
            # تحديد اللون بناءً على النوع
            color = "#1f538d" if t_type == "truck" else "#d35400" if t_type == "car" else "#27ae60"
            
            btn = ctk.CTkButton(self.main_frame, text=name, height=80, font=("Arial", 14, "bold"),
                                fg_color=color, hover_color="#34495e",
                                command=lambda s=script: self.launch(s))
            
            # توزيع ذكي (3 أعمدة في الصف)
            btn.grid(row=i//3, column=i%3, padx=15, pady=15, sticky="nsew")

        # جعل الأعمدة متساوية في العرض
        for i in range(3):
            self.main_frame.grid_columnconfigure(i, weight=1)

    def launch(self, script_name):
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        if os.path.exists(full_path):
            subprocess.Popen([sys.executable, full_path])
        else:
            print(f"الملف {script_name} غير موجود!")

if __name__ == "__main__":
    app = FakherMasterDashboard()
    app.mainloop()