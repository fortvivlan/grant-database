import sqlite3

conn = sqlite3.connect('grant_database.db')
cursor = conn.cursor()

# Check all language columns
cursor.execute('PRAGMA table_info(questions)')
columns = [col[1] for col in cursor.fetchall() if col[1] not in ('id', 'question_number', 'group_id', 'question_text')]
print(f"Language columns in database: {columns}\n")

# Count answers for each language
print("Answer counts per language:")
for lang in columns:
    cursor.execute(f'SELECT COUNT(*) FROM questions WHERE {lang} IS NOT NULL AND {lang} != ""')
    count = cursor.fetchone()[0]
    print(f"  {lang}: {count}")

# Show sample with HTML formatting
print("\n" + "="*80)
print("Sample question with HTML content:")
print("="*80)
cursor.execute('SELECT question_number, question_text, russian FROM questions WHERE russian != "" AND LENGTH(russian) > 100 LIMIT 1')
row = cursor.fetchone()
if row:
    print(f"\nQuestion {row[0]}:")
    print(f"Text: {row[1][:100]}...")
    print(f"\nRussian answer (first 500 chars):")
    print(row[2][:500])
    print("...")
    
    # Check if HTML tags are present
    if '<' in row[2] and '>' in row[2]:
        print("\n✓ HTML tags detected - content is preserved!")
    else:
        print("\n✗ No HTML tags found - content may have been converted")

# Check a specific question with known HTML content
print("\n" + "="*80)
print("Checking question 1.2 (should have complex HTML):")
print("="*80)
cursor.execute('SELECT russian FROM questions WHERE question_number = "1.2"')
row = cursor.fetchone()
if row and row[0]:
    print(f"Length: {len(row[0])} characters")
    print(f"First 400 chars:\n{row[0][:400]}")
    print("...")
    
    # Check for HTML elements
    html_elements = ['<i>', '<b>', '<br />', '<sub>', '<sup>']
    found_elements = [elem for elem in html_elements if elem in row[0]]
    print(f"\nHTML elements found: {found_elements}")

conn.close()
