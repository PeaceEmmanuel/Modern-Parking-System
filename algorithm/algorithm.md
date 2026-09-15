# PARKING SYSTEM ALGORITHM

## 1. VEHICLE ENTRY

START

Check the number of available parking slots.

IF available_slots > 0 THEN

    Read vehicle plate_number.

    Check if the vehicle is already parked.

    IF vehicle is already parked THEN

        Display "Ve# PARKSBY - PARKING MANAGEMENT SYSTEM ALGORITHMS

## 1. VEHICLE ENTRY ALGORITHM

START

Display the number of currently available parking slots.

IF available_slots > 0 THEN

    Read vehicle plate_number.

    Validate the vehicle plate number.

    Search for an active parking record using plate_number.

    IF an active parking record exists THEN

        Display "Vehicle is already parked."

    ELSE

        Find the first available parking slot.

        Generate a unique ticket_id.

        Record:
            - vehicle plate number
            - assigned parking slot
            - entry time
            - ticket ID
            - parking status = PARKED

        Save the parking record to the database.

        Decrease available_slots by 1.

        Open the entry barrier.

        Display:
            - ticket ID
            - assigned parking slot
            - entry time
            - remaining available slots

    END IF

ELSE

    Display "Parking Full."

    Ask whether the driver wants to join the waiting queue.

    IF driver accepts THEN

        Add vehicle to the waiting queue.

        Display queue confirmation.

    ELSE

        Display "Entry cannot be completed."

    END IF

END IF

STOP


## 2. PARKING SLOT MANAGEMENT ALGORITHM

START

Retrieve all parking slots from the database.

FOR each parking slot

    IF slot status = AVAILABLE THEN

        Add slot to available slots list.

    END IF

END FOR

Display the number of available slots.

Display the status of each parking slot.

STOP


## 3. VEHICLE EXIT ALGORITHM

START

Read vehicle plate_number or ticket_id.

Search for the active parking record.

IF active parking record exists THEN

    Record exit_time.

    Calculate parking duration in minutes.

    Send parking duration to the fee calculation module.

    Display calculated parking fee.

    Send fee to the payment module.

    IF payment is successful THEN

        Update parking record:
            - exit time
            - parking duration
            - amount paid
            - status = EXITED

        Mark the parking slot as AVAILABLE.

        Increase available_slots by 1.

        Open the exit barrier.

        Display:
            - parking duration
            - amount paid
            - payment confirmation
            - exit confirmation

    ELSE

        Display "Payment unsuccessful. Barrier remains closed."

    END IF

ELSE

    Display "Vehicle or ticket not found."

END IF

STOP


## 4. PARKING FEE CALCULATION ALGORITHM

START

Receive parking duration in minutes.

IF duration <= 30 THEN

    fee = KES 0

ELSE IF duration <= 120 THEN

    fee = KES 50

ELSE IF duration <= 240 THEN

    fee = KES 100

ELSE IF duration <= 360 THEN

    fee = KES 300

ELSE

    fee = KES 500

END IF

Return fee.

STOP


## 5. PAYMENT ALGORITHM

START

Receive parking fee.

Display amount to be paid.

Select payment method.

Process payment.

IF payment is successful THEN

    Generate payment reference.

    Record payment details.

    Display "Payment successful."

    Return payment_successful.

ELSE

    Display "Payment failed."

    Return payment_failed.

END IF

STOP


## 6. BARRIER CONTROL ALGORITHM

START

Receive barrier request.

IF request = ENTRY THEN

    IF parking slot has been successfully assigned THEN

        Open entry barrier.

    ELSE

        Keep entry barrier closed.

    END IF

ELSE IF request = EXIT THEN

    IF payment has been successfully completed THEN

        Open exit barrier.

    ELSE

        Keep exit barrier closed.

    END IF

END IF

STOP
