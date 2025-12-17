"""
Quick verification script for the new languages (abaza and turkish)
"""
import sqlite3

def verify_languages():
    conn = sqlite3.connect('grant_database.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("VERIFYING NEW LANGUAGES")
    print("=" * 60)
    
    # Check columns exist
    cursor.execute('PRAGMA table_info(questions)')
    columns = [row[1] for row in cursor.fetchall()]
    
    print("\n1. Checking if columns exist...")
    abaza_exists = 'abaza' in columns
    turkish_exists = 'turkish' in columns
    
    print(f"   {'✓' if abaza_exists else '✗'} abaza column: {'EXISTS' if abaza_exists else 'MISSING'}")
    print(f"   {'✓' if turkish_exists else '✗'} turkish column: {'EXISTS' if turkish_exists else 'MISSING'}")
    
    if not (abaza_exists and turkish_exists):
        print("\n❌ ERROR: One or both columns are missing!")
        conn.close()
        return False
    
    # Check data coverage
    print("\n2. Checking data coverage...")
    cursor.execute('SELECT COUNT(*) FROM questions')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM questions WHERE abaza IS NOT NULL AND abaza != ""')
    abaza_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM questions WHERE turkish IS NOT NULL AND turkish != ""')
    turkish_count = cursor.fetchone()[0]
    
    print(f"   Total questions: {total}")
    print(f"   Abaza answers: {abaza_count} ({abaza_count/total*100:.1f}% coverage)")
    print(f"   Turkish answers: {turkish_count} ({turkish_count/total*100:.1f}% coverage)")
    
    # Show sample data
    print("\n3. Sample data from new languages...")
    cursor.execute('''
        SELECT question_number, question_text, abaza, turkish 
        FROM questions 
        WHERE (abaza IS NOT NULL AND abaza != "") 
           OR (turkish IS NOT NULL AND turkish != "")
        LIMIT 3
    ''')
    
    for row in cursor.fetchall():
        q_num, q_text, abaza, turkish = row
        print(f"\n   Question {q_num}:")
        print(f"   {q_text[:80]}...")
        if abaza:
            print(f"   Abaza: {abaza[:100]}...")
        if turkish:
            print(f"   Turkish: {turkish[:100]}...")
    
    # Summary
    print("\n" + "=" * 60)
    print("✓ VERIFICATION COMPLETE")
    print("=" * 60)
    print(f"Both languages successfully added to the database!")
    print(f"- Abaza: {abaza_count} answers")
    print(f"- Turkish: {turkish_count} answers")
    
    conn.close()
    return True

if __name__ == '__main__':
    verify_languages()
