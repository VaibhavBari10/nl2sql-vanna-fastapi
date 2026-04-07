"""from vanna_setup import get_agent

agent = get_agent()

# Access memory
agent, memory = get_agent()

examples = [
    ("How many patients do we have?", "SELECT COUNT(*) AS total_patients FROM patients"),
    ("List all doctors and their specializations", "SELECT name, specialization FROM doctors"),
    ("Show total revenue", "SELECT SUM(total_amount) AS total_revenue FROM invoices"),
    ("Show unpaid invoices", "SELECT * FROM invoices WHERE status = 'Pending'"),
    ("Which city has the most patients?", "SELECT city, COUNT(*) AS patient_count FROM patients GROUP BY city ORDER BY patient_count DESC LIMIT 1"),
    ("Top 5 patients by spending", "SELECT patient_id, SUM(total_amount) AS total FROM invoices GROUP BY patient_id ORDER BY total DESC LIMIT 5"),
    ("Show appointments by status", "SELECT status, COUNT(*) FROM appointments GROUP BY status"),
    ("Show revenue by month", "SELECT strftime('%Y-%m', invoice_date) AS month, SUM(total_amount) FROM invoices GROUP BY month"),
    ("Average treatment cost", "SELECT AVG(cost) FROM treatments"),
    ("Busiest doctor", "SELECT doctor_id, COUNT(*) AS total FROM appointments GROUP BY doctor_id ORDER BY total DESC LIMIT 1")
]

for question, sql in examples:
    try:
        memory.save_correct_tool_use(
            tool_name="RunSqlTool",
            args={"query": sql},
            question=question
        )
        print(f"Learned: {question}")
    except Exception as e:
        print(f"Error seeding {question}: {e}")

print("Memory seeding completed")"""

print("Manual memory seeding not supported in Vanna 2.0.2")
print("Using automatic learning via built-in memory tools")