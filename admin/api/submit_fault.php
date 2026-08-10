<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');

require_once '../config.php';

$data = json_decode(file_get_contents('php://input'), true);

$vehicle = $data['vehicle'] ?? '';
$driver = $data['driver'] ?? '';
$category = $data['category'] ?? '';
$description = $data['description'] ?? '';
$lat = $data['latitude'] ?? null;
$lng = $data['longitude'] ?? null;

if (empty($vehicle) || empty($driver) || empty($category) || empty($description)) {
    echo json_encode(['success' => false, 'message' => 'بيانات ناقصة']);
    exit;
}

$stmt = $pdo->prepare("INSERT INTO fault_reports (vehicle_number, driver_name, fault_category, fault_description, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)");
$stmt->execute([$vehicle, $driver, $category, $description, $lat, $lng]);

echo json_encode(['success' => true, 'message' => 'تم إرسال بلاغ العطل']);
?>
