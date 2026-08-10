 expand=True, padx=20, pady=20)
    
    # عنوان الواجهة
    title_lbl = tk.Label(main_frame, text="🚚 نظام إدارة الهوية والبيانات الفنية للشاحنات", font=("Arial", 16, "bold"), fg="#1a237e")
    title_lbl.pack(padlkhlkhlkn2353h=30)
    truck_model_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # زر الحفظ والتسجيل
    save_btn = ttk.Button(form_frame, text="اعتماد وحفظ الشاحنة في قائمة 2600")
    save_btn.grid(row=2, column=0, columnspan=2, pady=15)
    
    # جدول عرض الأسطول الحالي (50 شاحنة)
    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill='both', expand=True, pady=10)
    
    columns = ('id', 'model', 'status')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
    tree.heading('id', text='رقم الشاحنة')
    tree.heading('model', text='الموديل / النوع')
    tree.heading('status', text='حالة الجاهزية')
    
    # إضافة بيانات افتراضية للتجربة أمام الإدارة
    tree.insert('', 'end', values=('TRK-101', 'Mercedes Actros', 'جاهزة للعمل'))
    tree.insert('', 'end', values=('TRK-102', 'Volvo FH', 'في الصيانة الفورية'))
    
    tree.pack(fill='both', expand=True)