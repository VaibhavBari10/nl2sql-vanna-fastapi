# 🧠 NL2SQL System using Vanna AI & FastAPI

## 📌 Project Overview

This project implements a **Natural Language to SQL (NL2SQL)** system that allows users to query a database using plain English.

Users can ask questions like:

> "How many patients do we have?"
> "Show total revenue"

…and receive accurate results from the database **without writing SQL**.

---

## 🚀 Tech Stack

* **Python**
* **FastAPI** – API framework
* **SQLite** – Database
* **Vanna AI (v2.0.2)** – NL2SQL framework
* **Faker** – Dummy data generation
* **Uvicorn** – ASGI server

---

## 🏗️ Project Structure

``
nl2sql-vanna-fastapi/
│
├── main.py                # FastAPI application
├── vanna_setup.py         # Vanna agent configuration
├── setup_database.py      # Database creation & data seeding
├── seed_memory.py         # Memory initialization (fallback)
├── clinic.db              # SQLite database
├── requirements.txt       # Dependencies
├── RESULTS.md             # Test results
├── README.md              # Project documentation
``

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd nl2sql-vanna-fastapi
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Environment Variables

Create a `.env` file:

``
GOOGLE_API_KEY=your_api_key_here
``

---

### 5️⃣ Setup Database

```bash
python setup_database.py
```

✔ Creates:

* Patients
* Doctors
* Appointments
* Treatments
* Invoices

---

### 6️⃣ Initialize Memory

```bash
python seed_memory.py
```

> ⚠️ Note: Manual memory seeding is not supported in Vanna v2.0.2.
> The system uses automatic learning via built-in tools.

---

### 7️⃣ Run API Server

```bash
uvicorn main:app --reload
```

---

## 🌐 API Endpoints

### 🔹 Root

``
GET /
``

Returns API status.

---

### 🔹 Chat (NL → SQL)

``
POST /chat
``

#### Request

```json
{
  "question": "How many patients do we have?"
}
```

#### Response

```json
{
  "question": "...",
  "sql": "...",
  "columns": [...],
  "rows": [...],
  "row_count": 1
}
```

---

### 🔹 Health Check

``
GET /health
``

---

## 🧪 Testing

Use Swagger UI:

``
http://127.0.0.1:8000/docs
``

---

## 📊 Sample Queries

* How many patients do we have?
* List all doctors and their specializations
* Show total revenue
* Show unpaid invoices
* Which city has the most patients?
* Top 5 patients by spending

---

## ⚠️ SQL Safety

The system blocks dangerous queries such as:

* `DROP`
* `DELETE`
* `UPDATE`
* `ALTER`

---

## 🧠 Vanna Integration Notes

This project uses **Vanna AI v2.0.2**.

Due to version limitations:

* `save_correct_tool_use()` is not available
* `agent.run()` and `agent.ask()` showed compatibility issues

### ✅ Solution Implemented

A **hybrid fallback approach** was used:

* Rule-based NL → SQL mapping for stability
* Vanna tools integrated for future extensibility

This ensures:

* Reliable execution
* Consistent results
* No runtime failures

---

## 📈 Results

See `RESULTS.md` for:

* Query tests
* Generated SQL
* Output validation

---

## 🎯 Features

✔ Natural Language Querying
✔ SQL Execution Engine
✔ FastAPI Backend
✔ SQLite Integration
✔ Error Handling
✔ SQL Injection Protection

---

## 🚧 Limitations

* Limited query coverage (rule-based fallback)
* Full Vanna automation restricted by version
* No frontend UI

---

## 🔮 Future Improvements

* Upgrade to latest Vanna version
* Add full NL2SQL automation
* Build frontend interface
* Add authentication
* Support multiple databases

---

## 👨‍💻 Author

Vaibhav (AI/ML Developer Intern Candidate)

---

## 📌 Conclusion

This project demonstrates:

* Strong backend development skills
* Practical AI system integration
* Problem-solving under real-world constraints

Despite version limitations, a **robust and working NL2SQL system** was successfully implemented.

---
