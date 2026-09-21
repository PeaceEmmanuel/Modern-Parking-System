-- PARKSBY DATABASE SCHEMA
-- Smart Parking Management System

PRAGMA foreign_keys = ON;

-- ==========================================
-- VEHICLES
-- ==========================================

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number VARCHAR(20) NOT NULL UNIQUE,
    vehicle_type VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- PARKING SLOTS
-- ==========================================

CREATE TABLE IF NOT EXISTS parking_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_number VARCHAR(10) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE'
        CHECK (status IN ('AVAILABLE', 'OCCUPIED'))
);


-- ==========================================
-- PARKING RECORDS
-- ==========================================

CREATE TABLE IF NOT EXISTS parking_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id VARCHAR(30) NOT NULL UNIQUE,
    vehicle_id INTEGER NOT NULL,
    slot_id INTEGER NOT NULL,
    entry_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exit_time DATETIME,
    duration_minutes INTEGER,
    fee DECIMAL(10,2),
    status VARCHAR(20) NOT NULL DEFAULT 'PARKED'
        CHECK (status IN ('PARKED', 'EXITED')),

    FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id),

    FOREIGN KEY (slot_id)
        REFERENCES parking_slots(slot_id)
);


-- ==========================================
-- PAYMENTS
-- ==========================================

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    payment_reference VARCHAR(50) NOT NULL UNIQUE,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'PENDING'
        CHECK (payment_status IN ('PENDING', 'PAID', 'FAILED')),
    payment_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (record_id)
        REFERENCES parking_records(record_id)
);


-- ==========================================
-- INITIAL PARKING SLOTS
-- ==========================================

INSERT OR IGNORE INTO parking_slots (slot_number, status)
VALUES
    ('P01', 'AVAILABLE'),
    ('P02', 'AVAILABLE'),
    ('P03', 'AVAILABLE'),
    ('P04', 'AVAILABLE'),
    ('P05', 'AVAILABLE'),
    ('P06', 'AVAILABLE'),
    ('P07', 'AVAILABLE'),
    ('P08', 'AVAILABLE'),
    ('P09', 'AVAILABLE'),
    ('P10', 'AVAILABLE');


-- ==========================================
-- PARKING RATES
-- ==========================================

CREATE TABLE IF NOT EXISTS parking_rates (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rate_name VARCHAR(100) NOT NULL,
    minimum_minutes INTEGER NOT NULL,
    maximum_minutes INTEGER,
    amount DECIMAL(10,2) NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
        CHECK (active IN (0, 1)),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- DEFAULT PARKING RATES
-- ==========================================

INSERT INTO parking_rates
    (rate_name, minimum_minutes, maximum_minutes, amount)
SELECT 'Free grace period', 0, 30, 0
WHERE NOT EXISTS (
    SELECT 1 FROM parking_rates
);

INSERT INTO parking_rates
    (rate_name, minimum_minutes, maximum_minutes, amount)
SELECT 'Up to 2 hours', 31, 120, 50
WHERE NOT EXISTS (
    SELECT 1 FROM parking_rates
    WHERE rate_name = 'Up to 2 hours'
);

INSERT INTO parking_rates
    (rate_name, minimum_minutes, maximum_minutes, amount)
SELECT 'Up to 4 hours', 121, 240, 100
WHERE NOT EXISTS (
    SELECT 1 FROM parking_rates
    WHERE rate_name = 'Up to 4 hours'
);

INSERT INTO parking_rates
    (rate_name, minimum_minutes, maximum_minutes, amount)
SELECT 'Up to 6 hours', 241, 360, 300
WHERE NOT EXISTS (
    SELECT 1 FROM parking_rates
    WHERE rate_name = 'Up to 6 hours'
);

INSERT INTO parking_rates
    (rate_name, minimum_minutes, maximum_minutes, amount)
SELECT 'Above 6 hours', 361, NULL, 500
WHERE NOT EXISTS (
    SELECT 1 FROM parking_rates
    WHERE rate_name = 'Above 6 hours'
);
