# SQL Injection (SQLi)

Occurs when untrusted user input is concatenated into database queries.

**Impact:**
- Data theft
- Data modification
- Authentication bypass
- Remote code execution

**Prevention:**
- Use parameterized queries (prepared statements)
- Implement input validation
- Apply least privilege to database accounts
- Use ORM frameworks

**Example:**
```python
# Vulnerable
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# Safe
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

---
*Generated on 2026-07-16*