"""
Script to add a new language to the database
Usage: python add_language.py <number> <language_name>
Example: python add_language.py 21 french

This script will:
1. Verify the language HTML file exists in languages/ folder
2. Recreate the entire database with all languages (including the new one)
"""

import sys
import os
import re
from create_database import create_database

def main():
    if len(sys.argv) != 3:
        print("Usage: python add_language.py <number> <language_name>")
        print("Example: python add_language.py 21 french")
        print("\nThis assumes you have already created a file like:")
        print("  languages/21-french.html")
        print("\nThe script will then recreate the database with all languages.")
        sys.exit(1)
    
    number = sys.argv[1]
    language_name = sys.argv[2].lower()
    
    # Validate number format (should be 2 digits)
    if not re.match(r'^\d{2}$', number):
        print("Error: Number must be exactly 2 digits (e.g., 01, 21)")
        sys.exit(1)
    
    # Validate language name (only letters, numbers, underscore, hyphen)
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', language_name):
        print("Error: Language name must start with a letter and contain only letters, numbers, underscores, and hyphens")
        sys.exit(1)
    
    # Expected filename
    expected_file = os.path.join('languages', f'{number}-{language_name}.html')
    
    print("=" * 70)
    print(f"ADDING LANGUAGE: {language_name.upper()}")
    print("=" * 70)
    
    # Check if file exists
    print(f"\n[1/2] Checking for language file...")
    if not os.path.exists(expected_file):
        print(f"✗ ERROR: File not found: {expected_file}")
        print("\nPlease create the language HTML file first with the following format:")
        print(f"  File: {expected_file}")
        print("  Format:")
        print("    1.1. <answer>")
        print("    Your answer text here (can include HTML tags)")
        print("    </answer>")
        print("")
        print("    2.1. <answer>")
        print("    Another answer")
        print("    </answer>")
        print("\nYou can use languages/!EMPTY.html as a template.")
        sys.exit(1)
    
    print(f"✓ Found: {expected_file}")
    
    # Count answers in the file
    with open(expected_file, 'r', encoding='utf-8') as f:
        content = f.read()
        answer_count = len(re.findall(r'<answer>', content, re.IGNORECASE))
    
    print(f"  File contains ~{answer_count} answer blocks")
    
    # Recreate the database
    print(f"\n[2/2] Recreating database with all languages...")
    print("  (This will include your new language)")
    print()
    
    # Delete old database
    db_path = 'grant_database.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"  ✓ Removed old database")
    
    # Create new database (this will discover all languages including the new one)
    create_database(db_path)
    
    print("\n" + "=" * 70)
    print(f"✓ Successfully added {language_name} to the database!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Verify the database: python test_database.py")
    print("2. Update PostgreSQL schema if needed: python export_to_postgres.py")
    print("3. Update the fallback language list in app.py")
    print(f"   Add '{language_name}' to the list in get_language_columns()")

if __name__ == '__main__':
    main()
