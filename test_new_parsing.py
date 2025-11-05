import sqlite3

conn = sqlite3.connect('grant_database.db')
cursor = conn.cursor()

print("Verifying new Excel-based parsing approach:\n")
print("="*100)

# Check question 1.1
cursor.execute('SELECT question_number, question_text, russian, danish, muira FROM questions WHERE question_number = "1.1"')
row = cursor.fetchone()
print(f"\n✓ Question 1.1")
print(f"Question: {row[1]}")
print(f"\nRussian answer (first 200 chars): {row[2][:200] if row[2] else '(empty)'}...")
print(f"\nDanish answer (first 200 chars): {row[3][:200] if row[3] else '(empty)'}...")
print(f"\nMuira answer (first 200 chars): {row[4][:200] if row[4] else '(empty)'}...")

print("\n" + "="*100)

# Check question 2.12 which should have "будет уточнено"
cursor.execute('SELECT question_number, question_text, russian, muira FROM questions WHERE question_number = "2.12"')
row = cursor.fetchone()
print(f"\n✓ Question 2.12 (should have 'будет уточнено' answers)")
print(f"Question: {row[1]}")
print(f"\nRussian answer: {row[2] if row[2] else '(empty)'}")
print(f"Muira answer: {row[3] if row[3] else '(empty)'}")

print("\n" + "="*100)

# Check a longer answer
cursor.execute('SELECT question_number, question_text, russian FROM questions WHERE question_number = "1.2"')
row = cursor.fetchone()
print(f"\n✓ Question 1.2 (longer answer)")
print(f"Question: {row[1]}")
print(f"\nRussian answer (first 300 chars):\n{row[2][:300] if row[2] else '(empty)'}...")

print("\n" + "="*100)

# Check coverage statistics
print("\n✓ Coverage Statistics:")
cursor.execute('SELECT COUNT(*) FROM questions')
total = cursor.fetchone()[0]

for lang in ['russian', 'danish', 'muira', 'nganasan', 'polish', 'circassian']:
    cursor.execute(f'SELECT COUNT(*) FROM questions WHERE {lang} != ""')
    count = cursor.fetchone()[0]
    percentage = (count / total * 100) if total > 0 else 0
    print(f"{lang.capitalize()}: {count}/{total} ({percentage:.1f}%)")

# Check for questions without any answers
cursor.execute('''SELECT question_number, question_text FROM questions 
                  WHERE russian = "" AND danish = "" AND muira = "" 
                  AND nganasan = "" AND polish = "" AND circassian = ""''')
no_answer_questions = cursor.fetchall()
if no_answer_questions:
    print(f"\n⚠ Questions with no answers in any language: {len(no_answer_questions)}")
    for q in no_answer_questions[:5]:
        print(f"  - {q[0]}: {q[1][:80]}...")
else:
    print(f"\n✓ All questions have at least one answer!")

conn.close()
