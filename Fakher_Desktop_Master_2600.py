# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - واجهة الـ 40 مفتاحاً المكتملة الشاملة
المشرف الفني العام: المهندس جمال سويد (أبا عبد الله)
تاريخ الإصدار: 2026
الوظيفة: واجهة تنفيذية رسمية بـ 40 مفتاحاً موحداً، خطوط مكبرة، وكافة الأقسام المستعادة.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, colorchooser
import sqlite3
import os
import subprocess
import sys
import json
from PIL import Image, ImageTk

BASE_DIR = "D:/" if os.path.exists("D:/") else "C:/Fakher_System"
DB_PATH = os.path.join(BASE_DIR, "Fakher_Central_Database_2600.db")
CONFIG_PATH = os.path.join(BASE_DIR, "Fakher_40_Keys_LargeFont.json")

class HDKeyButtonLarge(tk.Frame):
    """زر بتنسيق خط مكبر عالي الوضوح والنقاوة لشبكة الـ 40 مفتاح"""
    def __init__(self, parent, btn_data, click_cmd, right_click_cmd, theme_colors, **kwargs):
        super().__init__(
            parent, 
            bg=theme_colors.get("btn_border", "#d4af37"), 
            bd=1, 
            relief="solid", 
            cursor="hand2", 
            **kwargs
        )
        self.btn_data = btn_data
        self.click_cmd = click_cmd
        self.right_click_cmd = right_click_cmd
        self.theme_colors = theme_colors

        self.inner = tk.Frame(self, bg=theme_colors.get("btn_bg", "#1b4332"))
        self.inner.pack(fill="both", expand=True, padx=1, pady=1)

        self.lbl = tk.Label(
            self.inner, 
            text=btn_data["title"], 
            font=("Segoe UI", 13, "bold"), 
            fg=theme_colors.get("btn_fg", "#ffffff"), 
            bg=theme_colors.get("btn_bg", "#1b4332"),
            wraplength=150,
            justify="center"
        )
        self.lbl.pack(expand=True, fill="both", padx=2, pady=2)

        for widget in (self, self.inner, self.lbl):
            widget.bind("<Enter>", self._on_hover)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", lambda e: self.click_cmd(self.btn_data))
            widget.bind("<Button-3>", lambda e: self.right_click_cmd(self.btn_data))

    def _on_hover(self, e):
        hover_col = self.theme_colors.get("btn_hover", "#2d6a4f")
        self.inner.configure(bg=hover_col)
        self.lbl.configure(bg=hover_col)

    def _on_leave(self, e):
        base_col = self.theme_colors.get("btn_bg", "#1b4332")
        self.inner.configure(bg=base_col)
        self.lbl.configure(bg=base_col)

