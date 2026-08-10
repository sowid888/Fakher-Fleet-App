<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

require_once '../config.php';

$data = json_decode(file_get_contents('php://input'), true);

$vehicle = $data['vehicle'] ?? '';
$driver = $data['driver'] ?? '';
$secret = $data['secret'] ?? '';

if (empty($vehicle) || empty($driver) || empty($secret)) {
    echo json_encode(['success' => false, 'message' => 'بيانات ناقصة']);
    exit;
}

$stmt = $pdo->prepare("SELECT * FROM drivers WHERE vehicle_number = ? AND driver_name = ? AND secret_code = ? AND status = 'active'");
$stmt->execute([$vehicle, $driver, $secret]);
$driver_data = $stmt->fetch();

if ($driver_data) {
    echo json_encode([
        'success' => true,
        'message' => 'تم التحقق بنجاح',
        'data' => [
            'vehicle_number' => $driver_data['vehicle_number'],
            'driver_name' => $driver_data['driver_name'],
            'vehicle_type' => $driver_data['vehicle_type'],
            'phone' => $driver_data['phone']
        ]
    ]);
} else {
    echo json_encode(['success' => false, 'message' => 'رقم سري غير صحيح أو السائق غير موجود']);
}
?>
