# Grant Database - Linguistic Questionnaire Database

This database contains linguistic questionnaire data with questions in multiple languages (Russian, Danish, Muira, Nganasan).

## Database Structure

The database consists of a single table `questions` with the following schema:

```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_number VARCHAR(20) UNIQUE NOT NULL,  -- e.g., "1.1", "2.4.1"
    group_number VARCHAR(10) NOT NULL,            -- Top-level group: "1", "2", etc.
    question_text TEXT NOT NULL,                  -- The question from quest.txt
    russian TEXT,                                 -- Answer in Russian
    danish TEXT,                                  -- Answer in Danish
    muira TEXT,                                   -- Answer in Muira
    nganasan TEXT                                 -- Answer in Nganasan
);
```

## Files in This Repository

### Data Files
- **quest.txt** - Source questions (103 questions across 12 groups)
- **russian.txt, danish.txt, muira.txt, nganasan.txt** - Language-specific answers

### Scripts
- **create_database.py** - Parse text files and create SQLite database
- **add_language.py** - Add new language columns to the database dynamically
- **export_to_postgres.py** - Export SQLite to PostgreSQL-compatible SQL
- **test_database.py** - Comprehensive test suite for database validation
- **app.py** - Flask REST API with 8 endpoints

### Database Files
- **grant_database.db** - SQLite database (for local testing)
- **schema_postgres.sql** - PostgreSQL schema and data (for deployment)

### Web Interface
- **viewer.html** - Interactive web viewer with filtering, random sampling, and CSV export
- **example.html** - Simple API usage example

## Statistics

- **Total Questions:** 103
- **Total Groups:** 12
- **Languages:** 4+ (Russian, Danish, Muira, Nganasan - dynamically extensible)

## Local Setup

### Prerequisites
- Python 3.7+
- SQLite3
- Required packages: `pip install flask flask-cors psycopg2-binary gunicorn`

### Create the Database Locally

```bash
# Create SQLite database from text files
python create_database.py

# Run tests to verify database
python test_database.py

# Export to PostgreSQL format
python export_to_postgres.py
```

### Adding New Languages

You can dynamically add new language columns to the database:

```bash
# Add a new language
python add_language.py <language_name> <txt_file_path>

# Example:
python add_language.py german german.txt

# The script will:
# 1. Parse the language file
# 2. Add a new column to the database
# 3. Update all matching questions
# 4. Show coverage statistics
```

**Language file format:** Same as existing files (quest.txt format):
```
1.1. Answer for question 1.1
1.2. Answer for question 1.2
2.1. Answer for question 2.1
...
```

After adding a language:
1. Run `python test_database.py` to verify
2. Run `python export_to_postgres.py` to update PostgreSQL schema
3. The API and viewer will automatically detect the new language

### Using the Interactive Viewer

Open `viewer.html` in your browser (requires API running):

```bash
# Start the API locally
python app.py

# Then open viewer.html in your browser
# Features:
# - View full database as a table
# - Filter by groups (checkboxes for all 12 groups)
# - Filter by languages (dynamically shows all available languages)
# - Random sampling (choose number of rows per group)
# - Export to CSV
```

### Query Examples (SQLite)

```bash
# Open the database
sqlite3 grant_database.db

# Get all questions in group 1
SELECT * FROM questions WHERE group_number = '1';

# Get a random question from group 2
SELECT * FROM questions WHERE group_number = '2' ORDER BY RANDOM() LIMIT 1;

# Search for specific text
SELECT question_number, question_text FROM questions 
WHERE question_text LIKE '%контроль%';

# Get statistics by group
SELECT group_number, COUNT(*) as count FROM questions 
GROUP BY group_number ORDER BY group_number;
```

## Deployment to Render.com

### Step 1: Create PostgreSQL Database on Render

