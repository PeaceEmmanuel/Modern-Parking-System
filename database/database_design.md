# PARKSBY - DATABASE DESIGN

## 1. DATABASE OVERVIEW

Parksby uses a relational SQLite database to store and manage
parking information dynamically.

The database stores:
- Vehicle information
- Parking slot information
- Parking records
- Payment information

The database allows information to persist even after the application
is closed and restarted.


## 2. VEHICLES TABLE

The `vehicles` table stores information about vehicles using the
parking facility.

| Field | Data Type | Constraints | Description |
|---|---|---|---|
| vehicle_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique vehicle identifier |
| plate_number | VARCHAR(20) | NOT NULL UNIQUE | Vehicle registration number |
| vehicle_type | VARCHAR(20) | NOT NULL | Type of vehicle |
| created_at | DATETIME | NOT NULL | Date and time vehicle was registered |

### Purpose

This table prevents duplicate vehicle records and allows vehicles
to be identified using their registration plate.


## 3. PARKING_SLOTS TABLE

The `parking_slots` table stores the available parking spaces.

| Field | Data Type | Constraints | Description |
|---|---|---|---|
| slot_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique slot identifier |
| slot_number | VARCHAR(10) | NOT NULL UNIQUE | Parking slot number |
| status | VARCHAR(20) | NOT NULL | AVAILABLE or OCCUPIED |

### Purpose

This table allows Parksby to track which parking spaces are
available and which are occupied.


## 4. PARKING_RECORDS TABLE

The `parking_records` table records every parking session.

| Field | Data Type | Constraints | Description |
|---|---|---|---|
| record_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique parking record |
| ticket_id | VARCHAR(30) | NOT NULL UNIQUE | Unique parking ticket |
| vehicle_id | INTEGER | NOT NULL | Vehicle associated with the record |
| slot_id | INTEGER | NOT NULL | Assigned parking slot |
| entry_time | DATETIME | NOT NULL | Vehicle entry time |
| exit_time | DATETIME | NULL | Vehicle exit time |
| duration_minutes | INTEGER | NULL | Parking duration in minutes |
| fee | DECIMAL(10,2) | NULL | Calculated parking fee |
| status | VARCHAR(20) | NOT NULL | PARKED or EXITED |

### Foreign Keys

- `vehicle_id` references `vehicles(vehicle_id)`
- `slot_id` references `parking_slots(slot_id)`

### Purpose

This table links a vehicle to its assigned parking slot and stores
the complete parking session from entry to exit.


## 5. PAYMENTS TABLE

The `payments` table records payments made for parking sessions.

| Field | Data Type | Constraints | Description |
|---|---|---|---|
| payment_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique payment identifier |
| record_id | INTEGER | NOT NULL | Parking record being paid for |
| amount | DECIMAL(10,2) | NOT NULL | Amount paid |
| payment_method | VARCHAR(20) | NOT NULL | Payment method |
| payment_reference | VARCHAR(50) | NOT NULL UNIQUE | Unique payment reference |
| payment_status | VARCHAR(20) | NOT NULL | PENDING, PAID or FAILED |
| payment_time | DATETIME | NOT NULL | Date and time of payment |

### Foreign Key

- `record_id` references `parking_records(record_id)`

### Purpose

This table maintains a separate financial record for each parking
transaction.


## 6. ENTITY RELATIONSHIPS

The relationships between the tables are:

- One vehicle can have many parking records.
- One parking slot can appear in many parking records over time.
- One parking record can have a payment.
- Each parking record belongs to one vehicle.
- Each parking record uses one parking slot.

Relationship structure:

    VEHICLES
        |
        | 1
        |
        | *
        v
    PARKING_RECORDS
        |
        | 1
        |
        | 0..1
        v
    PAYMENTS

    PARKING_SLOTS
        |
        | 1
        |
        | *
        v
    PARKING_RECORDS


## 7. PARKING FEE STRUCTURE

Parksby uses the following parking tariff:

| Parking Duration | Fee |
|---|---:|
| 0 - 30 minutes | KES 0 |
| More than 30 minutes - 2 hours | KES 50 |
| More than 2 - 4 hours | KES 100 |
| More than 4 - 6 hours | KES 300 |
| More than 6 hours | KES 500 |


## 8. DATABASE OPERATIONS

The system performs the following database operations:

### Vehicle Entry

1. Check whether the vehicle already has an active parking record.
2. Find an available parking slot.
3. Create or retrieve the vehicle record.
4. Create a parking record.
5. Change the slot status to OCCUPIED.

### Vehicle Exit

1. Find the active parking record.
2. Record the exit time.
3. Calculate the parking duration.
4. Calculate the parking fee.
5. Record the payment.
6. Change the parking record status to EXITED.
7. Change the parking slot status to AVAILABLE.

### Slot Management

The database allows the system to:
- Count available slots.
- Identify occupied slots.
- Identify available slots.
- Update slot status.

### Payment Management

The database stores:
- Amount paid
- Payment method
- Payment reference
- Payment status
- Payment time


## 9. DATA INTEGRITY

The database uses constraints to maintain data integrity.

Examples:

- Primary keys uniquely identify records.
- Unique constraints prevent duplicate plate numbers.
- Unique constraints prevent duplicate ticket IDs.
- Foreign keys maintain relationships between tables.
- NOT NULL constraints ensure required information is provided.
- Status values are controlled by the application.

This ensures that invalid or incomplete parking records are
minimized.


## 10. DYNAMIC DATABASE

Parksby is dynamic because records are created, retrieved,
updated and deleted during system operation.

For example:

    Vehicle enters
          ↓
    Parking record created
          ↓
    Slot becomes OCCUPIED
          ↓
    Vehicle exits
          ↓
    Payment recorded
          ↓
    Parking record updated
          ↓
    Slot becomes AVAILABLE

The database therefore changes according to real parking activity
rather than containing static sample information.
