import sqlite3

conn = sqlite3.connect('grant_database.db')
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(questions)')
langs = sorted([c[1] for c in cursor.fetchall() if c[1] not in ('id','question_number','group_id','question_text')])

print('Answer counts per language:')
print('='*50)
for lang in langs:
    cursor.execute(f'SELECT COUNT(*) FROM questions WHERE {lang} IS NOT NULL AND {lang} != ""')
    count = cursor.fetchone()[0]
    print(f'{lang:20s}: {count:3d} answers')

print('='*50)
print(f'Total: {len(langs)} languages')

conn.close()
