import sqlite3

conn = sqlite3.connect('grant_database.db')
cursor = conn.cursor()

# Check columns
cursor.execute('PRAGMA table_info(questions)')
cols = [row[1] for row in cursor.fetchall()]
print('Columns:', cols)

# Count Bulgarian answers
cursor.execute('SELECT COUNT(*) FROM questions WHERE bulgarian IS NOT NULL AND bulgarian != ""')
count = cursor.fetchone()[0]
print(f'Questions with Bulgarian answers: {count}')

# Show a sample
cursor.execute('SELECT question_number, SUBSTR(bulgarian, 1, 100) FROM questions WHERE bulgarian IS NOT NULL AND bulgarian != "" LIMIT 1')
sample = cursor.fetchone()
if sample:
    print(f'\nSample (Question {sample[0]}):')
    print(sample[1] + '...')

conn.close()
