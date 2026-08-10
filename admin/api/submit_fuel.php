<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');

require_once '../config.php';

$data = json_decode(file_get_contents('php://input'), true);

$vehicle = $data['vehicle'] ?? '';
$driver = $data['driver'] ?? '';
$amount = $data['amount'] ?? 0;
$invoice = $data['invoice'] ?? '';
$station = $data['station'] ?? '';
$lat = $data['latitude'] ?? null;
$lng = $data['longitude'] ?? null;

if (empty($vehicle) || empty($driver) || $amount <= 0) {
    echo json_encode(['success' => false, 'message' => 'بيانات ناقصة']);
    exit;
}

$stmt = $pdo->prepare("INSERT INTO fuel_records (vehicle_number, driver_name, amount_liters, invoice_number, station_name, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)");
$stmt->execute([$vehicle, $driver, $amount, $invoice, $station, $lat, $lng]);

echo json_encode(['success' => true, 'message' => 'تم حفظ بيانات التعبئة']);
?>
