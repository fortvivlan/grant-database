import re
from collections import Counter

files = ['quest.txt', 'russian.txt', 'danish.txt', 'muira.txt', 'nganasan.txt']

for filename in files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        
        matches = re.findall(r'^(\d+(?:\.\d+)*)[.\s]\s*', data, re.MULTILINE)
        counter = Counter(matches)
        duplicates = [(k, v) for k, v in counter.items() if v > 1]
        
        print(f"\n{filename}:")
        print(f"  Total entries: {len(matches)}")
        print(f"  Unique entries: {len(counter)}")
        
        if duplicates:
            print(f"  DUPLICATES FOUND:")
            for num, count in duplicates:
                print(f"    {num}: appears {count} times")
        else:
            print(f"  No duplicates")
            
        # Check for entries not in quest.txt
        if filename != 'quest.txt':
            with open('quest.txt', 'r', encoding='utf-8') as f:
                quest_data = f.read()
            quest_matches = set(re.findall(r'^(\d+(?:\.\d+)*)[.\s]\s*', quest_data, re.MULTILINE))
            file_matches = set(matches)
            
            extra = file_matches - quest_matches
            missing = quest_matches - file_matches
            
            if extra:
                print(f"  EXTRA (not in quest.txt): {sorted(extra)}")
            if missing:
                print(f"  MISSING (in quest.txt but not here): {sorted(missing)}")
                
    except Exception as e:
        print(f"\n{filename}: Error - {e}")
