
# Parksby — Modern Parking Management System

Parksby is a modern parking management system developed to automate and simplify vehicle entry, parking-slot allocation, parking-duration tracking, fee calculation, payment recording, and vehicle exit.

The project demonstrates the practical use of **Python programming, Flask, SQLite, data structures, algorithms, and database management** in building a real-world parking management application.

---

## Project Overview

Traditional parking management can involve manual vehicle records, difficulty tracking available spaces, and delays when calculating parking charges.

Parksby provides a simple web-based solution that allows a parking attendant or administrator to:

- Register vehicles entering the parking area
- Automatically allocate an available parking slot
- Generate a unique parking ticket
- Track parking duration
- Calculate parking fees
- Record payments
- Release parking slots when vehicles exit
- Prevent the same vehicle from being parked multiple times
- Monitor available parking spaces in real time

---

## Main Features

### 🚗 Vehicle Entry

When a vehicle enters the parking area, the system:

1. Validates the vehicle registration number.
2. Checks whether the vehicle is already parked.
3. Checks whether parking spaces are available.
4. Generates a unique parking ticket.
5. Assigns the first available parking slot.
6. Records the entry time.
7. Displays the allocated slot and ticket information.

### 🅿️ Automatic Slot Allocation

Parksby automatically assigns an available parking space.

The system currently contains **10 parking slots**:

```text
P01
P02
P03
P04
P05
P06
P07
P08
P09
P10
````

Slots are tracked using their current status:

* `AVAILABLE`
* `OCCUPIED`

When a vehicle exits, its slot is automatically returned to the available pool.

### ⏱️ Parking Duration

The system records the vehicle's entry time and calculates the parking duration when the vehicle exits.

This allows the system to determine the correct parking fee automatically.

### 💰 Parking Fee Calculation

The current parking tariff is:

| Parking Duration               |     Fee |
| ------------------------------ | ------: |
| Up to 30 minutes               |   KES 0 |
| More than 30 minutes – 2 hours |  KES 50 |
| More than 2 – 4 hours          | KES 100 |
| More than 4 – 6 hours          | KES 300 |
| More than 6 hours              | KES 500 |

The fee is calculated automatically based on the recorded parking duration.

### 💳 Payment Recording

When a vehicle exits, the system:

1. Calculates the parking duration.
2. Calculates the parking fee.
3. Records the payment.
4. Completes the parking record.
5. Releases the occupied parking slot.

The current application uses a simulated payment process for demonstration purposes.

### 🔒 Duplicate Vehicle Protection

A vehicle that already has an active parking record cannot be registered again until its existing parking session has been completed.

### 📊 Parking Dashboard

The web dashboard displays:

* System status
* Number of available slots
* Vehicle entry form
* Vehicle exit form
* Parking-slot status
* Parking tariff
* Parking system information

---

## Technologies Used

| Technology | Purpose                          |
| ---------- | -------------------------------- |
| Python 3   | Application programming language |
| Flask      | Web application framework        |
| SQLite     | Database management              |
| HTML5      | Web page structure               |
| CSS3       | User interface styling           |
| Git        | Version control                  |
| GitHub     | Source code hosting              |

---

## Project Structure

```text
Modern-Parking-System/
│
├── algorithm/
│   └── algorithm.md
│
├── database/
│   ├── database_design.md
│   ├── parksby.db
│   └── schema.sql
│
├── data-structures/
│   └── data-structures.md
│
├── src/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── parking.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── .gitignore
└── README.md
```

---

## System Architecture

The application is organized into several layers.

```text
              ┌─────────────────────┐
              │   Web Browser       │
              │   Parksby Dashboard │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │      Flask App      │
              │       app.py        │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Parking Management  │
              │     parking.py      │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Data Models       │
              │     models.py       │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │      SQLite         │
              │    parksby.db       │
              └─────────────────────┘
