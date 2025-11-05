import re
from typing import Dict

def parse_file(filename: str, is_quest_file: bool = False) -> Dict[str, str]:
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
    in_answer_section = False
    
    lines = content.split('\n')
    
    for line in lines:
        match = re.match(r'^(\d+(?:\.\d+)*)[.\s]\s*(.*)$', line)
        
        if match:
            number_part = match.group(1)
            text_part = match.group(2).strip()
            
            if '.' not in number_part:
                if current_number:
                    questions[current_number] = ' '.join(current_text).strip()
                current_number = None
                current_text = []
                in_answer_section = False
                continue
            
            is_new_question = line.strip().startswith(number_part)
            
            if is_new_question:
                if current_number:
                    questions[current_number] = ' '.join(current_text).strip()
                
                current_number = number_part
                current_text = []
                in_answer_section = False
                
                if is_quest_file and text_part:
                    current_text = [text_part]
            elif current_number and line.strip():
                if is_quest_file:
                    current_text.append(line.strip())
                elif in_answer_section:
                    current_text.append(line.strip())
        elif current_number and line.strip():
            if line.strip().startswith('•'):
                in_answer_section = True
                answer_text = line.strip()[1:].strip()
                if answer_text:
                    current_text.append(answer_text)
            elif in_answer_section or is_quest_file:
                current_text.append(line.strip())
    
    if current_number:
        questions[current_number] = ' '.join(current_text).strip()
    
    return questions

# Test parsing
quest_data = parse_file('quest.txt', is_quest_file=True)
print(f"quest.txt: {len(quest_data)} questions")
print("\nFirst 5 from quest.txt:")
for i, (num, text) in enumerate(list(quest_data.items())[:5]):
    print(f"{num}: {text[:100]}...")

print("\n" + "="*80 + "\n")

russian_data = parse_file('russian.txt', is_quest_file=False)
print(f"russian.txt: {len(russian_data)} entries")
print("\nFirst 5 from russian.txt:")
for i, (num, text) in enumerate(list(russian_data.items())[:5]):
    print(f"{num}: {text[:100] if text else '(empty)'}...")

# Check for duplicates in quest.txt
quest_nums = list(quest_data.keys())
if len(quest_nums) != len(set(quest_nums)):
    print("\n!!! DUPLICATES IN QUEST.TXT !!!")
    from collections import Counter
    counts = Counter(quest_nums)
    for num, count in counts.items():
        if count > 1:
            print(f"  {num}: appears {count} times")
