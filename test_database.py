"""
Test script to verify the database structure and content
"""
import sqlite3

def test_database(db_path='grant_database.db'):
    """Run tests on the database."""
    print("=" * 60)
    print("GRANT DATABASE TEST SUITE")
    print("=" * 60)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Check table exists
    tests_total += 1
    print("\n[TEST 1] Checking if 'questions' table exists...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='questions'")
    if cursor.fetchone():
        print("✓ PASS: Table 'questions' exists")
        tests_passed += 1
    else:
        print("✗ FAIL: Table 'questions' not found")
    
    # Test 2: Check column structure
    tests_total += 1
    print("\n[TEST 2] Checking table structure...")
    cursor.execute("PRAGMA table_info(questions)")
    columns = [col[1] for col in cursor.fetchall()]
    expected_columns = ['id', 'question_number', 'group_number', 'question_text', 
                       'russian', 'danish', 'muira', 'nganasan']
    if set(expected_columns).issubset(set(columns)):
        print(f"✓ PASS: All expected columns present: {columns}")
        tests_passed += 1
    else:
        print(f"✗ FAIL: Missing columns. Expected: {expected_columns}, Found: {columns}")
    
    # Test 3: Check data count
    tests_total += 1
    print("\n[TEST 3] Checking total record count...")
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_count = cursor.fetchone()[0]
    if total_count > 0:
        print(f"✓ PASS: Database contains {total_count} questions")
        tests_passed += 1
    else:
        print("✗ FAIL: Database is empty")
    
    # Test 4: Check groups
    tests_total += 1
    print("\n[TEST 4] Checking groups...")
    cursor.execute("SELECT COUNT(DISTINCT group_number) FROM questions")
    group_count = cursor.fetchone()[0]
    if group_count > 0:
        print(f"✓ PASS: Found {group_count} distinct groups")
        tests_passed += 1
        
        # Show group distribution
        cursor.execute("""
            SELECT group_number, COUNT(*) as count 
            FROM questions 
            GROUP BY group_number 
            ORDER BY group_number
        """)
        print("\n  Group distribution:")
        for row in cursor.fetchall():
            print(f"    Group {row[0]}: {row[1]} questions")
    else:
        print("✗ FAIL: No groups found")
    
    # Test 5: Check for duplicate question numbers
    tests_total += 1
    print("\n[TEST 5] Checking for duplicate question numbers...")
    cursor.execute("""
        SELECT question_number, COUNT(*) as count 
        FROM questions 
        GROUP BY question_number 
        HAVING count > 1
    """)
    duplicates = cursor.fetchall()
    if len(duplicates) == 0:
        print("✓ PASS: No duplicate question numbers")
        tests_passed += 1
    else:
        print(f"✗ FAIL: Found {len(duplicates)} duplicate question numbers:")
        for dup in duplicates:
            print(f"    {dup[0]}: {dup[1]} occurrences")
    
    # Test 6: Check language data coverage
    tests_total += 1
    print("\n[TEST 6] Checking language data coverage...")
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN russian != '' AND russian IS NOT NULL THEN 1 ELSE 0 END) as russian,
            SUM(CASE WHEN danish != '' AND danish IS NOT NULL THEN 1 ELSE 0 END) as danish,
            SUM(CASE WHEN muira != '' AND muira IS NOT NULL THEN 1 ELSE 0 END) as muira,
            SUM(CASE WHEN nganasan != '' AND nganasan IS NOT NULL THEN 1 ELSE 0 END) as nganasan
        FROM questions
    """)
    coverage = cursor.fetchone()
    total = coverage[0]
    
    print(f"  Total questions: {total}")
    print(f"  Russian coverage: {coverage[1]} ({coverage[1]/total*100:.1f}%)")
    print(f"  Danish coverage: {coverage[2]} ({coverage[2]/total*100:.1f}%)")
    print(f"  Muira coverage: {coverage[3]} ({coverage[3]/total*100:.1f}%)")
    print(f"  Nganasan coverage: {coverage[4]} ({coverage[4]/total*100:.1f}%)")
    
    if all(c > 0 for c in coverage[1:]):
        print("✓ PASS: All languages have some data")
        tests_passed += 1
    else:
        print("✗ FAIL: Some languages have no data")
    
    # Test 7: Check for NULL values in required fields
    tests_total += 1
    print("\n[TEST 7] Checking for NULL values in required fields...")
    cursor.execute("""
        SELECT COUNT(*) FROM questions 
        WHERE question_number IS NULL 
           OR group_number IS NULL 
           OR question_text IS NULL
    """)
    null_count = cursor.fetchone()[0]
    if null_count == 0:
        print("✓ PASS: No NULL values in required fields")
        tests_passed += 1
    else:
        print(f"✗ FAIL: Found {null_count} records with NULL required fields")
    
    # Test 8: Sample data check
    tests_total += 1
    print("\n[TEST 8] Sampling random question...")
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    sample = cursor.fetchone()
    if sample:
        print("✓ PASS: Successfully retrieved random question")
        print(f"  Question {sample[1]}: {sample[3][:100]}...")
        tests_passed += 1
    else:
        print("✗ FAIL: Could not retrieve sample")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {tests_passed}/{tests_total} tests passed")
    print("=" * 60)
    
    if tests_passed == tests_total:
        print("✓ ALL TESTS PASSED! Database is ready for deployment.")
    else:
        print(f"✗ SOME TESTS FAILED. Please review the issues above.")
    
    conn.close()
    
    return tests_passed == tests_total

if __name__ == '__main__':
    success = test_database()
    exit(0 if success else 1)
