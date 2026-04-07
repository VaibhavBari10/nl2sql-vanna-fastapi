# NL2SQL Test Results

Q1: How many patients do we have?
SQL: SELECT COUNT(*) AS total_patients FROM patients  
Result: 200  

Q2: List all doctors and their specializations  
SQL: SELECT name, specialization FROM doctors  

Q3: Show total revenue  
SQL: SELECT SUM(total_amount) AS total_revenue FROM invoices  

Q4: Show unpaid invoices  
SQL: SELECT * FROM invoices WHERE status = 'Pending'  

Q5: Which city has the most patients?  
SQL: SELECT city, COUNT(*) AS patient_count FROM patients GROUP BY city ORDER BY patient_count DESC LIMIT 1  
