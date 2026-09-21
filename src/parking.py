import uuid
from datetime import datetime

from .models import (
    get_available_slots,
    get_active_vehicle,
    create_vehicle,
    create_parking_record,
    occupy_slot,
    get_parking_record,
    complete_parking_record,
    release_slot,
    create_payment
)

from .database import get_db_connection


def generate_ticket_id():
    """Generate a unique parking ticket ID."""
    return "PK-" + uuid.uuid4().hex[:8].upper()


def calculate_fee(duration_minutes):
    """
    Calculate the parking fee using active rates
    stored in the parking_rates database table.
    """

    if duration_minutes < 0:
        return 0

    db = get_db_connection()

    try:
        rate = db.execute(
            """
            SELECT amount
            FROM parking_rates
            WHERE active = 1
              AND minimum_minutes <= ?
              AND (
                    maximum_minutes IS NULL
                    OR maximum_minutes >= ?
                  )
            ORDER BY minimum_minutes DESC
            LIMIT 1
            """,
            (duration_minutes, duration_minutes)
        ).fetchone()

        if rate:
            return float(rate["amount"])

        return 0

    finally:
        db.close()


def get_parking_rates():
    """Return all active parking rates."""

    db = get_db_connection()

    try:
        rates = db.execute(
            """
            SELECT
                rate_id,
                rate_name,
                minimum_minutes,
                maximum_minutes,
                amount,
                active,
                created_at,
                updated_at
            FROM parking_rates
            WHERE active = 1
            ORDER BY minimum_minutes ASC
            """
        ).fetchall()

        return rates

    finally:
        db.close()


def vehicle_entry(plate_number, vehicle_type):
    """
    Process vehicle entry.

    Checks for duplicate vehicles, finds an available
    parking slot, creates a ticket and parking record,
    and occupies the selected slot.
    """

    if get_active_vehicle(plate_number):
        return {
            "success": False,
            "message": "Vehicle is already parked."
        }

    slots = get_available_slots()

    if not slots:
        return {
            "success": False,
            "message": "Parking is full."
        }

    slot = slots[0]

    vehicle_id = create_vehicle(
        plate_number,
        vehicle_type
    )

    ticket_id = generate_ticket_id()

    record_id = create_parking_record(
        ticket_id,
        vehicle_id,
        slot["slot_id"]
    )

    occupy_slot(slot["slot_id"])

    entry_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {
        "success": True,
        "message": "Vehicle entry successful.",
        "record_id": record_id,
        "ticket_id": ticket_id,
        "plate_number": plate_number,
        "slot_number": slot["slot_number"],
        "entry_time": entry_time
    }


def calculate_duration(entry_time, exit_time):
    """Calculate parking duration in minutes."""

    entry = datetime.strptime(
        entry_time,
        "%Y-%m-%d %H:%M:%S"
    )

    exit = datetime.strptime(
        exit_time,
        "%Y-%m-%d %H:%M:%S"
    )

    duration = exit - entry

    return max(
        0,
        int(duration.total_seconds() / 60)
    )


def process_payment(amount, payment_method):
    """
    Simulate payment processing.

    Supported methods:
    - M-Pesa
    - Card
    - Cash
    """

    if amount < 0:
        return {
            "success": False,
            "message": "Invalid payment amount."
        }

    if not payment_method:
        return {
            "success": False,
            "message": "Payment method is required."
        }

    payment_method = payment_method.strip()

    allowed_methods = {
        "M-Pesa",
        "Card",
        "Cash"
    }

    if payment_method not in allowed_methods:
        return {
            "success": False,
            "message": (
                "Invalid payment method. "
                "Use M-Pesa, Card, or Cash."
            )
        }

    payment_reference = (
        "PAY-" + uuid.uuid4().hex[:8].upper()
    )

    return {
        "success": True,
        "payment_reference": payment_reference,
        "payment_method": payment_method,
        "amount": amount
    }


def vehicle_exit(identifier, payment_method):
    """
    Process vehicle exit.

    Payment must succeed before the parking record
    and parking slot are updated.

    The exit barrier opens only after successful payment.
    """

    record = get_parking_record(identifier)

    if not record:
        return {
            "success": False,
            "message": "Vehicle or ticket not found."
        }

    exit_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    duration_minutes = calculate_duration(
        record["entry_time"],
        exit_time
    )

    fee = calculate_fee(duration_minutes)

    payment = process_payment(
        fee,
        payment_method
    )

    if not payment["success"]:
        return {
            "success": False,
            "message": (
                "Payment unsuccessful. "
                "Barrier remains closed."
            ),
            "fee": fee
        }

    create_payment(
        record["record_id"],
        fee,
        payment_method,
        payment["payment_reference"],
        "PAID"
    )

    complete_parking_record(
        record["record_id"],
        exit_time,
        duration_minutes,
        fee
    )

    release_slot(record["slot_id"])

    return {
        "success": True,
        "message": (
            "Payment successful. "
            "Exit barrier opened."
        ),
        "plate_number": record["plate_number"],
        "ticket_id": record["ticket_id"],
        "slot_number": record["slot_number"],
        "duration_minutes": duration_minutes,
        "fee": fee,
        "payment_reference": payment["payment_reference"],
        "payment_method": payment_method
    }