```

---

## Database Design

Parksby uses SQLite to store parking information.

The main database tables are:

### `vehicles`

Stores vehicle information.

Examples of stored information include:

* Vehicle registration number
* Vehicle details
* Vehicle creation information

### `parking_slots`

Stores the available parking spaces and their status.

Each slot can be either:

```text
AVAILABLE
```

or

```text
OCCUPIED
```

### `parking_records`

Stores individual parking sessions.

A parking record contains information such as:

* Vehicle
* Parking slot
* Ticket number
* Entry time
* Exit time
* Parking duration
* Parking fee
* Parking status

### `payments`

Stores payment information associated with completed parking sessions.

---

## Data Structures

The project demonstrates several fundamental data-structure concepts.

### Lists

Lists can be used when handling collections of parking slots and other application data.

### Database Tables

SQLite tables provide structured storage for vehicles, parking slots, parking records, and payments.

### Records

Parking records connect vehicles, slots, entry times, exit times, and payment information into individual parking sessions.

More details are available in:

```text
data-structures/data-structures.md
```

---

## Algorithms

The project includes algorithms for:

### Slot Allocation

The system searches for an available slot and assigns it to the entering vehicle.

Conceptually:

```text
START
  |
  v
Check available slots
  |
  +---- No slot ----> Parking Full
  |
  v
Find available slot
  |
  v
Assign slot to vehicle
  |
  v
Mark slot OCCUPIED
  |
  v
Create parking record
  |
  v
Generate ticket
  |
  v
END
```

### Slot Release

When a vehicle exits:

```text
Find active parking record
        |
        v
Calculate parking duration
        |
        v
Calculate parking fee
        |
        v
Record payment
        |
        v
Complete parking record
        |
        v
Mark slot AVAILABLE
```

### Fee Calculation

The parking duration is compared against the configured tariff ranges to determine the appropriate parking fee.

Detailed algorithm documentation is available in:

```text
algorithm/algorithm.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/PeaceEmmanuel/Modern-Parking-System.git
```

Move into the project directory:

```bash
cd Modern-Parking-System
```

### 2. Create a Python virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

On Linux:

```bash
source venv/bin/activate
```

### 4. Install Flask

```bash
pip install Flask
```

### 5. Run the application

```bash
python src/app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

Open that address in a web browser.

---

## How to Use the System

### Vehicle Entry

1. Open the Parksby dashboard.
2. Enter the vehicle registration number.
3. Enter the required vehicle information.
4. Submit the entry form.
5. The system checks for duplicate active vehicles.
6. The system assigns an available parking slot.
7. A parking ticket is generated.
8. The vehicle is marked as parked.

### Vehicle Exit

1. Enter the vehicle registration number or parking ticket.
2. Submit the exit request.
3. The system finds the active parking record.
4. Parking duration is calculated.
5. The parking fee is calculated.
6. Payment is recorded.
7. The parking record is completed.
8. The parking slot becomes available again.

---

## Example Workflow

A typical parking session follows this process:

```text
Vehicle Arrives
      |
      v
Register Vehicle
      |
      v
Check Duplicate Vehicle
      |
      v
Check Available Slot
      |
      v
Assign Parking Slot
      |
      v
Generate Ticket
      |
      v
Vehicle Parks
      |
      v
Vehicle Requests Exit
      |
      v
Calculate Duration
      |
      v
Calculate Fee
      |
      v
Record Payment
      |
      v
Release Parking Slot
      |
      v
Parking Session Completed
```

---

## Error Handling

The system handles common parking-management situations, including:

* Parking area is full
* Vehicle is already parked
* Vehicle has no active parking record
* Invalid exit request
* No available parking slot
* Invalid or missing vehicle information

---

## Testing

The system has been tested for core parking operations including:

* Vehicle entry
* Duplicate vehicle prevention
* Parking-slot allocation
* Available-slot counting
* Parking duration calculation
* Parking fee calculation
* Vehicle exit
* Payment recording
* Parking-slot release

---

## Future Improvements

Possible future improvements include:

* User authentication and administrator accounts
* Real payment gateway integration
* Vehicle search and parking history
* Daily and monthly revenue reports
* Printable parking receipts
* QR-code parking tickets
* Multiple parking locations
* PostgreSQL/MySQL support for larger deployments
* REST API integration
* Mobile application
* Advanced reporting and analytics

---

## Project Purpose

This project was developed as an academic software project to demonstrate the practical application of:

* Programming fundamentals
* Object-oriented programming concepts
* Algorithms
* Data structures
* Database management
* Web development
* Software engineering principles
* Version control with Git

---

## Author

**Peace Emmanuel Muthomi**

Phone: **+254 742 588 363**

Email: **[peace.muthomi1@gmail.com](mailto:peace.muthomi1@gmail.com)**

---

## License

This project is intended primarily for educational and academic purposes.

````