class Fakher40CompleteEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ منظومة فاخر السيادية 2600 — واجهة الـ 40 مفتاحاً (الخط المكبر)")
        self.root.geometry("1400x900")

        self.running_processes = {}
        self.bg_photo = None

        self.settings = {
            "bg_type": "color",
            "bg_color": "#4a0e17",
            "bg_image_path": "",
            "theme_colors": {
                "header_bg": "#2b080d",
                "header_fg": "#ffea00",
                "btn_bg": "#1b4332",
                "btn_fg": "#ffffff",
                "btn_border": "#d4af37",
                "btn_hover": "#2d6a4f"
            },
            "buttons": self.generate_complete_40_buttons()
        }

        try:
            self.root.state('zoomed')
        except:
            pass

        self.init_master_db()
        self.load_settings()
        self.build_40_grid_ui()

    def generate_complete_40_buttons(self):
        defaults = [
            {"id": 1, "title": "🚚 هوية الشاحنات\n(100 شاحنة)", "path": "", "type": "script"},
            {"id": 2, "title": "🚗 هوية السيارات\n(100 سيارة)", "path": "", "type": "script"},
            {"id": 3, "title": "⛽ وقود الشاحنات", "path": "", "type": "script"},
            {"id": 4, "title": "⛽ وقود السيارات", "path": "", "type": "script"},
            {"id": 5, "title": "🛠️ صيانة الشاحنات", "path": "", "type": "script"},
            {"id": 6, "title": "🛠️ صيانة السيارات", "path": "", "type": "script"},
            {"id": 7, "title": "📡 واجهة البلاغات الحية", "path": "", "type": "tracking"},
            {"id": 8, "title": "📩 رسائل وتنبيهات النظام", "path": "", "type": "script"},
            {"id": 9, "title": "🛞 فحص وتتبع الإطارات", "path": "", "type": "script"},
            {"id": 10, "title": "🚛 نظافة وجدولة الشاحنات", "path": "", "type": "script"},
            {"id": 11, "title": "🤖 مستشار الذكاء الاصطناعي", "path": "", "type": "script"},
            {"id": 12, "title": "⚙️ خادم الربط السيادي", "path": "", "type": "script"},
            {"id": 13, "title": "📊 التقارير المالية والإدارية", "path": "", "type": "script"}
        ]
        
        for i in range(14, 41):
            defaults.append({
                "id": i,
                "title": f"➕ مفتاح مخصص {i}",
                "path": "",
                "type": "script"
            })
        return defaults

    def init_master_db(self):
        try:
            if not os.path.exists(BASE_DIR):
                os.makedirs(BASE_DIR)
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Drivers_Online_Reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial_num TEXT,
                    km_reading TEXT,
                    report_text TEXT,
                    status TEXT DEFAULT 'قيد المراجعة',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error DB: {e}")

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "buttons" in data and len(data["buttons"]) == 40:
                        self.settings.update(data)
            except Exception as e:
                print(f"Error loading: {e}")

    def save_settings(self):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving: {e}")

    def build_40_grid_ui(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.root.configure(bg=self.settings["bg_color"])

        self.bg_container = tk.Frame(self.root, bg=self.settings["bg_color"])
        self.bg_container.pack(fill="both", expand=True)

        if self.settings["bg_type"] == "image" and os.path.exists(self.settings.get("bg_image_path", "")):
            try:
                sw = self.root.winfo_screenwidth()
                sh = self.root.winfo_screenheight()
                img = Image.open(self.settings["bg_image_path"]).resize((sw, sh), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(img)
                bg_lbl = tk.Label(self.bg_container, image=self.bg_photo)
                bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"Error image: {e}")

        theme = self.settings["theme_colors"]
        header = tk.Frame(self.bg_container, bg=theme["header_bg"], height=65, bd=1, relief="solid")
        header.pack(fill="x", side="top", padx=15, pady=8)

        btn_gear = tk.Button(
            header,
            text="⚙️ لوحة الضبط وتسمية المفاتيح",
            font=("Segoe UI", 11, "bold"),
            bg="#d4af37",
            fg="#2b080d",
            activebackground="#b38f28",
            activeforeground="#2b080d",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=6,
            command=self.open_settings_panel
        )
        btn_gear.pack(side="left", padx=15, pady=8)

        lbl_title = tk.Label(
            header, 
            text="🛡️ منظومة فاخر السيادية 2600 — لوحة الـ 40 مفتاحاً", 
            font=("Segoe UI", 16, "bold"), 
            bg=theme["header_bg"], 
            fg=theme["header_fg"]
        )
        lbl_title.pack(side="right", padx=15, pady=8)

        lbl_eng = tk.Label(
            header, 
            text="👨‍💻 م. جمال سويد (أبا عبد الله)", 
            font=("Segoe UI", 12, "bold"), 
            bg=theme["header_bg"], 
            fg="#52b788"
        )
        lbl_eng.pack(side="right", padx=10, pady=8)

        grid_panel = tk.Frame(self.bg_container, bg="")
        grid_panel.pack(fill="both", expand=True, padx=10, pady=5)

        cols = 8
        rows = 5

        for c in range(cols):
            grid_panel.grid_columnconfigure(c, weight=1, uniform="col_40")
        for r in range(rows):
            grid_panel.grid_rowconfigure(r, weight=1, uniform="row_40")

        for index, btn_data in enumerate(self.settings["buttons"][:40]):
            r = index // cols
            c = index % cols

            btn_card = HDKeyButtonLarge(
                grid_panel,
                btn_data=btn_data,
                click_cmd=self.on_button_click,
                right_click_cmd=self.configure_single_button,
                theme_colors=theme
            )
            btn_card.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

    def open_settings_panel(self):
        panel = tk.Toplevel(self.root)
        panel.title("⚙️ لوحة الضبط الشاملة وتسمية المفاتيح - المهندس جمال سويد")
        panel.geometry("580x620")
        panel.configure(bg="#2b080d")
        panel.attributes('-topmost', True)

        tk.Label(panel, text="⚙️ مركز التحكم بالتصميم وتسمية المفاتيح الـ 40", font=("Segoe UI", 13, "bold"), fg="#ffea00", bg="#2b080d").pack(pady=12)

        notebook = ttk.Notebook(panel)
        notebook.pack(fill="both", expand=True, padx=12, pady=8)

        tab_rename = tk.Frame(notebook, bg="#4a0e17", padx=15, pady=15)
        notebook.add(tab_rename, text="✏️ إعادة تسمية المفاتيح")

        tk.Label(tab_rename, text="اختر رقم المفتاح للتعديل مباشرة:", font=("Segoe UI", 10, "bold"), fg="white", bg="#4a0e17").pack(anchor="w", pady=5)

        combo_var = tk.StringVar()
        key_list = [f"مفتاح {b['id']}: {b['title'].replace('\n', ' ')}" for b in self.settings["buttons"]]
        combo_keys = ttk.Combobox(tab_rename, textvariable=combo_var, values=key_list, state="readonly", font=("Segoe UI", 10), width=45)
        combo_keys.pack(fill="x", pady=8)
        if key_list:
            combo_keys.current(0)

        def apply_quick_rename():
            idx = combo_keys.current()
            if idx >= 0:
                target_btn = self.settings["buttons"][idx]
                new_title = simpledialog.askstring("تعديل الاسم", f"أدخل الاسم الجديد للمفتاح رقم {target_btn['id']}:", initialvalue=target_btn["title"])
                if new_title:
                    target_btn["title"] = new_title
                    self.save_settings()
                    self.build_40_grid_ui()
                    messagebox.showinfo("تم التعديل", "تم تحديث اسم المفتاح فوراً على الواجهة!")

        def apply_quick_repath():
            idx = combo_keys.current()
            if idx >= 0:
                target_btn = self.settings["buttons"][idx]
                selected = filedialog.askopenfilename(title="اختر ملف بايثون (.py)", filetypes=[("Python Files", "*.py")])
                if selected:
                    target_btn["path"] = selected
                    self.save_settings()
                    messagebox.showinfo("تم الربط", "تم ربط المفتاح بالملف البرمجي بنجاح!")

        tk.Button(tab_rename, text="✏️ تعديل اسم المفتاح المحدد", font=("Segoe UI", 10, "bold"), bg="#1b4332", fg="white", bd=0, padx=10, pady=8, command=apply_quick_rename).pack(fill="x", pady=6)
        tk.Button(tab_rename, text="🔗 ربط المفتاح بملف كود (.py)", font=("Segoe UI", 10, "bold"), bg="#d4af37", fg="#2b080d", bd=0, padx=10, pady=8, command=apply_quick_repath).pack(fill="x", pady=6)

        tab_bg = tk.Frame(notebook, bg="#4a0e17", padx=15, pady=15)
        notebook.add(tab_bg, text="🖼️ الخلفية والألوان")

        def choose_bg_image():
            path = filedialog.askopenfilename(
                title="اختر صورة خلفية من الاستوديو",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")]
            )
            if path:
                self.settings["bg_type"] = "image"
                self.settings["bg_image_path"] = path
                self.save_settings()
                self.build_40_grid_ui()

        def set_bg_color():
            color = colorchooser.askcolor(title="اختر لون الخلفية")[1]
            if color:
                self.settings["bg_type"] = "color"
                self.settings["bg_color"] = color
                self.save_settings()
                self.build_40_grid_ui()

        tk.Button(tab_bg, text="🖼️ اختيار صورة من الاستوديو كخلفية", font=("Segoe UI", 10, "bold"), bg="#d4af37", fg="#2b080d", bd=0, padx=10, pady=6, command=choose_bg_image).pack(fill="x", pady=5)
        tk.Button(tab_bg, text="🎨 اختيار لون خلفية الشاشة", font=("Segoe UI", 10, "bold"), bg="#2b080d", fg="white", bd=0, padx=10, pady=6, command=set_bg_color).pack(fill="x", pady=5)

    def on_button_click(self, btn_data):
        if btn_data.get("type") == "tracking":
            self.open_tracking_window()
            return

        file_path = btn_data.get("path", "")
        if not file_path or not os.path.exists(file_path):
            messagebox.showinfo(
                "مفتاح شاغر", 
                f"المفتاح [{btn_data['title'].replace('\n', ' ')}] جاهز للربط.\nاختر ملف بايثون (.py) المخصص له."
            )
            selected = filedialog.askopenfilename(
                title=f"اختر ملف الكود لـ ({btn_data['title']})",
                filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
            )
            if selected:
                btn_data["path"] = selected
                self.save_settings()
                file_path = selected
            else:
                return

        if file_path in self.running_processes:
            proc = self.running_processes[file_path]
            if proc.poll() is None:
                messagebox.showwarning("تنبيه", "هذا القسم مفتوح بالفعل على جهازك!")
                return

        try:
            proc = subprocess.Popen([sys.executable, file_path])
            self.running_processes[file_path] = proc
        except Exception as e:
            messagebox.showerror("خطأ تشغيل", f"فشل تشغيل الملف:\n{str(e)}")

    def configure_single_button(self, btn_data):
        menu = tk.Menu(self.root, tearoff=0, font=("Segoe UI", 10))
        
        def rename():
            new_name = simpledialog.askstring("تعديل الاسم", "أدخل الاسم الجديد للمفتاح:", initialvalue=btn_data["title"])
            if new_name:
                btn_data["title"] = new_name
                self.save_settings()
                self.build_40_grid_ui()

        def repath():
            selected = filedialog.askopenfilename(title="اختر ملف بايثون المخصص", filetypes=[("Python Files", "*.py")])
            if selected:
                btn_data["path"] = selected
                self.save_settings()
                messagebox.showinfo("نجاح", "تم توجيه المفتاح بنجاح!")

        menu.add_command(label="✏️ تعديل اسم المفتاح", command=rename)
        menu.add_command(label="🔗 ربط/تغيير مسار الكود", command=repath)
        
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def open_tracking_window(self):
        win = tk.Toplevel(self.root)
        win.title("📡 مركز متابعة بلاغات وقراءات السائقين الحية")
        win.geometry("1000x550")
        win.configure(bg="#2b080d")

        header = tk.Frame(win, bg="#4a0e17", pady=10)
        header.pack(fill="x")
        tk.Label(header, text="📡 شاشة الاستقبال المباشر لبلاغات وقراءات العدادات", font=("Segoe UI", 13, "bold"), bg="#4a0e17", fg="#ffea00").pack()

        grid_frame = tk.Frame(win, bg="#2b080d", padx=10, pady=10)
        grid_frame.pack(fill="both", expand=True)

        cols = ("ID", "رقم السائق / الكود", "عداد KM", "تفاصيل البلاغ / القراءة", "الوقت والتاريخ", "الحالة")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1b4332", foreground="white", fieldbackground="#1b4332", rowheight=28)
        style.configure("Treeview.Heading", background="#2b080d", foreground="#ffea00", font=("Segoe UI", 11, "bold"))

        tree = ttk.Treeview(grid_frame, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=130)

        tree.pack(fill="both", expand=True)

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, serial_num, km_reading, report_text, created_at, status FROM Drivers_Online_Reports ORDER BY id DESC")
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                tree.insert("", "end", values=row)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Fakher40CompleteEngine(root)
    root.mainloop()