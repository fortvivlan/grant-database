# Grant Database - Quick Start Guide

## Adding a New Language

The database now dynamically discovers all languages from the `languages/` folder. To add a new language:

### Step 1: Create the Language HTML File

Create a new HTML file in the `languages/` folder following this naming pattern:
```
languages/XX-languagename.html
```

Where:
- `XX` is a 2-digit number (e.g., 21, 22, 23)
- `languagename` is the name of your language (lowercase, no spaces)

Example: `languages/21-french.html`

### Step 2: Format Your HTML File

Use the following format for your answers:

```html
1.1. <answer>
Your answer text here (can include HTML tags like <b>, <i>, <br />, etc.)
</answer>

1.2. <answer>
Another answer
</answer>

2.1. <answer>
More answers...
</answer>
```

**Tip:** You can use `languages/!EMPTY.html` as a template - it has all question numbers ready for you to fill in.

### Step 3: Add the Language to the Database

Run the add_language script:

```bash
python add_language.py <number> <language_name>
```

Example:
```bash
python add_language.py 21 french
```

This will:
1. Verify that `languages/21-french.html` exists
2. Recreate the entire database with all languages (including the new one)
3. Show you coverage statistics

### Step 4: Update the Fallback List (Optional)

Edit `app.py` and add your language to the fallback list in the `get_language_columns()` function:

```python
return ['abaza', 'bulgarian', 'danish', 'french', 'greben', ...]
```

**Note:** This is only needed as a fallback. The app normally reads languages dynamically from the database.

## Recreating the Database

To recreate the entire database from scratch (useful if you've made changes to multiple language files):

```bash
python create_database.py
```

This will:
- Automatically discover all `XX-languagename.html` files in the `languages/` folder
- Parse all of them
- Create a new database with all languages
- Show coverage statistics for each language

The script ignores files starting with `!` (like `!EMPTY.html`).

## Important Notes

### File Naming Rules
- Language files must follow the pattern: `XX-languagename.html`
- XX must be exactly 2 digits (01, 02, ..., 21, 22, etc.)
- Language name should be lowercase
- Hyphens in filenames are converted to underscores in the database (e.g., `09-nor-nakhichevan.html` becomes column `nor_nakhichevan`)

### What Gets Ignored
- Files starting with `!` (like `!EMPTY.html`)
- Files not matching the `XX-languagename.html` pattern

## Testing Your Changes

After adding or modifying languages:

```bash
# Test the database
python test_database.py

# Verify specific languages
python verify_new_languages.py

# Show language counts
python show_language_counts.py
```

## Exporting to PostgreSQL

After recreating the database, update your PostgreSQL schema:

```bash
python export_to_postgres.py
```

This will generate an updated schema with all current languages.
