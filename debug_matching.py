import openpyxl
import re

# Get a question from Excel
wb = openpyxl.load_workbook('quest.xlsx')
ws = wb.active

# Get question 1.1 from Excel
excel_question = ws.cell(1, 2).value
print("Question from Excel:")
print(f"'{excel_question}'")
print(f"\nLength: {len(excel_question)}")

# Now check what's in russian.txt
with open('russian.txt', 'r', encoding='utf-8') as f:
    russian_content = f.read()

# Find the question in russian.txt
lines = russian_content.split('\n')
for i, line in enumerate(lines[:10]):
    if '1.1' in line:
        print(f"\n\nLine {i} in russian.txt with '1.1':")
        print(f"'{line}'")
        print(f"\nLength: {len(line)}")

# Try to find with regex
match = re.search(r'1\.1[.\s\t]+', russian_content)
if match:
    print(f"\n\nFound '1.1' at position {match.start()}")
    print(f"Context (200 chars): {russian_content[match.start():match.start()+200]}")

wb.close()
