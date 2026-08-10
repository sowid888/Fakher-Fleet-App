<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');

require_once '../config.php';

$data = json_decode(file_get_contents('php://input'), true);
$vehicle = $data['vehicle'] ?? '';

if (empty($vehicle)) {
    echo json_encode(['success' => false, 'message' => 'رقم المركبة مطلوب']);
    exit;
}

$stmt = $pdo->prepare("
    SELECT m.*, dm.is_read, dm.read_at 
    FROM messages m 
    LEFT JOIN driver_messages dm ON m.id = dm.message_id AND dm.driver_vehicle = ?
    WHERE m.is_broadcast = TRUE OR m.vehicle_number = ?
    ORDER BY m.created_at DESC
");
$stmt->execute([$vehicle, $vehicle]);
$messages = $stmt->fetchAll();

echo json_encode(['success' => true, 'messages' => $messages]);
?>
