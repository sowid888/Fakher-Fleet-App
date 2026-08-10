# -*- coding: utf-8 -*-
import os
import tkinter as tk
import sqlite3

class DetectiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 كشاف قاعدة البيانات المفقودة - المهندس جمال سويد")
        self.root.geometry("800x600")
        self.root.configure(bg="#0f172a")
        
        self.txt = tk.Text(root, bg="#1e293b", fg="#4ade80", font=("Arial", 12))
        self.txt.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.start_search()

    def start_search(self):
        self.txt.insert(tk.END, "🔍 جاري البحث في القرص (D) و (C) عن ملفات قواعد البيانات...\n\n")
        # البحث في الأقراص الرئيسية
        for drive in ['D:\\', 'C:\\']:
            if os.path.exists(drive):
                self.txt.insert(tk.END, f"🔎 البحث في: {drive}\n")
                for root_dir, dirs, files in os.walk(drive):
                    for file in files:
                        if file.endswith(".db"):
                            full_path = os.path.join(root_dir, file)
                            self.check_file(full_path)

    def check_file(self, path):
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if tables:
                self.txt.insert(tk.END, f"✅ تم العثور على قاعدة بيانات: {path}\n")
                self.txt.insert(tk.END, f"   الجداول: {tables}\n\n")
            conn.close()
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    DetectiveApp(root)
    root.mainloop()