# Database Update - November 21, 2025

## Changes Made

### 1. New File Structure
- All language files moved to `languages/` folder
- Files renamed with numeric prefixes (e.g., `01-russian.html`, `02-muira.html`)
- Files now in HTML format instead of plain text

### 2. Language Files
Updated from 7 to 11 languages:
1. `01-russian.html` (89 answers)
2. `02-muira.html` (87 answers)
3. `03-danish.html` (92 answers)
4. `04-nganasan.html` (88 answers)
5. `05-westcircassian.html` (86 answers)
6. `06-polish.html` (88 answers)
7. `07-bulgarian.html` (89 answers)
8. `08-nanai.html` (89 answers) **NEW**
9. `09-nor-nakhichevan.html` (85 answers) **NEW**
10. `10-udmurt.html` (87 answers) **NEW**
11. `11-Greben.html` (89 answers) **NEW**

### 3. HTML Content Preservation
- Answers in language files are now in HTML format within `<answer>` tags
- HTML formatting is preserved unchanged in the database
- Includes tags like `<i>`, `<b>`, `<br />`, `<sub>`, `<sup>`, etc.
- No conversion or processing applied to answer content

### 4. Updated Files

#### create_database.py
- Modified `parse_language_file()` to read HTML files from `languages/` folder
- Removed HTML conversion logic - content is stored as-is
- Added parsing for 4 new languages (nanai, nornakhichevan, udmurt, greben)
- Updated database schema to include 11 language columns
- Updated INSERT statements to handle all 11 languages

#### schema_postgres.sql
- Added 4 new language columns: `nanai`, `nornakhichevan`, `udmurt`, `greben`
- Reordered columns to match create_database.py

#### app.py
- Updated fallback language list to include all 11 languages
- Alphabetically sorted: bulgarian, danish, greben, muira, nanai, nganasan, nornakhichevan, polish, russian, udmurt, westcircassian

### 5. Database Statistics
- Total questions: 97
- Total groups: 12
- Total languages: 11
- All HTML formatting preserved in database

### 6. API Endpoints
All existing endpoints continue to work:
- `/api/languages` - Returns all 11 languages
- `/api/questions/<number>` - Returns question with HTML-formatted answers
- `/api/questions/group/<number>` - Returns all questions in group
- `/api/questions/random/<number>` - Returns random question(s)
- `/api/search` - Searches across all languages
- `/api/stats` - Database statistics

### 7. Verification
✓ All 11 languages parsed successfully
✓ HTML tags preserved in database (`<i>`, `<b>`, `<br />`, `<sub>`, `<sup>`)
✓ API returns HTML content unchanged
✓ Dynamic language detection works correctly
✓ Question number sorting works correctly (numerical order)

## Next Steps
1. Update deployment on Render.com
2. Commit and push changes to repository
3. Test all endpoints in production environment
