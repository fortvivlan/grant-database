"""
Script to add a new language to the database
Usage: python add_language.py <language_name> <txt_file_path>
Example: python add_language.py french french.txt
"""

import sqlite3
import sys
import re
from typing import Dict

def parse_file(filename: str) -> Dict[str, str]:
    """Parse a text file and extract questions with their numbers."""
    # Try different encodings
    encodings = ['utf-8', 'utf-16', 'cp1251', 'latin-1']
    content = None
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                content = f.read()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if content is None:
        raise ValueError(f"Could not decode file {filename} with any known encoding")
    
    questions = {}
    current_number = None
    current_text = []
    
    lines = content.split('\n')
    
    for line in lines:
        # Match question numbers like "1.1.", "2.4.1.", etc.
        # Also match without the period after the number (for muira)
        match = re.match(r'^(\d+(?:\.\d+)*)[.\s]\s*(.*)$', line)
        
        if match:
            # Check if this is actually a new question number or just continuation
            number_part = match.group(1)
            text_part = match.group(2).strip()
            
            # Determine if this is a new question or continuation
            is_new_question = line.strip().startswith(number_part)
            
            if is_new_question:
                # Save previous question if exists
                if current_number:
                    questions[current_number] = ' '.join(current_text).strip()
                
                current_number = number_part
                current_text = [text_part] if text_part else []
            elif current_number and line.strip():
                # Continue multiline questions - join with space
                current_text.append(line.strip())
        elif current_number and line.strip():
            # Continue multiline questions - join with space
            current_text.append(line.strip())
    
    # Save last question
    if current_number:
        questions[current_number] = ' '.join(current_text).strip()
    
    return questions

def add_language_column(db_path: str, language_name: str):
    """Add a new language column to the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(questions)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if language_name.lower() in columns:
        print(f"Warning: Column '{language_name}' already exists. Will update existing data.")
        conn.close()
        return True
    
    # Add new column
    cursor.execute(f'ALTER TABLE questions ADD COLUMN {language_name.lower()} TEXT')
    conn.commit()
    conn.close()
    print(f"✓ Added column '{language_name}' to database")
    return False

def update_language_data(db_path: str, language_name: str, language_data: Dict[str, str]):
    """Update the database with language data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    updated_count = 0
    missing_questions = []
    
    for question_num, answer in language_data.items():
        cursor.execute(
            f'UPDATE questions SET {language_name.lower()} = ? WHERE question_number = ?',
            (answer, question_num)
        )
        if cursor.rowcount > 0:
            updated_count += 1
        else:
            missing_questions.append(question_num)
    
    conn.commit()
    conn.close()
    
    return updated_count, missing_questions

def main():
    if len(sys.argv) != 3:
        print("Usage: python add_language.py <language_name> <txt_file_path>")
        print("Example: python add_language.py french french.txt")
        sys.exit(1)
    
    language_name = sys.argv[1]
    txt_file = sys.argv[2]
    db_path = 'grant_database.db'
    
    print("=" * 60)
    print(f"ADDING LANGUAGE: {language_name.upper()}")
    print("=" * 60)
    
    # Validate language name (only letters, numbers, underscore)
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', language_name):
        print("Error: Language name must start with a letter and contain only letters, numbers, and underscores")
        sys.exit(1)
    
    # Parse the file
    print(f"\n[1/4] Parsing {txt_file}...")
    try:
        language_data = parse_file(txt_file)
        print(f"✓ Found {len(language_data)} entries")
    except FileNotFoundError:
        print(f"Error: File '{txt_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)
    
    # Add column to database
    print(f"\n[2/4] Adding '{language_name}' column to database...")
    column_exists = add_language_column(db_path, language_name)
    
    # Update data
    print(f"\n[3/4] Updating database with {language_name} data...")
    updated_count, missing_questions = update_language_data(db_path, language_name, language_data)
    print(f"✓ Updated {updated_count} questions")
    
    if missing_questions:
        print(f"\nWarning: {len(missing_questions)} question numbers in the file don't exist in database:")
        for q in missing_questions[:10]:  # Show first 10
            print(f"  - {q}")
        if len(missing_questions) > 10:
            print(f"  ... and {len(missing_questions) - 10} more")
    
    # Verify
    print(f"\n[4/4] Verifying data...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM questions WHERE {language_name.lower()} IS NOT NULL AND {language_name.lower()} != ""')
    count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM questions')
    total = cursor.fetchone()[0]
    conn.close()
    
    print(f"✓ {language_name} coverage: {count}/{total} ({count/total*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully added {language_name} to the database!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run 'python test_database.py' to verify")
    print("2. Run 'python export_to_postgres.py' to update PostgreSQL schema")
    print("3. Update your API/interface to include the new language")

if __name__ == '__main__':
    main()