1. Log in to [render.com](https://render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure your database:
   - **Name:** grant-database (or your choice)
   - **Database:** grant_db
   - **User:** (will be auto-generated)
   - **Region:** Choose closest to your users
   - **PostgreSQL Version:** 15 or later
   - **Plan:** Free (or choose based on needs)
4. Click **"Create Database"**

### Step 2: Get Connection Details

After creation, Render will provide:
- **Internal Database URL** (for apps on Render)
- **External Database URL** (for external connections)
- **PSQL Command** (for command-line access)

### Step 3: Import Data

#### Option A: Using Render Dashboard

1. Go to your database dashboard on Render
2. Click on **"Connect"** → **"External Connection"**
3. Use the provided connection string with `psql` or any PostgreSQL client
4. Run the SQL file:
   ```bash
   psql <connection-string> < schema_postgres.sql
   ```

#### Option B: Using psql Command Line

```bash
# Copy the PSQL command from Render dashboard (looks like this):
# PGPASSWORD=xxxx psql -h xxxx.oregon-postgres.render.com -U grant_db_user grant_db

# Then import the schema:
PGPASSWORD=your_password psql -h your-host.render.com -U your_user your_db < schema_postgres.sql
```

#### Option C: Using a PostgreSQL GUI Client

1. Use tools like **pgAdmin**, **DBeaver**, or **TablePlus**
2. Connect using the External Database URL from Render
3. Open and execute `schema_postgres.sql`

### Step 4: Verify Database

```sql
-- Check if data was imported
SELECT COUNT(*) FROM questions;

-- Should return: 103

-- Check groups
SELECT group_number, COUNT(*) FROM questions 
GROUP BY group_number 
ORDER BY group_number;
```

## Using the Database in Your Application

### Connection String Format

```
postgresql://user:password@host:port/database
```

Example with Python (using psycopg2):

```python
import psycopg2
import os

# Use environment variable for security
DATABASE_URL = os.environ.get('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Get all questions in group 1
cursor.execute("SELECT * FROM questions WHERE group_number = %s", ('1',))
questions = cursor.fetchall()

# Get random question from group 2
cursor.execute("""
    SELECT * FROM questions 
    WHERE group_number = %s 
    ORDER BY RANDOM() 
    LIMIT 1
""", ('2',))
random_question = cursor.fetchone()

conn.close()
```

### Common Query Patterns

#### Get All Questions in a Group
```sql
SELECT * FROM questions 
WHERE group_number = '1' 
ORDER BY question_number;
```

#### Get Random Questions from a Group
```sql
SELECT * FROM questions 
WHERE group_number = '2' 
ORDER BY RANDOM() 
LIMIT 5;
```

#### Get Random Questions from Each Group
```sql
SELECT DISTINCT ON (group_number) 
    question_number, group_number, question_text, russian, danish, muira, nganasan
FROM questions 
ORDER BY group_number, RANDOM();
```

#### Search Across All Fields
```sql
SELECT * FROM questions 
WHERE question_text ILIKE '%control%' 
   OR russian ILIKE '%контроль%'
   OR danish ILIKE '%kontrol%';
```

#### Get Statistics
```sql
-- Questions per group
SELECT group_number, COUNT(*) as question_count
FROM questions
GROUP BY group_number
ORDER BY group_number;

-- Questions with all languages filled
SELECT COUNT(*) FROM questions
WHERE russian != '' AND danish != '' 
  AND muira != '' AND nganasan != '';
```

## Flask REST API

The included `app.py` provides a complete REST API with 8 endpoints:

### Available Endpoints

1. **GET /** - API documentation and endpoint list
2. **GET /api/languages** - Get list of available languages
3. **GET /api/groups** - Get all groups with question counts
4. **GET /api/questions/group/<group_number>** - Get all questions in a group
5. **GET /api/questions/random/<group_number>?count=N** - Get random questions from a group
6. **GET /api/questions/<question_number>** - Get specific question by number
7. **GET /api/search?q=<query>&lang=<language>** - Search questions and answers
8. **GET /api/stats** - Get database statistics

### Running the API Locally

```bash
# Set DATABASE_URL environment variable (for PostgreSQL)
export DATABASE_URL="postgresql://user:password@localhost:5432/grant_db"

# Or use SQLite for local testing (modify app.py to use sqlite3 instead of psycopg2)

# Start the server
python app.py

# API will be available at http://localhost:5000
```

### API Examples

```bash
# Get all languages
curl http://localhost:5000/api/languages

# Get all groups
curl http://localhost:5000/api/groups

# Get all questions in group 1
curl http://localhost:5000/api/questions/group/1

# Get 5 random questions from group 2
curl http://localhost:5000/api/questions/random/2?count=5

# Get specific question
curl http://localhost:5000/api/questions/1.1

# Search for text
curl "http://localhost:5000/api/search?q=контроль&lang=russian"

# Get statistics
curl http://localhost:5000/api/stats
```

## Environment Variables

For security, always use environment variables for database credentials:

```bash
# .env file (don't commit this!)
DATABASE_URL=postgresql://user:password@host:port/database
```

## Security Best Practices

1. **Never commit database credentials** to version control
2. Use **environment variables** for sensitive data
3. **Whitelist IP addresses** if possible (Render allows this)
4. Use **SSL connections** (Render enforces this by default)
5. Create **read-only users** for public-facing applications
6. Implement **rate limiting** on your API

## Backup

Render automatically backs up your database. To manually backup:

```bash
# Using pg_dump
pg_dump <connection-string> > backup.sql

# Restore from backup
psql <connection-string> < backup.sql
```

## Troubleshooting

### Connection Issues
- Verify the connection string is correct
- Check if your IP is whitelisted (if required)
- Ensure SSL mode is enabled

### Data Import Issues
- Check for special characters in the SQL file
- Verify PostgreSQL version compatibility
- Look at Render logs for specific errors

### Performance Issues
- Add indexes on frequently queried columns
- Use connection pooling (e.g., pgBouncer)
- Consider upgrading your Render plan

## License

[Add your license here]

## Contact

[Add your contact information]
