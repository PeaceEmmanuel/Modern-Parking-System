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


def generate_ticket_id():
    """Generate a unique parking ticket ID."""
    return "PK-" + uuid.uuid4().hex[:8].upper()


def calculate_fee(duration_minutes):
    """
    Calculate parking fee according to the assignment tariff.

    Up to 30 minutes       = KES 0
    More than 30 to 2 hrs  = KES 50
    More than 2 to 4 hrs   = KES 100
    More than 4 to 6 hrs   = KES 300
    More than 6 hrs        = KES 500
    """

    if duration_minutes <= 30:
        return 0

    elif duration_minutes <= 120:
        return 50

    elif duration_minutes <= 240:
        return 100

    elif duration_minutes <= 360:
        return 300

    else:
        return 500


def vehicle_entry(plate_number, vehicle_type):
    """
    Process vehicle entry.

    Checks for duplicate vehicles, finds an available
    parking slot, creates a ticket and parking record,
    and occupies the selected slot.
    """

    # Check whether the vehicle is already parked
    if get_active_vehicle(plate_number):
        return {
            "success": False,
            "message": "Vehicle is already parked."
        }

    # Check available parking slots
    slots = get_available_slots()

    if not slots:
        return {
            "success": False,
            "message": "Parking is full."
        }

    # Assign the first available slot
    slot = slots[0]

    # Create or retrieve vehicle
    vehicle_id = create_vehicle(
        plate_number,
        vehicle_type
    )

    # Generate a unique ticket
    ticket_id = generate_ticket_id()

    # Create parking record
    record_id = create_parking_record(
        ticket_id,
        vehicle_id,
        slot["slot_id"]
    )

    # Mark parking slot as occupied
    occupy_slot(slot["slot_id"])

    return {
        "success": True,
        "message": "Vehicle entry successful.",
        "record_id": record_id,
        "ticket_id": ticket_id,
        "plate_number": plate_number,
        "slot_number": slot["slot_number"],
        "entry_time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
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

    The system can later be connected to
    M-Pesa or another real payment service.
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
    """

    # Find active parking record
    record = get_parking_record(identifier)

    if not record:
        return {
            "success": False,
            "message": "Vehicle or ticket not found."
        }

    # Record exit time
    exit_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Calculate parking duration
    duration_minutes = calculate_duration(
        record["entry_time"],
        exit_time
    )

    # Calculate parking fee
    fee = calculate_fee(duration_minutes)

    # Process payment
    payment = process_payment(
        fee,
        payment_method
    )

    # Keep barrier closed if payment fails
    if not payment["success"]:
        return {
            "success": False,
            "message": "Payment unsuccessful. "
                       "Barrier remains closed.",
            "fee": fee
        }

    # Record successful payment
    create_payment(
        record["record_id"],
        fee,
        payment_method,
        payment["payment_reference"],
        "PAID"
    )

    # Complete parking record
    complete_parking_record(
        record["record_id"],
        exit_time,
        duration_minutes,
        fee
    )

    # Release the parking slot
    release_slot(record["slot_id"])

    return {
        "success": True,
        "message": "Payment successful. "
                   "Exit barrier opened.",
        "plate_number": record["plate_number"],
        "ticket_id": record["ticket_id"],
        "slot_number": record["slot_number"],
        "duration_minutes": duration_minutes,
        "fee": fee,
        "payment_reference": payment["payment_reference"],
        "payment_method": payment_method
    }
