from flask import Flask, render_template, request

from .models import get_available_slots
from .parking import vehicle_entry, vehicle_exit


app = Flask(__name__)


@app.route("/")
def dashboard():
    """Display the main Parksby dashboard."""

    available_slots = get_available_slots()

    return render_template(
        "index.html",
        available_slots=available_slots,
        available_count=len(available_slots)
    )


@app.route("/entry", methods=["POST"])
def entry():
    """Handle vehicle entry."""

    plate_number = request.form.get("plate_number", "").strip().upper()
    vehicle_type = request.form.get("vehicle_type", "").strip()

    if not plate_number or not vehicle_type:
        return render_template(
            "index.html",
            available_slots=get_available_slots(),
            available_count=len(get_available_slots()),
            error="Please provide the vehicle plate number and vehicle type."
        )

    result = vehicle_entry(
        plate_number,
        vehicle_type
    )

    return render_template(
        "index.html",
        available_slots=get_available_slots(),
        available_count=len(get_available_slots()),
        entry_result=result
    )


@app.route("/exit", methods=["POST"])
def exit_vehicle():
    """Handle vehicle exit and payment."""

    identifier = request.form.get("identifier", "").strip().upper()
    payment_method = request.form.get("payment_method", "").strip()

    if not identifier or not payment_method:
        return render_template(
            "index.html",
            available_slots=get_available_slots(),
            available_count=len(get_available_slots()),
            error="Please provide the vehicle plate/ticket and payment method."
        )

    result = vehicle_exit(
        identifier,
        payment_method
    )

    return render_template(
        "index.html",
        available_slots=get_available_slots(),
        available_count=len(get_available_slots()),
        exit_result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
