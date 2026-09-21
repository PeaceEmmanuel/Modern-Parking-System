from flask import Flask, render_template, request, redirect, url_for

from .models import (
    get_available_slots,
    get_payment_summary,
    get_payment_history,
    get_daily_collection_summary
)

from .parking import (
    vehicle_entry,
    vehicle_exit,
    get_parking_rates
)

from .database import get_db_connection


app = Flask(__name__)


def render_page(template="index.html", **kwargs):
    """Render a Parksby page with the data required by that page."""

    available_slots = get_available_slots()
    parking_rates = get_parking_rates()

    return render_template(
        template,
        available_slots=available_slots,
        available_count=len(available_slots),
        parking_rates=parking_rates,
        **kwargs
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/")
def dashboard():
    """Main operational parking dashboard."""

    return render_page(
        active_tab="dashboard"
    )


# ==========================================================
# VEHICLE ENTRY
# ==========================================================

@app.route("/entry", methods=["POST"])
def entry():
    """Handle vehicle entry."""

    plate_number = (
        request.form.get("plate_number", "")
        .strip()
        .upper()
    )

    vehicle_type = (
        request.form.get("vehicle_type", "")
        .strip()
    )

    if not plate_number or not vehicle_type:
        return render_page(
            error=(
                "Please provide the vehicle plate number "
                "and vehicle type."
            ),
            active_tab="dashboard"
        )

    result = vehicle_entry(
        plate_number,
        vehicle_type
    )

    return render_page(
        entry_result=result,
        active_tab="dashboard"
    )


# ==========================================================
# VEHICLE EXIT
# ==========================================================

@app.route("/exit", methods=["POST"])
def exit_vehicle():
    """Handle vehicle exit and payment."""

    identifier = (
        request.form.get("identifier", "")
        .strip()
        .upper()
    )

    payment_method = (
        request.form.get("payment_method", "")
        .strip()
    )

    if not identifier or not payment_method:
        return render_page(
            error=(
                "Please provide the vehicle plate/ticket "
                "and payment method."
            ),
            active_tab="dashboard"
        )

    result = vehicle_exit(
        identifier,
        payment_method
    )

    return render_page(
        exit_result=result,
        active_tab="dashboard"
    )


# ==========================================================
# PAYMENTS & AUDIT
# ==========================================================

@app.route("/payments")
def payments():
    """Display payment collection and audit information."""

    payment_summary = get_payment_summary()
    payment_history = get_payment_history()
    daily_collection = get_daily_collection_summary()

    return render_page(
        "payments.html",
        payment_summary=payment_summary,
        payment_history=payment_history,
        daily_collection=daily_collection,
        active_tab="payments"
    )


# ==========================================================
# PARKING RATES
# ==========================================================

@app.route("/rates")
def rates():
    """Display parking-rate management."""

    return render_page(
        "rates.html",
        active_tab="rates"
    )


@app.route("/rates", methods=["POST"])
def update_rate():
    """
    Update a parking rate.

    Management can change parking charges
    without modifying the application source code.
    """

    rate_id = request.form.get("rate_id", "").strip()
    amount = request.form.get("amount", "").strip()

    if not rate_id or not amount:
        return render_page(
            "rates.html",
            error="Please provide a valid rate and amount.",
            active_tab="rates"
        )

    try:
        rate_id = int(rate_id)
        amount = float(amount)

        if amount < 0:
            return render_page(
                "rates.html",
                error="Parking rate cannot be negative.",
                active_tab="rates"
            )

    except ValueError:
        return render_page(
            "rates.html",
            error="Please enter a valid parking rate.",
            active_tab="rates"
        )

    db = get_db_connection()

    try:
        rate = db.execute(
            """
            SELECT
                rate_id,
                rate_name
            FROM parking_rates
            WHERE rate_id = ?
            """,
            (rate_id,)
        ).fetchone()

        if not rate:
            return render_page(
                "rates.html",
                error="Parking rate was not found.",
                active_tab="rates"
            )

        db.execute(
            """
            UPDATE parking_rates
            SET
                amount = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE rate_id = ?
            """,
            (
                amount,
                rate_id
            )
        )

        db.commit()

    finally:
        db.close()

    return redirect(url_for("rates"))


if __name__ == "__main__":
    app.run(debug=True)
