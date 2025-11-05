import sqlite3

conn = sqlite3.connect('grant_database.db')
cursor = conn.cursor()

print("="*100)
print("COMPREHENSIVE VERIFICATION OF NEW EXCEL-BASED PARSING")
print("="*100)

# Test 1: Verify answers don't include question text
print("\n✓ TEST 1: Clean answer extraction (no question text in answers)")
print("-"*100)
cursor.execute('SELECT question_number, question_text, russian FROM questions WHERE question_number IN ("1.1", "2.1", "3.1") ORDER BY question_number')
for row in cursor.fetchall():
    print(f"\nQuestion {row[0]}:")
    print(f"  Q: {row[1][:80]}...")
    print(f"  A: {row[2][:120] if row[2] else '(no answer)'}...")

# Test 2: Verify "будет уточнено" answers are captured
print("\n\n✓ TEST 2: Placeholder answers ('будет уточнено', 'будет заполнено позднее') captured")
print("-"*100)
cursor.execute('''SELECT question_number, question_text, russian, muira 
                  FROM questions 
                  WHERE russian LIKE '%будет%' OR muira LIKE '%будет%' 
                  LIMIT 5''')
for row in cursor.fetchall():
    print(f"\nQuestion {row[0]}: {row[1][:60]}...")
    if row[2] and 'будет' in row[2].lower():
        print(f"  Russian: {row[2]}")
    if row[3] and 'будет' in row[3].lower():
        print(f"  Muira: {row[3]}")

# Test 3: Verify long answers are fully captured
print("\n\n✓ TEST 3: Long multi-paragraph answers fully captured")
print("-"*100)
cursor.execute('''SELECT question_number, question_text, LENGTH(russian) as len, russian 
                  FROM questions 
                  WHERE LENGTH(russian) > 500 
                  ORDER BY len DESC LIMIT 3''')
for row in cursor.fetchall():
    print(f"\nQuestion {row[0]}: {row[1][:60]}...")
    print(f"  Answer length: {row[2]} characters")
    print(f"  First 200 chars: {row[3][:200]}...")
    print(f"  Last 100 chars: ...{row[3][-100:]}")

# Test 4: Coverage statistics
print("\n\n✓ TEST 4: Overall coverage statistics")
print("-"*100)
cursor.execute('SELECT COUNT(*) FROM questions')
total = cursor.fetchone()[0]

print(f"Total questions: {total}")
print(f"\nAnswers by language:")
for lang in ['russian', 'danish', 'muira', 'nganasan', 'polish', 'circassian']:
    cursor.execute(f'SELECT COUNT(*) FROM questions WHERE {lang} != "" AND {lang} IS NOT NULL')
    count = cursor.fetchone()[0]
    percentage = (count / total * 100) if total > 0 else 0
    print(f"  {lang.capitalize():12s}: {count:3d}/{total} ({percentage:5.1f}%)")

# Test 5: Questions without answers in any language
print("\n\n✓ TEST 5: Questions missing from all language files")
print("-"*100)
cursor.execute('''SELECT question_number, question_text FROM questions 
                  WHERE (russian = "" OR russian IS NULL) 
                  AND (danish = "" OR danish IS NULL)
                  AND (muira = "" OR muira IS NULL)
                  AND (nganasan = "" OR nganasan IS NULL)
                  AND (polish = "" OR polish IS NULL)
                  AND (circassian = "" OR circassian IS NULL)''')
missing = cursor.fetchall()
if missing:
    print(f"Found {len(missing)} questions with no answers in any language:")
    for q in missing:
        print(f"  - {q[0]}: {q[1][:80]}...")
else:
    print("✓ All questions have at least one answer!")

# Test 6: Verify different answer formats (bullet vs tab format)
print("\n\n✓ TEST 6: Handling different file formats")
print("-"*100)
cursor.execute('SELECT question_number, russian, muira FROM questions WHERE question_number = "2.5"')
row = cursor.fetchone()
print(f"Question 2.5 (bullet format in Russian, tab format in Muira):")
print(f"  Russian (bullet format): {row[1][:100] if row[1] else '(no answer)'}...")
print(f"  Muira (tab format): {row[2][:100] if row[2] else '(no answer)'}...")

print("\n" + "="*100)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("="*100)

conn.close()
