import sqlite3

conn = sqlite3.connect('grant_database.db')
c = conn.cursor()

# Check quest.txt questions around 11.11
print("Questions in quest.txt around 11.11:")
c.execute('SELECT question_number FROM questions WHERE question_number LIKE "11.1%" ORDER BY question_number')
quest_questions = [row[0] for row in c.fetchall()]
print(f"  {quest_questions}")

# Check if 11.11.1, 11.11.2 exist as separate rows
c.execute('SELECT question_number, SUBSTR(question_text, 1, 80) FROM questions WHERE question_number IN ("11.11", "11.11.1", "11.11.2") ORDER BY question_number')
rows = c.fetchall()
print(f"\n✓ Questions 11.11.x in database ({len(rows)} rows):")
for row in rows:
    print(f"  {row[0]}: {row[1]}")

# Check Russian data for 11.11
c.execute('SELECT question_number, SUBSTR(russian, 1, 200) FROM questions WHERE question_number = "11.11"')
row = c.fetchone()
if row:
    print(f"\n✓ Russian data for 11.11:")
    print(f"  {row[1]}")
    # Check if it contains merged sub-questions
    if "11.11.1" in row[1] or "11.11.2" in row[1] or "11.11.3" in row[1]:
        print("  ✓ Contains merged sub-questions!")
    else:
        print("  ✗ Does NOT contain merged sub-questions")

conn.close()
