"""
Show all languages currently in the database with their coverage statistics
"""
import sqlite3
import os
import glob
import re

def show_database_languages():
    """Display all languages in the database with coverage stats."""
    db_path = 'grant_database.db'
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found: {db_path}")
        print("Run 'python create_database.py' first")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all column names
    cursor.execute('PRAGMA table_info(questions)')
    columns = cursor.fetchall()
    
    # Filter for language columns (exclude id, question_number, group_id, question_text)
    system_columns = {'id', 'question_number', 'group_id', 'question_text'}
    language_columns = [col[1] for col in columns if col[1] not in system_columns]
    
    # Get total questions
    cursor.execute('SELECT COUNT(*) FROM questions')
    total_questions = cursor.fetchone()[0]
    
    print("=" * 70)
    print("LANGUAGES IN DATABASE")
    print("=" * 70)
    print(f"\nTotal questions: {total_questions}")
    print(f"Total languages: {len(language_columns)}\n")
    
    # Show coverage for each language
    print(f"{'#':<4} {'Language':<25} {'Answers':<10} {'Coverage':<10}")
    print("-" * 70)
    
    for i, lang_name in enumerate(language_columns, 1):
        cursor.execute(f'SELECT COUNT(*) FROM questions WHERE {lang_name} IS NOT NULL AND {lang_name} != ""')
        count = cursor.fetchone()[0]
        percentage = (count / total_questions * 100) if total_questions > 0 else 0
        print(f"{i:<4} {lang_name:<25} {count:>3}/{total_questions:<5} {percentage:>5.1f}%")
    
    conn.close()
    
    print("\n" + "=" * 70)
    
    # Also show HTML files in languages/ folder
    print("\nHTML FILES IN languages/ FOLDER")
    print("=" * 70)
    
    pattern = os.path.join('languages', '[0-9][0-9]-*.html')
    files = glob.glob(pattern)
    files.sort()
    
    print(f"\nTotal files: {len(files)}\n")
    
    for filepath in files:
        filename = os.path.basename(filepath)
        match = re.match(r'^(\d+)-(.+)\.html$', filename)
        if match:
            number = match.group(1)
            lang_name = match.group(2)
            # Check if in database
            db_name = lang_name.lower().replace('-', '_')
            in_db = "✓" if db_name in language_columns else "✗"
            print(f"  {in_db} {number}. {lang_name:<25} ({filename})")
    
    print()

if __name__ == '__main__':
    show_database_languages()
