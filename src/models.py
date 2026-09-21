from datetime import datetime

from .database import get_db_connection


def get_available_slots():
    """Return all currently available parking slots."""

    db = get_db_connection()

    slots = db.execute("""
        SELECT
            slot_id,
            slot_number,
            status
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
        JOIN vehicles v
            ON pr.vehicle_id = v.vehicle_id
        JOIN parking_slots ps
            ON pr.slot_id = ps.slot_id
        WHERE v.plate_number = ?
          AND pr.status = 'PARKED'
    """, (plate_number,)).fetchone()

    db.close()

    return vehicle


def create_vehicle(plate_number, vehicle_type):
    """Create a vehicle record if it does not already exist."""

    db = get_db_connection()

    existing = db.execute("""
        SELECT
            vehicle_id
        FROM vehicles
        WHERE plate_number = ?
    """, (plate_number,)).fetchone()

    if existing:
        db.close()
        return existing["vehicle_id"]

    cursor = db.execute("""
        INSERT INTO vehicles (
            plate_number,
            vehicle_type
        )
        VALUES (?, ?)
    """, (
        plate_number,
        vehicle_type
    ))

    db.commit()

    vehicle_id = cursor.lastrowid

    db.close()

    return vehicle_id


def create_parking_record(ticket_id, vehicle_id, slot_id):
    """Create a new active parking record."""

    db = get_db_connection()

    cursor = db.execute("""
        INSERT INTO parking_records (
            ticket_id,
            vehicle_id,
            slot_id,
            entry_time,
            status
        )
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


def create_parking_slot():
    """
    Create the next available parking slot.

    Slot numbers are generated automatically:
    P01, P02, P03, ... P10, P11, P12, etc.
    """

    db = get_db_connection()

    try:
        result = db.execute(
            """
            SELECT
                MAX(
                    CAST(
                        SUBSTR(slot_number, 2)
                        AS INTEGER
                    )
                ) AS maximum_number
            FROM parking_slots
            WHERE slot_number LIKE 'P%'
            """
        ).fetchone()

        maximum_number = result["maximum_number"]

        if maximum_number is None:
            next_number = 1
        else:
            next_number = maximum_number + 1

        slot_number = f"P{next_number:02d}"

        cursor = db.execute(
            """
            INSERT INTO parking_slots
                (slot_number, status)
            VALUES (?, 'AVAILABLE')
            """,
            (slot_number,)
        )

        db.commit()

        return {
            "success": True,
            "slot_id": cursor.lastrowid,
            "slot_number": slot_number
        }

    finally:
        db.close()


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
        JOIN vehicles v
            ON pr.vehicle_id = v.vehicle_id
        JOIN parking_slots ps
            ON pr.slot_id = ps.slot_id
        WHERE (
            v.plate_number = ?
            OR pr.ticket_id = ?
        )
        AND pr.status = 'PARKED'
    """, (
        identifier,
        identifier
    )).fetchone()

    db.close()

    return record


def complete_parking_record(
    record_id,
    exit_time,
    duration_minutes,
    fee
):
    """Complete a parking record after successful payment."""

    db = get_db_connection()

    db.execute("""
        UPDATE parking_records
        SET
            exit_time = ?,
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
        INSERT INTO payments (
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


# ==========================================================
# PAYMENT & COLLECTION REPORTING
# ==========================================================

def get_payment_summary():
    """
    Return the overall collection summary.

    Only PAID transactions are included in collections.
    """

    db = get_db_connection()

    summary = db.execute("""
        SELECT
            COUNT(*) AS payment_count,
            COALESCE(SUM(amount), 0) AS total_collection,

            COALESCE(
                SUM(
                    CASE
                        WHEN payment_method = 'M-Pesa'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS mpesa_collection,

            COALESCE(
                SUM(
                    CASE
                        WHEN payment_method = 'Cash'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS cash_collection,

            COALESCE(
                SUM(
                    CASE
                        WHEN payment_method = 'Card'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS card_collection

        FROM payments
        WHERE payment_status = 'PAID'
    """).fetchone()

    db.close()

    return summary


def get_payment_history(limit=100):
    """
    Return recent successful payment transactions.

    The result includes the information needed for
    payment auditing and reconciliation.
    """

    db = get_db_connection()

    payments = db.execute("""
        SELECT
            p.payment_id,
            v.plate_number,
            pr.ticket_id,
            ps.slot_number,
            p.amount,
            p.payment_method,
            p.payment_reference,
            p.payment_status,
            p.payment_time,
            pr.entry_time,
            pr.exit_time,
            pr.duration_minutes
        FROM payments p
        JOIN parking_records pr
            ON p.record_id = pr.record_id
        JOIN vehicles v
            ON pr.vehicle_id = v.vehicle_id
        JOIN parking_slots ps
            ON pr.slot_id = ps.slot_id
        WHERE p.payment_status = 'PAID'
        ORDER BY p.payment_time DESC
        LIMIT ?
    """, (limit,)).fetchall()

    db.close()

    return payments


def get_daily_collection_summary():
    """
    Return collections grouped by payment date.

    This supports daily reconciliation and
    administrative reporting.
    """

    db = get_db_connection()

    daily_summary = db.execute("""
        SELECT
            DATE(payment_time) AS collection_date,
            COUNT(*) AS payment_count,
            COALESCE(SUM(amount), 0) AS total_collection,

            COALESCE(
                SUM(
                    CASE
                        WHEN payment_method = 'M-Pesa'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS mpesa_collection,

            COALESCE(
                SUM(
                    CASE
                        WHEN payment_method = 'Cash'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS cash_collection,

            COALESCE(
                SUM(
                    CASE
                        WHEN payment_method = 'Card'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS card_collection

        FROM payments
        WHERE payment_status = 'PAID'
        GROUP BY DATE(payment_time)
        ORDER BY collection_date DESC
    """).fetchall()

    db.close()

    return daily_summary
