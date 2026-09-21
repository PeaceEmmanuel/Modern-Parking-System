
# Parksby — Academic Parking Management System

Parksby is a web-based academic parking management system developed to manage vehicle entry, parking-space allocation, parking duration, fee calculation, payments, vehicle exits, and administrative reporting.

The system is designed as a practical parking-management solution for an academic institution. It combines a Flask web application with a SQLite database and includes database documentation, algorithms, data-structure documentation, configurable parking rates, and payment/audit reporting.

---

## 1. Project Overview

Parksby provides a central system for managing the complete parking process:

1. A vehicle arrives at the parking facility.
2. The vehicle number plate and vehicle type are recorded.
3. The system checks whether the vehicle is already parked.
4. An available parking slot is allocated.
5. A parking ticket is generated.
6. The slot is marked as occupied.
7. When the vehicle exits, the system calculates the parking duration.
8. The applicable parking rate is retrieved from the configured rate table.
9. A payment is processed using the selected payment method.
10. The payment is recorded for auditing and reconciliation.
11. The parking record is completed.
12. The parking slot is released.
13. The exit barrier is considered opened only after successful payment.

The application also provides administrative pages for payment auditing and parking-rate management.

---

## 2. Main Features

### Vehicle Entry

- Records vehicle number plate.
- Records vehicle type.
- Prevents duplicate active parking for the same vehicle.
- Automatically selects an available parking slot.
- Generates a unique parking ticket.
- Records the entry time.
- Marks the allocated slot as occupied.

### Parking Slot Management

- Tracks parking-slot availability.
- Uses parking slots P01–P10 in the current academic system configuration.
- Displays occupied and available slots on the dashboard.
- Releases a slot after a successful vehicle exit.

### Vehicle Exit

- Searches for a vehicle using its plate number or parking ticket.
- Calculates the parking duration.
- Calculates the applicable parking fee.
- Processes the selected payment method.
- Records the successful payment.
- Completes the parking record.
- Releases the occupied slot.
- Confirms that the exit barrier opens only after successful payment.

### Payment Management

Supported payment methods:

- M-Pesa
- Card
- Cash

Each successful payment receives a unique payment reference.

Payment records include:

- Payment ID
- Parking record
- Amount
- Payment method
- Payment reference
- Payment status
- Payment time

### Payment & Audit Reporting

The **Payments & Audit** page provides:

- Total collection
- Number of successful payments
- M-Pesa collection
- Cash collection
- Card collection
- Detailed payment history
- Daily collection summaries
- Parking and payment references for reconciliation

Only payments with a `PAID` status are included in collection reports.

### Configurable Parking Rates

Parking fees are stored in the database rather than being permanently hard-coded into the application.

Administrators can:

- View active parking-rate segments.
- Update rate names.
- Change minimum duration.
- Change maximum duration.
- Change the amount charged.
- Add new rate segments.
- Remove rate segments.
- Configure an open-ended rate by leaving the maximum duration blank.

The system also checks for overlapping active rate ranges when rates are updated.

### Dashboard

The main dashboard provides an operational view of the parking facility, including:

- Parking capacity status
- Available spaces
- Occupied spaces
- Current parking slots
- Vehicle entry controls
- Vehicle exit controls
- Current parking-rate information

---

## 3. Current Parking Rate Configuration

The default rate structure included with the database is:

| Duration | Amount |
|---|---:|
| 0–30 minutes | KES 0 |
| 31–120 minutes | KES 50 |
| 121–240 minutes | KES 100 |
| 241–360 minutes | KES 300 |
| 361+ minutes | KES 500 |

These values are configurable through the **Parking Rates** management page.

The fee calculation selects the active rate whose duration range contains the calculated parking duration.

---

## 4. System Architecture

Parksby follows a simple layered architecture:

