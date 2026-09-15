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
