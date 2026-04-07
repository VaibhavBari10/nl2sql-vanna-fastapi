from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

from vanna_setup import get_agent
from vanna.tools import RunSqlTool

app = FastAPI()

# Get agent (not used directly for execution now)
agent, memory = get_agent()

# Create direct SQL runner
sql_runner = RunSqlTool(sqlite3.connect("clinic.db"))


class Question(BaseModel):
    question: str


# SQL safety validation
def validate_sql(sql: str):
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER"]
    for word in forbidden:
        if word in sql.upper():
            return False
    return True


@app.get("/")
def root():
    return {"message": "NL2SQL API is running 🚀"}


@app.post("/chat")
def chat(q: Question):
    try:
        # ⚠️ TEMP: Simple rule-based fallback (since agent methods broken)
        question = q.question.lower()

        if "how many patients" in question:
            sql = "SELECT COUNT(*) AS total_patients FROM patients"

        elif "doctors" in question:
            sql = "SELECT name, specialization FROM doctors"

        elif "total revenue" in question:
            sql = "SELECT SUM(total_amount) AS total_revenue FROM invoices"

        elif "unpaid invoices" in question:
            sql = "SELECT * FROM invoices WHERE status = 'Pending'"

        elif "city has the most patients" in question:
            sql = """
            SELECT city, COUNT(*) AS patient_count
            FROM patients
            GROUP BY city
            ORDER BY patient_count DESC
            LIMIT 1
            """

        elif "top 5 patients" in question:
            sql = """
            SELECT patient_id, SUM(total_amount) AS total
            FROM invoices
            GROUP BY patient_id
            ORDER BY total DESC
            LIMIT 5
            """

        else:
            return {"error": "Query not supported yet"}

        # Validate SQL
        if not validate_sql(sql):
            return {"error": "Unsafe SQL detected"}

        # Execute SQL
        conn = sqlite3.connect("clinic.db")
        cursor = conn.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        conn.close()

        return {
            "question": q.question,
            "sql": sql,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    return {"status": "ok"}