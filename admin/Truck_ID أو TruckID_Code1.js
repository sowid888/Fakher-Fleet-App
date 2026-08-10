async function handleLogin() {
    const plate = document.getElementById('txtPlate').value.trim();
    const driver = document.getElementById('txtDriver').value.trim();
    const adminId = document.getElementById('txtAdminId').value.trim();
    const pin = document.getElementById('txtPin').value.trim();
    const vehicleType = document.getElementById('vehicleTypeSelect').value;
    const errDiv = document.getElementById('loginError');

    if (!plate || !driver || !adminId || !pin) {
        errDiv.innerText = "لقد حدث خطأ في أحد الحقول أو الحقول فارغة!";
        errDiv.classList.remove('hidden');
        return;
    }

    // إرسال البيانات إلى السيرفر للتحقق من الرقم السري وتسجيل الدخول
    try {
        errDiv.classList.add('hidden');
        // يمكنك استبدال الرابط أدناه برابط السيرفر الفعلي الخاص بك
        const response = await fetch('https://your-server-domain.com/api/login.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                vehicleType: vehicleType,
                plate: plate,
                driver: driver,
                adminId: adminId,
                pin: pin
            })
        });

        const result = await response.json();

        if (result.success) {
            // إذا وافق السيرفر على الرقم السري والبيانات
            currentVehicleData.type = vehicleType;
            currentVehicleData.plate = plate;
            currentVehicleData.driver = driver;

            document.getElementById('mainTitle').innerText = `نظام الجوزي - ${vehicleType === 'TRUCK' ? 'شاحنة' : 'سيارة'} (${plate})`;
            document.getElementById('mainSubtitle').innerText = `السائق: ${driver}`;

            showSection('mainDashboard');
        } else {
            // إذا كان الرقم السري خطأ أو هناك خطأ في البيانات من السيرفر
            errDiv.innerText = result.message || "الرقم السري غير صحيح أو حدث خطأ في المطابقة!";
            errDiv.classList.remove('hidden');
        }
    } catch (error) {
        // في حال عدم توفر اتصال بالإنترنت أو خطأ في السيرفر
        errDiv.innerText = "تعذر الاتصال بسيرفر النظام. تحقق من شبكة الإنترنت.";
        errDiv.classList.remove('hidden');
    }
}