```text
┌───────────────────────────────┐
│          Web Browser          │
│ HTML / CSS / JavaScript       │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Flask Application      │
│            app.py             │
└───────────────┬───────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
┌───────────────┐  ┌────────────────┐
│ Parking Logic │  │ Data Models    │
│ parking.py    │  │ models.py      │
└───────┬───────┘  └───────┬────────┘
        │                   │
        └─────────┬─────────┘
                  ▼
        ┌─────────────────────┐
        │   SQLite Database   │
        │     parksby.db      │


Application Layers

Presentation Layer

HTML templates
CSS
Browser forms
Dashboard and administration pages

Application Layer

Flask routes
Vehicle entry and exit processing
Payment processing
Rate management
Reporting

Business Logic Layer

Slot allocation
Duration calculation
Fee calculation
Payment validation
Parking-record completion

Data Layer

SQLite
Database connection utilities
SQL queries
CRUD operations
5. Technology Stack
Technology	Purpose
Python	Application programming language
Flask	Web application framework
SQLite	Relational database
HTML5	Web-page structure
CSS3	Interface styling
Jinja2	Server-side HTML templating
JavaScript	Client-side interactions
Git	Version control
GitHub	Source-code hosting


6. Project Structure
parking-system/
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
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   └── templates/
│       ├── index.html
│       ├── payments.html
│       └── rates.html
│
├── .gitignore
└── README.md


7. Important Source Files
src/app.py

The Flask application entry point.

Responsibilities include:

Starting the web application.
Defining HTTP routes.
Handling dashboard requests.
Handling vehicle-entry requests.
Handling vehicle-exit requests.
Serving payment reports.
Serving parking-rate management.
Handling rate creation, updates, and deletion.
src/parking.py

Contains the main parking business logic.

Responsibilities include:

Ticket generation.
Parking entry.
Parking exit.
Parking-duration calculation.
Parking-fee calculation.
Payment validation.
Payment processing.
src/models.py

Contains database operations and data-access functions.

Responsibilities include:

Vehicle operations.
Parking-record operations.
Parking-slot operations.
Payment operations.
Parking-rate operations.
Payment reporting and reconciliation.
src/database.py

Provides the SQLite database connection used by the application.

src/templates/index.html

The main dashboard template.

It contains:

Navigation
Parking dashboard
Vehicle entry form
Vehicle exit form
Parking-slot display
System messages
src/templates/payments.html

The payment and audit page.

It contains:

Collection summaries
Payment history
Daily collection summaries
Reconciliation information
src/templates/rates.html

The parking-rate administration page.

It provides forms for:

Viewing rates
Updating rates
Adding rate segments
Removing rate segments
src/static/css/style.css

Contains the visual design of the application, including:

Dashboard styling
Navigation
Forms
Parking-slot indicators
Payment tables
Rate-management cards
Responsive layouts
Status messages
8. Database Design

Parksby uses SQLite for persistent storage.

The main database entities are:

Vehicles

Stores information about vehicles using the parking facility.

Typical information includes:

Vehicle ID
Plate number
Vehicle type
Parking Slots

Stores parking-space information.

Each slot has:

Slot ID
Slot number
Status

Allowed slot statuses are:

AVAILABLE
OCCUPIED

The current database is initialized with:

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
Parking Records

Stores the lifecycle of a parking visit.

The record connects:

Vehicle
Parking slot
Ticket
Entry time
Exit time
Duration
Fee
Payments

Stores payment information associated with completed parking records.

Payment status values include:

PENDING
PAID
FAILED
Parking Rates

Stores configurable duration-based parking charges.

Each rate contains:

Rate ID
Rate name
Minimum minutes
Maximum minutes
Amount
Active status
Creation timestamp
Update timestamp
9. Database Relationship Overview
VEHICLES
   │
   │ 1
   │
   │ many
   ▼
PARKING_RECORDS
   │
   ├──────────────► PARKING_SLOTS
   │
   │ 1
   │
   │ many
   ▼
PAYMENTS


PARKING_RATES
   │
   └── Used by the fee-calculation process

The parking record acts as the central transaction connecting a vehicle, its allocated slot, the parking duration, and the resulting payment.

10. Vehicle Entry Algorithm

The entry process follows these steps:

START
  │
  ▼
Receive vehicle plate and vehicle type
  │
  ▼
Check whether vehicle is already parked
  │
  ├── YES ──► Reject entry
  │
  ▼ NO
Find an available parking slot
  │
  ├── NONE ──► Report parking full
  │
  ▼
Create vehicle record
  │
  ▼
Generate parking ticket
  │
  ▼
Create parking record
  │
  ▼
Mark slot OCCUPIED
  │
  ▼
Return ticket, slot and entry details
  │
  ▼
END
11. Vehicle Exit Algorithm
START
  │
  ▼
Receive vehicle plate/ticket
and payment method
  │
  ▼
Find active parking record
  │
  ├── NOT FOUND ──► Reject exit
  │
  ▼ FOUND
Calculate parking duration
  │
  ▼
Find applicable parking rate
  │
  ▼
Calculate parking fee
  │
  ▼
Validate payment method
  │
  ├── INVALID ──► Reject payment
  │
  ▼ VALID
Generate payment reference
  │
  ▼
Record PAID payment
  │
  ▼
Complete parking record
  │
  ▼
Release parking slot
  │
  ▼
Confirm exit barrier opened
  │
  ▼
END
12. Fee Calculation

The fee calculation is duration-based.

The system first calculates:

duration = exit time - entry time

The duration is converted into minutes.

The system then searches the active parking_rates records for a rate where:

minimum_minutes <= duration

and either:

maximum_minutes >= duration

or:

maximum_minutes IS NULL

The matching rate determines the parking fee.

This approach allows administrators to modify the tariff structure without modifying the core fee-calculation code.

13. Payment Processing

Parksby validates payment methods against the supported options:

M-Pesa
Card
Cash

A successful payment receives a generated reference such as:

PAY-XXXXXXXX

The payment is then stored with a PAID status.

The system completes the parking record and releases the slot only after successful payment processing.

If payment validation fails, the system returns an unsuccessful payment response and the exit process does not release the parking slot.

14. Payment Audit and Reconciliation

The payment reporting system supports operational auditing.

The payment summary provides:

Total Collection
Successful Payments
M-Pesa Collection
Cash Collection
Card Collection

The payment-history report records information such as:

Payment ID
Vehicle Plate
Ticket
Parking Slot
Amount
Payment Method
Payment Reference
Payment Status
Payment Time
Entry Time
Exit Time
Duration

The daily collection report groups successful payments by date.

This provides a basis for comparing recorded collections against payment-channel totals.

15. Data Structures

The system uses several fundamental data structures and database structures.

Lists

Lists are used where collections of records need to be processed or displayed.

Examples:

Available parking slots
Parking rates
Payment history
Daily collection records
Dictionaries

Python dictionaries are used for structured responses and transaction results.

For example:

{
    "success": True,
    "ticket_id": "PK-1234ABCD",
    "slot_number": "P01",
    "fee": 50
}
Database Tables

SQLite relational tables provide persistent storage for:

Vehicles
Parking slots
Parking records
Payments
Parking rates
Unique Constraints

The database uses unique constraints to protect important identifiers, such as:

Vehicle plate numbers where applicable
Slot numbers
Payment references
16. Validation and Error Handling

Parksby includes validation for common operational errors.

Examples include:

Duplicate Vehicle

If a vehicle is already actively parked:

Vehicle is already parked.

The system prevents another active parking record from being created.

Parking Full

If no available slot exists:

Parking is full.
Invalid Payment Method

Only the supported payment methods are accepted.

Missing Vehicle or Ticket

If no matching parking record is found:

Vehicle or ticket not found.
Invalid Rate Configuration

Rate management validates:

Required fields
Numeric values
Non-negative durations
Non-negative amounts
Duration ranges
Overlapping active rate segments
17. User Interface

The application is divided into three main areas.

Dashboard
Dashboard
├── Parking status
├── Vehicle entry
├── Vehicle exit
└── Parking slots
Payments & Audit
Payments & Audit
├── Total collection
├── Successful payments
├── M-Pesa
├── Cash
├── Card
├── Payment history
└── Daily collection summary
Parking Rates
Parking Rates
├── Current rate segments
├── Update rate
├── Add rate segment
└── Remove rate segment
18. Installation
Requirements

Install:

Python 3
pip
Git
Clone the Repository
git clone https://github.com/PeaceEmmanuel/Modern-Parking-System.git
cd Modern-Parking-System
Create a Virtual Environment

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate
Install Flask
pip install flask
19. Database Setup

The project includes:

database/schema.sql

and the SQLite database:

database/parksby.db

The schema contains the tables required by the application and initializes the standard parking slots and default parking rates.

If a fresh database is required:

python - <<'PY'
import sqlite3

connection = sqlite3.connect("database/parksby.db")

with open("database/schema.sql", "r", encoding="utf-8") as file:
    connection.executescript(file.read())

connection.commit()
connection.close()

print("Database schema applied successfully.")
PY
20. Running the Application

From the project root:

python -m src.app

The Flask development server will start.

Open the local address shown by Flask in a web browser, normally:

http://127.0.0.1:5000
21. Typical Usage Workflow
Step 1 — Vehicle Entry

Enter:

Plate Number: KDA 123A
Vehicle Type: Car

The system:

Checks for duplicate parking.
Finds an available slot.
Creates a parking record.
Generates a ticket.
Occupies the slot.
Step 2 — Vehicle Remains Parked

The dashboard shows the allocated slot as occupied.

Step 3 — Vehicle Exit

Enter the vehicle plate number or ticket and select:

M-Pesa

or:

Card

or:

Cash
Step 4 — Fee Calculation

The system calculates the parking duration and finds the corresponding configured rate.

Step 5 — Payment

A payment reference is generated and the successful payment is recorded.

Step 6 — Exit

The parking record is completed and the slot becomes available again.

Step 7 — Audit

The payment appears in:

Payments & Audit

where it contributes to the relevant collection totals.

22. Testing

Basic application validation can be performed with:

python -m py_compile src/app.py src/models.py src/parking.py

A complete functional test should cover:

Entry Tests
Valid vehicle entry
Duplicate vehicle entry
Parking-full condition
Slot allocation
Exit Tests
Valid vehicle exit
Invalid vehicle/ticket
Duration calculation
Fee calculation
Slot release
Payment Tests
M-Pesa payment
Card payment
Cash payment
Invalid payment method
Payment reference generation
Rate Tests
Viewing rates
Updating a rate
Adding a rate
Removing a rate
Overlapping-rate validation
Open-ended rates
Reporting Tests
Successful payment count
Total collection
Payment-method totals
Payment history
Daily collection summary
23. Security and Data Integrity Considerations

The current academic implementation focuses on functionality and database integrity.

Important controls include:

Parameterized database queries.
Database constraints.
Unique payment references.
Controlled payment-method values.
Validation of parking-rate ranges.
Prevention of duplicate active vehicle parking.
Payment status tracking.

For a production deployment, additional measures would be appropriate, including:

Authentication and authorization.
CSRF protection.
HTTPS.
Secure secret management.
Stronger input validation.
Production-grade payment gateway integration.
Database backups.
Role-based administration.
Comprehensive automated tests.
Production WSGI deployment.
24. Project Scope
Included
Vehicle registration during entry
Parking-space allocation
Parking occupancy tracking
Parking ticket generation
Entry-time recording
Vehicle exit processing
Parking-duration calculation
Configurable fee calculation
M-Pesa, Card and Cash payment options
Payment recording
Payment references
Payment auditing
Daily collection reporting
Parking-rate administration
Web dashboard
Out of Scope

The current academic implementation does not include:

Online parking pre-booking
Valet parking
Loyalty programmes
Automated plate blacklisting
Live external payment-provider integration
Hardware-controlled physical barriers
Multi-site parking management
25. Design Documentation

Additional academic documentation is included in the repository.

Algorithms
algorithm/algorithm.md

Contains the algorithms and process descriptions used by the parking system.

Database Design
database/database_design.md

Documents the database structure and relationships.

SQL Schema
database/schema.sql

Contains the database creation and initialization SQL.

Data Structures
data-structures/data-structures.md

Documents the data structures used in the implementation.

26. Git and GitHub

The project is maintained using Git.

Repository:

Modern Parking System — Parksby

GitHub:

https://github.com/PeaceEmmanuel/Modern-Parking-System

Typical workflow:

git status
git add .
git commit -m "Update Parksby system"
git push origin main

Before committing:

python -m py_compile src/app.py src/models.py src/parking.py
27. Future Improvements

Possible future improvements include:

Real M-Pesa API integration.
Real card-payment gateway integration.
Authentication and role-based access.
Automated database backups.
Advanced analytics dashboards.
Exportable payment reports.
Search and filtering for audit records.
Automated receipt generation.
QR-code parking tickets.
Hardware barrier integration.
Real-time notifications.
Multi-location parking support.
Automated license-plate recognition.
REST API integration.
Automated unit and integration test suites.

These are potential extensions and are not required for the current academic scope.

28. Academic Purpose

Parksby demonstrates the application of software-development concepts in a practical parking-management scenario.

The project brings together:

Web application development
Database design
CRUD operations
Algorithms
Data structures
Input validation
Transaction processing
Payment recording
Reporting
User-interface design
Version control

The system provides a complete academic demonstration of how a parking operation can be represented using software and a relational database.

29. Author

Peace Emmanuel Muthomi

Phone: +254742588363

Email: peace.muthoni1@gmail.com

30. License

This project was developed as an academic software project.

Use, modification, and distribution should follow the requirements of the institution or course under which the project was submitted.
EOF


Then verify it:

```bash
wc -l README.md
head -20 README.md
git diff --stat README.md

