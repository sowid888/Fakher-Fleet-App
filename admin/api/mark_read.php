<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');

require_once '../config.php';

$data = json_decode(file_get_contents('php://input'), true);
$vehicle = $data['vehicle'] ?? '';
$message_id = $data['message_id'] ?? 0;

if (empty($vehicle) || $message_id <= 0) {
    echo json_encode(['success' => false, 'message' => 'بيانات ناقصة']);
    exit;
}

$stmt = $pdo->prepare("INSERT INTO driver_messages (driver_vehicle, message_id, is_read, read_at) VALUES (?, ?, TRUE, NOW()) ON DUPLICATE KEY UPDATE is_read = TRUE, read_at = NOW()");
$stmt->execute([$vehicle, $message_id]);

echo json_encode(['success' => true, 'message' => 'تم التحديث']);
?>
