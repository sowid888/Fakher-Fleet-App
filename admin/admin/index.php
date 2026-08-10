<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>لوحة تحكم مؤسسة الجوزي</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Cairo', sans-serif; }
        body { background: #f5f0e6; }
        .header { background: linear-gradient(135deg, #3D2314, #6B4226); color: #C9A84C; padding: 20px; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .card { background: white; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .card h2 { color: #3D2314; margin-bottom: 15px; border-bottom: 2px solid #C9A84C; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: right; border-bottom: 1px solid #eee; }
        th { background: #3D2314; color: #C9A84C; }
        tr:hover { background: #f9f9f9; }
        .btn { padding: 8px 16px; border: none; border-radius: 8px; cursor: pointer; font-family: 'Cairo'; }
        .btn-primary { background: #C9A84C; color: #3D2314; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-box { background: linear-gradient(135deg, #3D2314, #6B4226); color: #C9A84C; padding: 20px; border-radius: 15px; text-align: center; }
        .stat-box h3 { font-size: 32px; margin-bottom: 5px; }
        .nav { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a { text-decoration: none; padding: 10px 20px; background: #3D2314; color: #C9A84C; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚛 مؤسسة الجوزي - لوحة التحكم</h1>
        <p>قطاع الحركة والأتمتة</p>
    </div>

    <div class="container">
        <div class="nav">
            <a href="index.php">الرئيسية</a>
            <a href="drivers.php">السائقين</a>
            <a href="readings.php">قراءات العداد</a>
            <a href="fuel.php">التعبئة</a>
            <a href="faults.php">الأعطال</a>
            <a href="messages.php">الرسائل</a>
        </div>

        <div class="stats">
            <div class="stat-box">
                <h3>4</h3>
                <p>سائق نشط</p>
            </div>
            <div class="stat-box">
                <h3>0</h3>
                <p>قراءة اليوم</p>
            </div>
            <div class="stat-box">
                <h3>0</h3>
                <p>عطل معلق</p>
            </div>
            <div class="stat-box">
                <h3>0</h3>
                <p>تعبئة اليوم</p>
            </div>
        </div>

        <div class="card">
            <h2>📊 آخر القراءات</h2>
            <table>
                <tr>
                    <th>المركبة</th>
                    <th>السائق</th>
                    <th>القراءة</th>
                    <th>النوع</th>
                    <th>التاريخ</th>
                </tr>
                <tr>
                    <td colspan="5" style="text-align: center; color: #999;">لا توجد قراءات بعد</td>
                </tr>
            </table>
        </div>

        <div class="card">
            <h2>⚠️ آبلاغات الأعطال</h2>
            <table>
                <tr>
                    <th>المركبة</th>
                    <th>السائق</th>
                    <th>العطل</th>
                    <th>الحالة</th>
                    <th>التاريخ</th>
                </tr>
                <tr>
                    <td colspan="5" style="text-align: center; color: #999;">لا توجد أعطال بعد</td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>
