# PARKSBY - DATA STRUCTURES

## 1. ARRAY / LIST

### Purpose
A list is used to maintain the collection of parking slots.

### Example
parking_slots = [P01, P02, P03, P04, ...]

### Why it is used
- Stores multiple parking slots.
- Allows the system to iterate through slots.
- Makes it easy to identify available and occupied slots.
- Supports displaying parking slot status to drivers.

### Operations
- Traversal
- Searching
- Updating slot status


## 2. QUEUE

### Purpose
A queue is used to manage vehicles waiting when all parking slots are occupied.

### Principle
The queue follows FIFO (First In, First Out).

### Why it is used
- The first vehicle to join the waiting queue should be served first when a slot becomes available.
- Provides fair waiting order.
- Efficiently manages vehicles during peak parking periods.

### Operations
- Enqueue: Add a waiting vehicle.
- Dequeue: Remove the first waiting vehicle.
- Peek: View the first vehicle without removing it.


## 3. HASH MAP / DICTIONARY

### Purpose
A dictionary/hash map can be used to quickly locate an active parking record using a vehicle's plate number or ticket ID.

### Example
active_vehicles = {
    "KDA123A": parking_record
}

### Why it is used
- Provides fast vehicle lookup.
- Helps detect duplicate parked vehicles.
- Allows efficient retrieval during vehicle exit.
- Reduces unnecessary sequential searching.


## 4. OBJECTS / RECORDS

### Purpose
Objects are used to represent real-world entities in the parking system.

### Examples
- Vehicle
- ParkingSlot
- ParkingRecord
- Payment

### Why they are used
Each object groups related information and operations together.

For example, a ParkingRecord can contain:
- ticket_id
- plate_number
- slot_number
- entry_time
- exit_time
- duration
- fee
- status


## 5. ENUMERATION

### Purpose
Enumerations can represent fixed states within the system.

### Examples

Parking slot status:
- AVAILABLE
- OCCUPIED

Parking record status:
- PARKED
- EXITED

Payment status:
- PENDING
- PAID
- FAILED

### Why it is used
Enumerations prevent inconsistent status values and make the system easier to maintain.
