import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class FakherMainDashboard2600:
    def __init__(self, root):
        self.root = root
        self.root.title("منظومة فاخر لإدارة الأسطول - الحزمة المركزية 2600 (المهندس جمال)")
        self.root.geometry("1200x800")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        self.load_modules()

    def load_modules(self):
        modules_to_load = [
            {"name": "إدارة الشاحنات", "file": "Truck_Identity"},
            {"name": "إدارة السيارات", "file": "Car_Identity"},
            {"name": "صيانة الشاحنات", "file": "Truck_Maintenance"},
        ]
        
        for mod in modules_to_load:
            try:
                module = __import__(mod["file"])
                tab_frame = ttk.Frame(self.notebook)
                self.notebook.add(tab_frame, text=mod["name"])
                
                if hasattr(module, "create_ui"):
                    module.create_ui(tab_frame)
                elif hasattr(module, "MainApplication"):
                    module.MainApplication(tab_frame)
                else:
                    lbl = tk.Label(tab_frame, text=f"تم تحميل ملف {mod['name']} بنجاح", font=("Arial", 14))
                    lbl.pack(pady=50)
                    
            except ImportError as e:
                print(f"تنبيه: لم يتم العثور على ملف {mod['file']}.py: {e}")
            except Exception as e:
                print(f"خطأ أثناء تشغيل {mod['file']}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakherMainDashboard2600(root)
    root.mainloop()