import sqlite3
import re
from typing import Dict, List, Tuple

def parse_file(filename: str, is_quest_file: bool = False) -> Dict[str, str]:
    """Parse a text file and extract questions with their numbers.
    
    For language files (not quest.txt), sub-questions like 5.3.1, 5.3.2 that don't exist 
    in quest.txt will be merged into their parent question (5.3) as plain text.
    
    Skips section headers (single digit numbers like "1.", "2.", etc.) as these are group titles.
    """
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
            # A new question starts with a number at the beginning of a line
            number_part = match.group(1)
            text_part = match.group(2).strip()
            
            # Skip section headers (single digit numbers like "1", "2", etc.)
            # These are group titles, not actual questions
            if '.' not in number_part:
                # This is a section header, not a question - skip it
                if current_number:
                    questions[current_number] = ' '.join(current_text).strip()
                current_number = None
                current_text = []
                continue
            
            # Determine if this is a new question or continuation
            # New question: starts with number pattern at line start
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

def merge_subquestions(language_data: Dict[str, str], quest_data: Dict[str, str]) -> Dict[str, str]:
    """Merge sub-questions that don't exist in quest.txt into their parent questions.
    
    For example, if 5.3.1, 5.3.2 exist in language file but not in quest.txt,
    merge them into 5.3 as: "5.3 text. 5.3.1: sub text. 5.3.2: sub text."
    """
    merged = {}
    quest_numbers = set(quest_data.keys())
    
    for num, text in language_data.items():
        if num in quest_numbers:
            # This question exists in quest.txt, keep it as is
            merged[num] = text
        else:
            # This is a sub-question not in quest.txt, find parent
            parts = num.split('.')
            # Try to find parent by removing last component
            while len(parts) > 1:
                parts = parts[:-1]
                parent_num = '.'.join(parts)
                if parent_num in quest_numbers:
                    # Append to parent question
                    if parent_num not in merged:
                        merged[parent_num] = language_data.get(parent_num, '')
                    # Add sub-question as continuation
                    if merged[parent_num]:
                        merged[parent_num] += f" {num}: {text}"
                    else:
                        merged[parent_num] = f"{num}: {text}"
                    break
    
    return merged

def get_group_number(question_number: str) -> str:
    """Extract the top-level group number from a question number."""
    return question_number.split('.')[0]

def create_database(db_path: str):
    """Create SQLite database with questionnaire data."""
    
    print("Parsing files...")
    quest_data = parse_file('quest.txt', is_quest_file=True)
    russian_data = parse_file('russian.txt')
    danish_data = parse_file('danish.txt')
    muira_data = parse_file('muira.txt')
    nganasan_data = parse_file('nganasan.txt')
    
    print(f"Found {len(quest_data)} questions in quest.txt")
    print(f"Found {len(russian_data)} entries in russian.txt")
    print(f"Found {len(danish_data)} entries in danish.txt")
    print(f"Found {len(muira_data)} entries in muira.txt")
    print(f"Found {len(nganasan_data)} entries in nganasan.txt")
    
    # Merge sub-questions into parent questions
    print("\nMerging sub-questions into parent questions...")
    russian_data = merge_subquestions(russian_data, quest_data)
    danish_data = merge_subquestions(danish_data, quest_data)
    muira_data = merge_subquestions(muira_data, quest_data)
    nganasan_data = merge_subquestions(nganasan_data, quest_data)
    
    # Create database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_number TEXT UNIQUE NOT NULL,
            group_number TEXT NOT NULL,
            question_text TEXT NOT NULL,
            russian TEXT,
            danish TEXT,
            muira TEXT,
            nganasan TEXT
        )
    ''')
    
    # Create index for faster group queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_group_number ON questions(group_number)
    ''')
    
    # Insert data
    print("\nInserting data into database...")
    for question_num, question_text in quest_data.items():
        group_num = get_group_number(question_num)
        
        # Get language data (use empty string if not found)
        russian_text = russian_data.get(question_num, '')
        danish_text = danish_data.get(question_num, '')
        muira_text = muira_data.get(question_num, '')
        nganasan_text = nganasan_data.get(question_num, '')
        
        try:
            cursor.execute('''
                INSERT INTO questions 
                (question_number, group_number, question_text, russian, danish, muira, nganasan)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (question_num, group_num, question_text, russian_text, danish_text, muira_text, nganasan_text))
        except sqlite3.IntegrityError as e:
            print(f"ERROR: Duplicate question number: {question_num}")
            print(f"  Text: {question_text[:100]}")
            raise
    
    conn.commit()
    
    # Print statistics
    cursor.execute('SELECT COUNT(*) FROM questions')
    total_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT group_number) FROM questions')
    group_count = cursor.fetchone()[0]
    
    print(f"\nDatabase created successfully!")
    print(f"Total questions: {total_count}")
    print(f"Total groups: {group_count}")
    
    # Show some examples
    print("\nExample queries:")
    print("\n1. First 3 questions:")
    cursor.execute('SELECT question_number, question_text FROM questions LIMIT 3')
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1][:80]}...")
    
    print("\n2. Questions in group 1:")
    cursor.execute('SELECT COUNT(*) FROM questions WHERE group_number = "1"')
    print(f"  Count: {cursor.fetchone()[0]}")
    
    print("\n3. Random question from group 2:")
    cursor.execute('SELECT question_number, question_text FROM questions WHERE group_number = "2" ORDER BY RANDOM() LIMIT 1')
    row = cursor.fetchone()
    if row:
        print(f"  {row[0]}: {row[1][:80]}...")
    
    conn.close()

if __name__ == '__main__':
    create_database('grant_database.db')
    print("\nDatabase file created: grant_database.db")
