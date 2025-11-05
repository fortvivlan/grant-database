import sqlite3

# Connect to database
conn = sqlite3.connect('grant_database.db')
cursor = conn.cursor()

print("Verifying all languages are parsed correctly:\n")
print("="*100)

# Check question 1.1 - verify all languages
cursor.execute('SELECT question_number, question_text, russian, danish, muira, polish, circassian FROM questions WHERE question_number = "1.1"')
row = cursor.fetchone()
print(f"\n✓ Question 1.1")
print(f"Question: {row[1][:100]}...")
print(f"\nRussian: {row[2][:120] if row[2] else '(empty)'}...")
print(f"Danish: {row[3][:120] if row[3] else '(empty)'}...")
print(f"Muira: {row[4][:120] if row[4] else '(empty)'}...")
print(f"Polish: {row[5][:120] if row[5] else '(empty)'}...")
print(f"Circassian: {row[6][:120] if row[6] else '(empty)'}...")

print("\n" + "="*100)

# Check question 2.1 - different format handling
cursor.execute('SELECT question_number, question_text, russian, muira, circassian FROM questions WHERE question_number = "2.1"')
row = cursor.fetchone()
print(f"\n✓ Question 2.1")
print(f"Question: {row[1][:100]}...")
print(f"\nRussian (bullet format): {row[2][:120] if row[2] else '(empty)'}...")
print(f"Muira (tab format): {row[3][:120] if row[3] else '(empty)'}...")
print(f"Circassian (tab format): {row[4][:120] if row[4] else '(empty)'}...")

print("\n" + "="*100)

# Statistics
print("\n✓ Statistics:")
cursor.execute('SELECT COUNT(*) FROM questions WHERE russian != ""')
print(f"Russian answers: {cursor.fetchone()[0]}/97")

cursor.execute('SELECT COUNT(*) FROM questions WHERE danish != ""')
print(f"Danish answers: {cursor.fetchone()[0]}/97")

cursor.execute('SELECT COUNT(*) FROM questions WHERE muira != ""')
print(f"Muira answers: {cursor.fetchone()[0]}/97")

cursor.execute('SELECT COUNT(*) FROM questions WHERE nganasan != ""')
print(f"Nganasan answers: {cursor.fetchone()[0]}/97")

cursor.execute('SELECT COUNT(*) FROM questions WHERE polish != ""')
print(f"Polish answers: {cursor.fetchone()[0]}/97")

cursor.execute('SELECT COUNT(*) FROM questions WHERE circassian != ""')
print(f"Circassian answers: {cursor.fetchone()[0]}/97")

print("\n" + "="*100)

# Check a specific muira entry to see if formatting is correct
cursor.execute('SELECT question_number, muira FROM questions WHERE question_number = "1.2"')
row = cursor.fetchone()
print(f"\n✓ Detailed check - Question 1.2 (Muira tab format):")
print(f"Answer (should start with answer text, not question):")
print(f"{row[1][:200] if row[1] else '(empty)'}...")

conn.close()
