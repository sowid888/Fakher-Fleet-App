-- database_setup.sql
-- Run this in phpMyAdmin

CREATE DATABASE IF NOT EXISTS aljawzi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE aljawzi_db;

CREATE TABLE IF NOT EXISTS drivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20) NOT NULL,
    driver_name VARCHAR(100) NOT NULL,
    secret_code VARCHAR(50) NOT NULL,
    vehicle_type ENUM('truck', 'car') DEFAULT 'truck',
    phone VARCHAR(20),
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_vehicle (vehicle_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS odometer_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20) NOT NULL,
    driver_name VARCHAR(100) NOT NULL,
    reading INT NOT NULL,
    reading_type ENUM('camera', 'manual') DEFAULT 'manual',
    image_path VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS fuel_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20) NOT NULL,
    driver_name VARCHAR(100) NOT NULL,
    amount_liters INT NOT NULL,
    invoice_number VARCHAR(50),
    station_name VARCHAR(100),
    image_path VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS fault_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20) NOT NULL,
    driver_name VARCHAR(100) NOT NULL,
    fault_category ENUM('electrical', 'tire_brake', 'engine', 'fridge', 'brake_system') NOT NULL,
    fault_description TEXT NOT NULL,
    status ENUM('pending', 'in_progress', 'resolved') DEFAULT 'pending',
    image_path VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20),
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    message_type ENUM('alert', 'maintenance', 'info', 'general') DEFAULT 'general',
    is_broadcast BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS driver_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    driver_vehicle VARCHAR(20) NOT NULL,
    message_id INT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample data
INSERT INTO drivers (vehicle_number, driver_name, secret_code, vehicle_type, phone, status) VALUES
('101', 'أحمد محمد', '7845', 'truck', '0500111111', 'active'),
('205', 'خالد عبدالله', '9231', 'truck', '0500222222', 'active'),
('301', 'سعد Ibrahim', '4567', 'car', '0500333333', 'active'),
('102', 'محمد سالم', '1111', 'truck', '0500444444', 'active');

INSERT INTO messages (vehicle_number, title, body, message_type, is_broadcast) VALUES
(NULL, 'تذكير بقراءة العداد', 'يجب إرسال قراءة عداد المسافة خلال 24 ساعة القادمة.', 'alert', TRUE),
(NULL, 'موعد صيانة دورية', 'تبقى 500 كم على تغيير زيت المحرك.', 'maintenance', TRUE),
(NULL, 'تعميم من الإدارة', 'تم تحديث سياسة التعبئة.', 'info', TRUE);
