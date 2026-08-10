<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');

require_once '../config.php';

$data = json_decode(file_get_contents('php://input'), true);

$vehicle = $data['vehicle'] ?? '';
$driver = $data['driver'] ?? '';
$reading = $data['reading'] ?? 0;
$type = $data['type'] ?? 'manual';
$lat = $data['latitude'] ?? null;
$lng = $data['longitude'] ?? null;

if (empty($vehicle) || empty($driver) || $reading <= 0) {
    echo json_encode(['success' => false, 'message' => 'بيانات ناقصة']);
    exit;
}

$stmt = $pdo->prepare("INSERT INTO odometer_readings (vehicle_number, driver_name, reading, reading_type, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)");
$stmt->execute([$vehicle, $driver, $reading, $type, $lat, $lng]);

$lastStmt = $pdo->prepare("SELECT reading FROM odometer_readings WHERE vehicle_number = ? ORDER BY created_at DESC LIMIT 2");
$lastStmt->execute([$vehicle]);
$readings = $lastStmt->fetchAll();

$alert = null;
if (count($readings) >= 2) {
    $diff = $readings[0]['reading'] - $readings[1]['reading'];
    if ($diff > 4500) {
        $alert = 'تنبيه: اقترب موعد تغيير الزيت!';
    }
}

echo json_encode([
    'success' => true,
    'message' => 'تم حفظ القراءة بنجاح',
    'alert' => $alert
]);
?>
