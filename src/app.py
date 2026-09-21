from flask import Flask, render_template, request, redirect, url_for

from .models import (
    get_available_slots,
    get_payment_summary,
    get_payment_history,
    get_daily_collection_summary,
    create_parking_slot
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
# PARKING CAPACITY MANAGEMENT
# ==========================================================

@app.route("/slots/add", methods=["POST"])
def add_parking_slot():
    """Add a new available parking slot."""

    result = create_parking_slot()

    if not result["success"]:
        return render_page(
            error="Unable to add a new parking slot.",
            active_tab="dashboard"
        )

    return render_page(
        success=(
            f"Parking slot {result['slot_number']} "
            "was added successfully."
        ),
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
    """Update an existing parking rate segment."""

    rate_id = request.form.get("rate_id", "").strip()
    rate_name = request.form.get("rate_name", "").strip()
    minimum_minutes = request.form.get(
        "minimum_minutes", ""
    ).strip()
    maximum_minutes = request.form.get(
        "maximum_minutes", ""
    ).strip()
    amount = request.form.get("amount", "").strip()

    try:
        rate_id = int(rate_id)
        minimum_minutes = int(minimum_minutes)
        amount = float(amount)

        maximum_minutes = (
            int(maximum_minutes)
            if maximum_minutes
            else None
        )

    except ValueError:
        return render_page(
            "rates.html",
            error="Please enter valid rate values.",
            active_tab="rates"
        )

    if not rate_name:
        return render_page(
            "rates.html",
            error="Rate name is required.",
            active_tab="rates"
        )

    if minimum_minutes < 0:
        return render_page(
            "rates.html",
            error="Minimum minutes cannot be negative.",
            active_tab="rates"
        )

    if maximum_minutes is not None:
        if maximum_minutes < minimum_minutes:
            return render_page(
                "rates.html",
                error=(
                    "Maximum minutes must be greater than "
                    "or equal to minimum minutes."
                ),
                active_tab="rates"
            )

    if amount < 0:
        return render_page(
            "rates.html",
            error="Parking rate cannot be negative.",
            active_tab="rates"
        )

    db = get_db_connection()

    try:

        rate = db.execute(
            """
            SELECT rate_id
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


        overlap = find_rate_overlap(
            db,
            rate_id,
            minimum_minutes,
            maximum_minutes
        )

        if overlap:
            return render_page(
                "rates.html",
                error=(
                    "The selected duration overlaps with "
                    f"'{overlap['rate_name']}'."
                ),
                active_tab="rates"
            )


        db.execute(
            """
            UPDATE parking_rates
            SET
                rate_name = ?,
                minimum_minutes = ?,
                maximum_minutes = ?,
                amount = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE rate_id = ?
            """,
            (
                rate_name,
                minimum_minutes,
                maximum_minutes,
                amount,
                rate_id
            )
        )

        db.commit()

    finally:
        db.close()

    return redirect(url_for("rates"))


@app.route("/rates/add", methods=["POST"])
def add_rate():
    """Create a new parking rate segment."""

    db = get_db_connection()

    try:

        existing = db.execute(
            """
            SELECT
                rate_id,
                minimum_minutes,
                maximum_minutes
            FROM parking_rates
            WHERE active = 1
            ORDER BY minimum_minutes DESC
            LIMIT 1
            """
        ).fetchone()


        if existing and existing["maximum_minutes"] is None:
            return render_page(
                "rates.html",
                error=(
                    "The current tariff already has an open-ended "
                    "rate. Give that rate a maximum duration before "
                    "adding another segment."
                ),
                active_tab="rates"
            )


        if existing:
            minimum_minutes = (
                existing["maximum_minutes"] + 1
            )
        else:
            minimum_minutes = 0


        rate_name = f"New Rate {minimum_minutes}+"

        db.execute(
            """
            INSERT INTO parking_rates
                (
                    rate_name,
                    minimum_minutes,
                    maximum_minutes,
                    amount,
                    active
                )
            VALUES (?, ?, NULL, 0, 1)
            """,
            (
                rate_name,
                minimum_minutes
            )
        )

        db.commit()

    finally:
        db.close()

    return redirect(url_for("rates"))


@app.route("/rates/delete", methods=["POST"])
def delete_rate():
    """Remove a parking rate segment."""

    rate_id = request.form.get("rate_id", "").strip()

    try:
        rate_id = int(rate_id)
    except ValueError:
        return render_page(
            "rates.html",
            error="Invalid rate identifier.",
            active_tab="rates"
        )

    db = get_db_connection()

    try:

        rate = db.execute(
            """
            SELECT rate_id
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
            DELETE FROM parking_rates
            WHERE rate_id = ?
            """,
            (rate_id,)
        )

        db.commit()

    finally:
        db.close()

    return redirect(url_for("rates"))


def find_rate_overlap(
    db,
    rate_id,
    minimum_minutes,
    maximum_minutes
):
    """
    Find another active rate whose duration range overlaps
    the proposed range.
    """

    rates = db.execute(
        """
        SELECT
            rate_id,
            rate_name,
            minimum_minutes,
            maximum_minutes
        FROM parking_rates
        WHERE active = 1
          AND rate_id != ?
        ORDER BY minimum_minutes ASC
        """,
        (rate_id,)
    ).fetchall()


    for rate in rates:

        existing_min = rate["minimum_minutes"]
        existing_max = rate["maximum_minutes"]


        proposed_max = (
            maximum_minutes
            if maximum_minutes is not None
            else float("inf")
        )

        existing_max_value = (
            existing_max
            if existing_max is not None
            else float("inf")
        )


        if (
            minimum_minutes <= existing_max_value
            and existing_min <= proposed_max
        ):
            return rate


    return None


if __name__ == "__main__":
    app.run(debug=True)
