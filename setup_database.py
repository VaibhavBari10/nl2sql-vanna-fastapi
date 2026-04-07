import sqlite3
import random
from faker import Faker
from datetime import datetime

fake = Faker()

# Connect DB
conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# Drop existing tables
cursor.executescript("""
DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
""")

# Create tables with constraints
cursor.executescript("""
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    date_of_birth DATE,
    gender TEXT,
    city TEXT,
    registered_date DATE
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT,
    department TEXT,
    phone TEXT
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATETIME,
    status TEXT,
    notes TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(id)
);

CREATE TABLE treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    treatment_name TEXT,
    cost REAL,
    duration_minutes INTEGER,
    FOREIGN KEY(appointment_id) REFERENCES appointments(id)
);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    invoice_date DATE,
    total_amount REAL,
    paid_amount REAL,
    status TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);
""")

# Insert Doctors
specializations = ["Dermatology", "Cardiology", "Orthopedics", "General", "Pediatrics"]

for _ in range(15):
    cursor.execute("""
        INSERT INTO doctors (name, specialization, department, phone)
        VALUES (?, ?, ?, ?)
    """, (
        fake.name(),
        random.choice(specializations),
        "Medical",
        fake.phone_number()
    ))


# Insert Patients (with NULL values)
cities = ["Mumbai", "Pune", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Nagpur", "Nashik"]

for _ in range(200):
    email = fake.email() if random.random() > 0.2 else None
    phone = fake.phone_number() if random.random() > 0.2 else None

    cursor.execute("""
        INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        fake.first_name(),
        fake.last_name(),
        email,
        phone,
        fake.date_of_birth(),
        random.choice(["M", "F"]),
        random.choice(cities),
        fake.date_between(start_date='-1y', end_date='today')
    ))


# Insert Appointments (skewed doctor distribution)
statuses = ["Scheduled", "Completed", "Cancelled", "No-Show"]

# Make some doctors busier
doctor_ids = [1]*5 + list(range(2, 16))

for _ in range(500):
    cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        random.randint(1, 200),
        random.choice(doctor_ids),
        fake.date_time_between(start_date='-1y', end_date='now'),
        random.choice(statuses),
        fake.sentence() if random.random() > 0.2 else None
    ))


# Insert Treatments (ONLY for completed appointments)
cursor.execute("SELECT id FROM appointments WHERE status='Completed'")
completed_appointments = [row[0] for row in cursor.fetchall()]

for _ in range(350):
    if not completed_appointments:
        break

    cursor.execute("""
        INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes)
        VALUES (?, ?, ?, ?)
    """, (
        random.choice(completed_appointments),
        fake.word(),
        random.randint(50, 5000),
        random.randint(10, 120)
    ))


# Insert Invoices (realistic payment logic)
for _ in range(300):
    total = random.randint(100, 5000)
    paid = random.randint(0, total)

    if paid == total:
        status = "Paid"
    elif paid == 0:
        status = "Overdue"
    else:
        status = "Pending"

    cursor.execute("""
        INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        random.randint(1, 200),
        fake.date_between(start_date='-1y', end_date='today'),
        total,
        paid,
        status
    ))

# Commit and close
conn.commit()
conn.close()

# Summary Output
print("""
Database created successfully!

Records inserted:
- Doctors: 15
- Patients: 200
- Appointments: 500
- Treatments: 350
- Invoices: 300
""")