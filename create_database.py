import sqlite3
import re
import openpyxl
from typing import Dict, List, Tuple

def parse_excel_questions(excel_path: str) -> Dict[str, str]:
    """Parse quest.xlsx and extract all questions with their numbers and full text.
    
    Returns a dictionary mapping question numbers to their full question text.
    """
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    
    questions = {}
    
    for row in range(1, ws.max_row + 1):
        # Check column 2 (main questions)
        question_cell = ws.cell(row, 2).value
        if question_cell and isinstance(question_cell, str):
            question_text = question_cell.strip()
            # Extract question number (e.g., "1.1.", "2.4.")
            match = re.match(r'^(\d+\.\d+(?:\.\d+)*)[.\s]', question_text)
            if match:
                question_num = match.group(1)
                questions[question_num] = question_text
        
        # Check column 3 (subquestions)
        subquestion_cell = ws.cell(row, 3).value
        if subquestion_cell and isinstance(subquestion_cell, str):
            subquestion_text = subquestion_cell.strip()
            # Extract subquestion number (e.g., "2.4.1.", "2.12.")
            match = re.match(r'^(\d+\.\d+(?:\.\d+)*)[.\s]', subquestion_text)
            if match:
                subquestion_num = match.group(1)
                questions[subquestion_num] = subquestion_text
    
    wb.close()
    return questions

def normalize_question_text(text: str) -> str:
    """Normalize question text for matching: remove extra spaces, normalize whitespace."""
    # Replace multiple spaces/tabs with single space
    text = re.sub(r'[\s]+', ' ', text)
    return text.strip()

def parse_language_file(filename: str, questions: Dict[str, str]) -> Dict[str, str]:
    """Parse a language file by finding question texts and extracting answers between them.
    
    Args:
        filename: Path to the language text file
        questions: Dictionary of question numbers to question texts from Excel
    
    Returns:
        Dictionary mapping question numbers to answer texts
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
    
    answers = {}
    
    # Create a sorted list of questions by their position in the file
    question_positions = []
    
    for question_num, question_text in questions.items():
        # Extract the question number
        match = re.match(r'^(\d+\.\d+(?:\.\d+)*)[.\s\t]', question_text)
        if match:
            number_part = match.group(1)
            
            # Find the question number in the content
            # Pattern: number followed by period, space, or tab
            pattern = r'\b' + re.escape(number_part) + r'[.\s\t]'
            
            for m in re.finditer(pattern, content):
                # Get the line containing this question number
                line_start = content.rfind('\n', 0, m.start()) + 1
                line_end = content.find('\n', m.end())
                if line_end == -1:
                    line_end = len(content)
                
                line_content = content[line_start:line_end]
                
                # Check if this line contains the question (not just the number)
                # by checking if it's long enough and starts with the number
                if line_content.strip().startswith(number_part):
                    # This looks like a question line
                    question_positions.append({
                        'number': question_num,
                        'start': line_start,
                        'end': line_end + 1,  # Include the newline
                        'full_text': question_text
                    })
                    break  # Only take first match
    
    # Sort by position in file
    question_positions.sort(key=lambda x: x['start'])
    
    # Extract text between questions
    for i, question_info in enumerate(question_positions):
        question_num = question_info['number']
        start_pos = question_info['end']
        
        # Find end position (start of next question, or end of file)
        if i + 1 < len(question_positions):
            end_pos = question_positions[i + 1]['start']
        else:
            end_pos = len(content)
        
        # Extract answer text
        answer_text = content[start_pos:end_pos].strip()
        
        # Clean up the answer text
        # Remove leading bullets, newlines, etc.
        answer_text = re.sub(r'^[\s•\n\r]+', '', answer_text)
        answer_text = re.sub(r'[\n\r]+', ' ', answer_text)  # Replace newlines with spaces
        answer_text = re.sub(r'\s+', ' ', answer_text)  # Normalize spaces
        answer_text = answer_text.strip()
        
        if answer_text:
            answers[question_num] = answer_text
    
    return answers

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
    
    print("Parsing Excel file for questions...")
    quest_data = parse_excel_questions('quest.xlsx')
    print(f"Found {len(quest_data)} questions in quest.xlsx")
    
    print("\nParsing language files...")
    russian_data = parse_language_file('russian.txt', quest_data)
    print(f"Found {len(russian_data)} answers in russian.txt")
    
    danish_data = parse_language_file('danish.txt', quest_data)
    print(f"Found {len(danish_data)} answers in danish.txt")
    
    muira_data = parse_language_file('muira.txt', quest_data)
    print(f"Found {len(muira_data)} answers in muira.txt")
    
    nganasan_data = parse_language_file('nganasan.txt', quest_data)
    print(f"Found {len(nganasan_data)} answers in nganasan.txt")
    
    polish_data = parse_language_file('polish.txt', quest_data)
    print(f"Found {len(polish_data)} answers in polish.txt")
    
    circassian_data = parse_language_file('circassian.txt', quest_data)
    print(f"Found {len(circassian_data)} answers in circassian.txt")
    
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
            nganasan TEXT,
            polish TEXT,
            circassian TEXT
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
        polish_text = polish_data.get(question_num, '')
        circassian_text = circassian_data.get(question_num, '')
        
        try:
            cursor.execute('''
                INSERT INTO questions 
                (question_number, group_number, question_text, russian, danish, muira, nganasan, polish, circassian)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (question_num, group_num, question_text, russian_text, danish_text, muira_text, nganasan_text, polish_text, circassian_text))
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
