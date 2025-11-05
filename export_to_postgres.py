import sqlite3

def export_to_postgres_sql(sqlite_db_path: str, output_file: str):
    """Export SQLite database to PostgreSQL-compatible SQL file."""
    
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    
    # Get all columns dynamically
    cursor.execute("PRAGMA table_info(questions)")
    columns_info = cursor.fetchall()
    all_columns = [col[1] for col in columns_info]
    
    # Separate base columns from language columns
    base_columns = ['id', 'question_number', 'group_number', 'question_text']
    language_columns = [col for col in all_columns if col not in base_columns]
    
    print(f"Found {len(language_columns)} language columns: {', '.join(language_columns)}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write PostgreSQL schema
        f.write("-- PostgreSQL schema for Grant Database\n")
        f.write("-- Compatible with render.com\n\n")
        
        # Drop table if exists
        f.write("DROP TABLE IF EXISTS questions CASCADE;\n\n")
        
        # Create table with dynamic language columns
        f.write("CREATE TABLE questions (\n")
        f.write("    id SERIAL PRIMARY KEY,\n")
        f.write("    question_number VARCHAR(20) UNIQUE NOT NULL,\n")
        f.write("    group_number VARCHAR(10) NOT NULL,\n")
        f.write("    question_text TEXT NOT NULL")
        
        for lang in language_columns:
            f.write(",\n")
            f.write(f"    {lang} TEXT")
        
        f.write("\n);\n\n")
        
        # Create index
        f.write("CREATE INDEX idx_group_number ON questions(group_number);\n\n")
        
        # Export data
        f.write("-- Insert data\n")
        
        # Build SELECT query with all columns
        select_columns = ['question_number', 'group_number', 'question_text'] + language_columns
        cursor.execute(f'SELECT {", ".join(select_columns)} FROM questions ORDER BY id')
        
        # Escape single quotes for PostgreSQL
        def escape_sql(text):
            if text is None:
                return 'NULL'
            # Replace single quotes with two single quotes
            text = text.replace("'", "''")
            return f"'{text}'"
        
        for row in cursor.fetchall():
            # Write INSERT statement
            column_names = ', '.join(select_columns)
            f.write(f"INSERT INTO questions ({column_names}) VALUES (\n")
            
            # Write values
            values = [escape_sql(val) for val in row]
            for i, val in enumerate(values):
                if i < len(values) - 1:
                    f.write(f"    {val},\n")
                else:
                    f.write(f"    {val}\n")
            f.write(");\n\n")
        
        # Add some useful views
        f.write("\n-- Useful views\n")
        f.write("""
-- View to get questions by group
CREATE OR REPLACE VIEW questions_by_group AS
SELECT group_number, COUNT(*) as question_count
FROM questions
GROUP BY group_number
ORDER BY group_number;

-- View to get all complete responses (all languages filled)
CREATE OR REPLACE VIEW complete_responses AS
SELECT * FROM questions
WHERE russian IS NOT NULL AND russian != ''
  AND danish IS NOT NULL AND danish != ''
  AND muira IS NOT NULL AND muira != ''
  AND nganasan IS NOT NULL AND nganasan != '';

""")
        
        # Add example queries as comments
        f.write("""
-- Example queries for your application:

-- Get all questions in a specific group:
-- SELECT * FROM questions WHERE group_number = '1' ORDER BY question_number;

-- Get a random question from a group:
-- SELECT * FROM questions WHERE group_number = '2' ORDER BY RANDOM() LIMIT 1;

-- Get random questions from each group (5 per group):
-- SELECT DISTINCT ON (group_number) * FROM questions ORDER BY group_number, RANDOM() LIMIT 60;

-- Search questions containing specific text:
-- SELECT * FROM questions WHERE question_text ILIKE '%контроль%';

-- Get statistics:
-- SELECT group_number, COUNT(*) FROM questions GROUP BY group_number;
""")
    
    conn.close()
    print(f"PostgreSQL SQL file created: {output_file}")
    
    # Get file size
    import os
    file_size = os.path.getsize(output_file)
    print(f"File size: {file_size / 1024:.2f} KB")

if __name__ == '__main__':
    export_to_postgres_sql('grant_database.db', 'schema_postgres.sql')
