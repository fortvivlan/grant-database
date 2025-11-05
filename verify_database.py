import sqlite3

# Connect to database
conn = sqlite3.connect('grant_database.db')
cursor = conn.cursor()

# Check a few entries to verify the fix
print("Checking database entries to verify language columns contain only answers:\n")
print("="*100)

# Check question 1.1
cursor.execute('SELECT question_number, question_text, russian, danish FROM questions WHERE question_number = "1.1"')
row = cursor.fetchone()
print(f"\nQuestion Number: {row[0]}")
print(f"Question Text: {row[1][:150]}...")
print(f"\nRussian (should be answer only): {row[2][:150]}...")
print(f"\nDanish (should be answer only): {row[3][:150]}...")

print("\n" + "="*100)

# Check question 2.1
cursor.execute('SELECT question_number, question_text, russian, danish FROM questions WHERE question_number = "2.1"')
row = cursor.fetchone()
print(f"\nQuestion Number: {row[0]}")
print(f"Question Text: {row[1][:150]}...")
print(f"\nRussian (should be answer only): {row[2][:150]}...")
print(f"\nDanish (should be answer only): {row[3][:150]}...")

print("\n" + "="*100)

# Check question 2.8
cursor.execute('SELECT question_number, question_text, russian, danish FROM questions WHERE question_number = "2.8"')
row = cursor.fetchone()
print(f"\nQuestion Number: {row[0]}")
print(f"Question Text: {row[1][:150]}...")
print(f"\nRussian (should be answer only): {row[2][:200]}...")
print(f"\nDanish (should be answer only): {row[3][:200]}...")

# Count entries with data
cursor.execute('SELECT COUNT(*) FROM questions WHERE russian != ""')
russian_count = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM questions WHERE danish != ""')
danish_count = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM questions WHERE muira != ""')
muira_count = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM questions WHERE nganasan != ""')
nganasan_count = cursor.fetchone()[0]

print("\n" + "="*100)
print("\nStatistics:")
print(f"Questions with Russian answers: {russian_count}/97")
print(f"Questions with Danish answers: {danish_count}/97")
print(f"Questions with Muira answers: {muira_count}/97")
print(f"Questions with Nganasan answers: {nganasan_count}/97")

conn.close()
