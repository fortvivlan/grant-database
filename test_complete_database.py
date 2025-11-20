"""
Comprehensive verification script for the updated database structure.
Tests all 11 languages and HTML content preservation.
"""
import sqlite3
import os

def test_database():
    print("="*80)
    print("DATABASE VERIFICATION TEST")
    print("="*80)
    
    db_path = 'grant_database.db'
    if not os.path.exists(db_path):
        print(f"❌ ERROR: Database file '{db_path}' not found!")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Test 1: Check database structure
    print("\n1. Checking database structure...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    expected_tables = ['groups', 'questions']
    
    if set(expected_tables).issubset(set(tables)):
        print(f"   ✓ Tables: {tables}")
    else:
        print(f"   ❌ Missing tables. Found: {tables}, Expected: {expected_tables}")
        return False
    
    # Test 2: Check language columns
    print("\n2. Checking language columns...")
    cursor.execute("PRAGMA table_info(questions)")
    columns = [col[1] for col in cursor.fetchall()]
    language_columns = [col for col in columns if col not in ('id', 'question_number', 'group_id', 'question_text')]
    
    expected_languages = ['russian', 'muira', 'danish', 'nganasan', 'westcircassian', 
                         'polish', 'bulgarian', 'nanai', 'nornakhichevan', 'udmurt', 'greben']
    
    if set(language_columns) == set(expected_languages):
        print(f"   ✓ All 11 languages present: {sorted(language_columns)}")
    else:
        missing = set(expected_languages) - set(language_columns)
        extra = set(language_columns) - set(expected_languages)
        if missing:
            print(f"   ❌ Missing languages: {missing}")
        if extra:
            print(f"   ⚠ Extra languages: {extra}")
        return False
    
    # Test 3: Count data
    print("\n3. Checking data counts...")
    cursor.execute("SELECT COUNT(*) FROM groups")
    group_count = cursor.fetchone()[0]
    print(f"   Groups: {group_count} (expected: 12)")
    
    cursor.execute("SELECT COUNT(*) FROM questions")
    question_count = cursor.fetchone()[0]
    print(f"   Questions: {question_count} (expected: 97)")
    
    if group_count != 12 or question_count != 97:
        print("   ❌ Data count mismatch!")
        return False
    print("   ✓ Data counts correct")
    
    # Test 4: Check answer counts per language
    print("\n4. Checking answers per language...")
    all_good = True
    for lang in sorted(expected_languages):
        cursor.execute(f'SELECT COUNT(*) FROM questions WHERE {lang} IS NOT NULL AND {lang} != ""')
        count = cursor.fetchone()[0]
        status = "✓" if count > 80 else "⚠"
        print(f"   {status} {lang}: {count} answers")
        if count < 80:
            all_good = False
    
    # Test 5: HTML content preservation
    print("\n5. Checking HTML content preservation...")
    cursor.execute("""
        SELECT question_number, russian 
        FROM questions 
        WHERE russian IS NOT NULL AND russian != "" 
        AND question_number = '1.2'
    """)
    row = cursor.fetchone()
    
    if row:
        question_num, answer = row
        html_tags = ['<i>', '<b>', '<br />', '<sub>', '<sup>']
        found_tags = [tag for tag in html_tags if tag in answer]
        
        if found_tags:
            print(f"   ✓ HTML tags found in question {question_num}: {found_tags}")
            print(f"   ✓ Answer length: {len(answer)} characters")
        else:
            print(f"   ❌ No HTML tags found in question {question_num}")
            print(f"   Sample: {answer[:200]}...")
            all_good = False
    else:
        print("   ❌ Could not find test question 1.2")
        all_good = False
    
    # Test 6: Check new languages have data
    print("\n6. Checking new languages have content...")
    new_languages = ['nanai', 'nornakhichevan', 'udmurt', 'greben']
    for lang in new_languages:
        cursor.execute(f'SELECT COUNT(*) FROM questions WHERE {lang} IS NOT NULL AND {lang} != ""')
        count = cursor.fetchone()[0]
        status = "✓" if count > 0 else "❌"
        print(f"   {status} {lang}: {count} answers")
        if count == 0:
            all_good = False
    
    # Test 7: Sample questions
    print("\n7. Sample questions from different groups...")
    cursor.execute("""
        SELECT q.question_number, g.group_number, g.group_name, q.question_text
        FROM questions q
        JOIN groups g ON q.group_id = g.id
        WHERE g.group_number IN ('1', '5', '10')
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"   ✓ Q{row[0]} (Group {row[1]}): {row[3][:60]}...")
    
    # Test 8: HTML formatting in multiple languages
    print("\n8. Testing HTML across different languages...")
    test_question = '2.4.2'
    for lang in ['russian', 'danish', 'muira']:
        cursor.execute(f'SELECT {lang} FROM questions WHERE question_number = ?', (test_question,))
        row = cursor.fetchone()
        if row and row[0]:
            has_html = '<' in row[0] and '>' in row[0]
            status = "✓" if has_html else "⚠"
            print(f"   {status} {lang}: {'HTML detected' if has_html else 'Plain text'} ({len(row[0])} chars)")
    
    conn.close()
    
    print("\n" + "="*80)
    if all_good:
        print("✓ ALL TESTS PASSED!")
    else:
        print("⚠ SOME TESTS HAD WARNINGS")
    print("="*80)
    
    return all_good

if __name__ == '__main__':
    success = test_database()
    exit(0 if success else 1)