If it looks good, commit and push:

git add README.md
git commit -m "Update README documentation"
git push origin main

That will replace the old README with the updated documentation and put it on GitHub.

this is the readme i wann replace 


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


text
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


Slots are tracked using their current status:

* AVAILABLE
* OCCUPIED

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


text
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


---

## System Architecture

The application is organized into several layers.


text
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


---

## Database Design

Parksby uses SQLite to store parking information.

The main database tables are:

### vehicles

Stores vehicle information.

Examples of stored information include:

* Vehicle registration number
* Vehicle details
* Vehicle creation information

### parking_slots

Stores the available parking spaces and their status.

Each slot can be either:


text
AVAILABLE


or


text
OCCUPIED


### parking_records

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

### payments

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


text
data-structures/data-structures.md


---

## Algorithms

The project includes algorithms for:

### Slot Allocation

The system searches for an available slot and assigns it to the entering vehicle.

Conceptually:


text
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


### Slot Release

When a vehicle exits:


text
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


### Fee Calculation

The parking duration is compared against the configured tariff ranges to determine the appropriate parking fee.

Detailed algorithm documentation is available in:


text
algorithm/algorithm.md


---

## Installation

### 1. Clone the repository


bash
git clone https://github.com/PeaceEmmanuel/Modern-Parking-System.git


Move into the project directory:


bash
cd Modern-Parking-System


### 2. Create a Python virtual environment


bash
python3 -m venv venv


### 3. Activate the virtual environment

On Linux:


bash
source venv/bin/activate


### 4. Install Flask


bash
pip install Flask


### 5. Run the application


bash
python src/app.py


The application will normally be available at:


text
http://127.0.0.1:5000


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


text
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


`















        └─────────────────────┘
