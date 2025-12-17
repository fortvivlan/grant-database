# Database System Update Summary

## Changes Made

### 1. Dynamic Language Discovery
The database system now automatically discovers and processes all language HTML files in the `languages/` folder. No more hardcoding!

### 2. Updated Scripts

#### create_database.py
- **New function:** `discover_language_files()` - Scans the `languages/` folder for all `XX-languagename.html` files
- **Dynamic table creation:** Creates database columns based on discovered languages
- **Automatic name sanitization:** Converts hyphens to underscores for SQL compatibility (e.g., `nor-nakhichevan` → `nor_nakhichevan`)
- **Better output:** Shows progress with numbered steps and detailed coverage statistics
- **Clean slate:** Automatically drops and recreates tables for a fresh database

#### add_language.py
- **Complete rewrite:** Now expects `<number> <language_name>` instead of text files
- **Simplified workflow:** Just checks if the HTML file exists and recreates the database
- **Better validation:** Checks number format (must be 2 digits) and language name format
- **Clear instructions:** Provides helpful error messages if file is missing

### 3. New Utility Scripts

#### list_languages.py
Shows all languages currently in the database with:
- Coverage statistics for each language
- Comparison between database columns and HTML files
- Easy-to-read table format

#### ADDING_LANGUAGES.md
Complete guide for adding new languages with:
- Step-by-step instructions
- File format examples
- Important notes about naming conventions
- Testing recommendations

### 4. Files Modified

1. **create_database.py** - Fully dynamic language handling
2. **add_language.py** - Simplified workflow
3. **schema_postgres.sql** - Added note about dynamic updates
4. **app.py** - Updated fallback list (already had dynamic detection)

### 5. Files Created

1. **list_languages.py** - Language listing utility
2. **ADDING_LANGUAGES.md** - User guide for adding languages

## How It Works Now

### Adding a New Language

1. Create `languages/21-french.html` with your answers
2. Run: `python add_language.py 21 french`
3. Done! Database is recreated with all 21 languages

### What Happens Behind the Scenes

1. Script scans `languages/` folder
2. Finds all files matching `[0-9][0-9]-*.html` (ignoring `!EMPTY.html`)
3. Extracts language names and sanitizes them for SQL
4. Creates a database table with dynamic columns for each language
5. Parses each HTML file and populates the database
6. Shows coverage statistics

## Benefits

✅ **No more hardcoding** - Add languages by just creating HTML files
✅ **Automatic discovery** - System finds and processes all languages
✅ **Error prevention** - SQL-safe column names automatically generated
✅ **Better visibility** - Clear progress output and coverage stats
✅ **Simpler workflow** - Just two arguments to add a language
✅ **Maintainable** - Future languages require zero code changes

## Usage Examples

```bash
# Recreate database from all HTML files
python create_database.py

# Add a new language (after creating the HTML file)
python add_language.py 21 french

# See what languages are in the database
python list_languages.py

# Verify the database
python verify_new_languages.py
```

## Current Database

- **Total Questions:** 97
- **Total Groups:** 12
- **Total Languages:** 20

All languages have 85-92 answers (87.6% - 94.8% coverage)

## Technical Details

### SQL Column Naming
- Hyphens in filenames → underscores in database
- Example: `09-nor-nakhichevan.html` → `nor_nakhichevan` column

### File Pattern Matching
- Pattern: `[0-9][0-9]-*.html`
- Excludes: Files starting with `!`
- Case: Preserves filename case but converts to lowercase for database

### Database Recreation
- Drops existing `questions` and `groups` tables
- Creates fresh tables with discovered languages
- Maintains referential integrity with foreign keys
- Creates indexes for performance
