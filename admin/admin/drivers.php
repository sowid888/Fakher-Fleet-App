<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>إدارة السائقين - مؤسسة الجوزي</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Cairo', sans-serif; }
        body { background: #f5f0e6; }
        .header { background: linear-gradient(135deg, #3D2314, #6B4226); color: #C9A84C; padding: 20px; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .card { background: white; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .card h2 { color: #3D2314; margin-bottom: 15px; border-bottom: 2px solid #C9A84C; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; text-align: right; border-bottom: 1px solid #eee; }
        th { background: #3D2314; color: #C9A84C; }
        .btn { padding: 8px 16px; border: none; border-radius: 8px; cursor: pointer; font-family: 'Cairo'; }
        .btn-primary { background: #C9A84C; color: #3D2314; }
        .btn-danger { background: #8B0000; color: white; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #3D2314; }
        .form-group input, .form-group select { width: 100%; padding: 10px; border: 2px solid #C9A84C; border-radius: 8px; font-family: 'Cairo'; }
        .grid { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="header">
        <h1>👨‍✈️ إدارة السائقين</h1>
        <p>مؤسسة الجوزي - قطاع الحركة والأتمتة</p>
    </div>

    <div class="container">
        <div class="grid">
            <div class="card">
                <h2>➕ إضافة سائق جديد</h2>
                <form method="POST" action="add_driver.php">
                    <div class="form-group">
                        <label>رقم المركبة</label>
                        <input type="text" name="vehicle_number" required placeholder="مثال: 101">
                    </div>
                    <div class="form-group">
                        <label>اسم السائق</label>
                        <input type="text" name="driver_name" required placeholder="أدخل الاسم">
                    </div>
                    <div class="form-group">
                        <label>الرقم السري</label>
                        <input type="text" name="secret_code" required placeholder="أدخل الرقم السري">
                    </div>
                    <div class="form-group">
                        <label>نوع المركبة</label>
                        <select name="vehicle_type">
                            <option value="truck">🚛 شاحنة</option>
                            <option value="car">🚗 سيارة</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>رقم الهاتف</label>
                        <input type="text" name="phone" placeholder="0500XXXXXX">
                    </div>
                    <button type="submit" class="btn btn-primary">💾 حفظ السائق</button>
                </form>
            </div>

            <div class="card">
                <h2>📋 قائمة السائقين</h2>
                <table>
                    <tr>
                        <th>المركبة</th>
                        <th>الاسم</th>
                        <th>الرقم السري</th>
                        <th>النوع</th>
                        <th>الحالة</th>
                    </tr>
                    <tr>
                        <td>101</td>
                        <td>أحمد محمد</td>
                        <td>7845</td>
                        <td>🚛 شاحنة</td>
                        <td>✅ نشط</td>
                    </tr>
                    <tr>
                        <td>205</td>
                        <td>خالد عبدالله</td>
                        <td>9231</td>
                        <td>🚛 شاحنة</td>
                        <td>✅ نشط</td>
                    </tr>
                    <tr>
                        <td>301</td>
                        <td>سعد Ibrahim</td>
                        <td>4567</td>
                        <td>🚗 سيارة</td>
                        <td>✅ نشط</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
