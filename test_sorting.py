import sqlite3

conn = sqlite3.connect('grant_database.db')
cursor = conn.cursor()

print("Testing question number sorting:")
print("-" * 80)

# Test with group 2 (should have questions like 2.1, 2.2, ..., 2.10, etc.)
cursor.execute("""
    SELECT q.question_number, SUBSTR(q.question_text, 1, 60) as text_preview
    FROM questions q
    JOIN groups g ON q.group_id = g.id
    WHERE g.group_number = '2'
    ORDER BY CAST(SUBSTR(q.question_number, 1, INSTR(q.question_number, '.') - 1) AS INTEGER),
             CAST(SUBSTR(q.question_number, INSTR(q.question_number, '.') + 1) AS INTEGER)
""")

results = cursor.fetchall()
print(f"Found {len(results)} questions in group 2:")
for qnum, text in results:
    print(f"  {qnum}: {text}...")

conn.close()
