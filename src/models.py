from datetime import datetime
from .database import get_db_connection


def get_available_slots():
    """Return all currently available parking slots."""
    db = get_db_connection()

    slots = db.execute("""
        SELECT slot_id, slot_number, status
        FROM parking_slots
        WHERE status = 'AVAILABLE'
        ORDER BY slot_id
    """).fetchall()

    db.close()
    return slots


def get_active_vehicle(plate_number):
    """Find an active parking record for a vehicle."""
    db = get_db_connection()

    vehicle = db.execute("""
        SELECT
            pr.record_id,
            pr.ticket_id,
            v.plate_number,
            ps.slot_number,
            pr.entry_time,
            pr.status
        FROM parking_records pr
        JOIN vehicles v ON pr.vehicle_id = v.vehicle_id
        JOIN parking_slots ps ON pr.slot_id = ps.slot_id
        WHERE v.plate_number = ?
          AND pr.status = 'PARKED'
    """, (plate_number,)).fetchone()

    db.close()
    return vehicle


def create_vehicle(plate_number, vehicle_type):
    """Create a vehicle record if it does not already exist."""
    db = get_db_connection()

    existing = db.execute("""
        SELECT vehicle_id
        FROM vehicles
        WHERE plate_number = ?
    """, (plate_number,)).fetchone()

    if existing:
        db.close()
        return existing["vehicle_id"]

    cursor = db.execute("""
        INSERT INTO vehicles (plate_number, vehicle_type)
        VALUES (?, ?)
    """, (plate_number, vehicle_type))

    db.commit()
    vehicle_id = cursor.lastrowid

    db.close()
    return vehicle_id


def create_parking_record(ticket_id, vehicle_id, slot_id):
    """Create a new active parking record."""
    db = get_db_connection()

    cursor = db.execute("""
        INSERT INTO parking_records
        (ticket_id, vehicle_id, slot_id, entry_time, status)
        VALUES (?, ?, ?, ?, 'PARKED')
    """, (
        ticket_id,
        vehicle_id,
        slot_id,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    db.commit()
    record_id = cursor.lastrowid

    db.close()
    return record_id


def occupy_slot(slot_id):
    """Mark a parking slot as occupied."""
    db = get_db_connection()

    db.execute("""
        UPDATE parking_slots
        SET status = 'OCCUPIED'
        WHERE slot_id = ?
    """, (slot_id,))

    db.commit()
    db.close()


def get_parking_record(identifier):
    """Find an active parking record using plate number or ticket ID."""
    db = get_db_connection()

    record = db.execute("""
        SELECT
            pr.record_id,
            pr.ticket_id,
            v.vehicle_id,
            v.plate_number,
            ps.slot_id,
            ps.slot_number,
            pr.entry_time,
            pr.status
        FROM parking_records pr
        JOIN vehicles v ON pr.vehicle_id = v.vehicle_id
        JOIN parking_slots ps ON pr.slot_id = ps.slot_id
        WHERE (v.plate_number = ? OR pr.ticket_id = ?)
          AND pr.status = 'PARKED'
    """, (identifier, identifier)).fetchone()

    db.close()
    return record


def complete_parking_record(record_id, exit_time, duration_minutes, fee):
    """Complete a parking record after successful payment."""
    db = get_db_connection()

    db.execute("""
        UPDATE parking_records
        SET exit_time = ?,
            duration_minutes = ?,
            fee = ?,
            status = 'EXITED'
        WHERE record_id = ?
    """, (
        exit_time,
        duration_minutes,
        fee,
        record_id
    ))

    db.commit()
    db.close()


def release_slot(slot_id):
    """Mark a parking slot as available."""
    db = get_db_connection()

    db.execute("""
        UPDATE parking_slots
        SET status = 'AVAILABLE'
        WHERE slot_id = ?
    """, (slot_id,))

    db.commit()
    db.close()


def create_payment(
    record_id,
    amount,
    payment_method,
    payment_reference,
    payment_status
):
    """Record a payment in the database."""

    db = get_db_connection()

    db.execute("""
        INSERT INTO payments
        (
            record_id,
            amount,
            payment_method,
            payment_reference,
            payment_status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        record_id,
        amount,
        payment_method,
        payment_reference,
        payment_status
    ))

    db.commit()
    db.close()
