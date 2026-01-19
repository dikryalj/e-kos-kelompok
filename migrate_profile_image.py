"""
Script to add profile_image column to User table
Run this script once to migrate the database
"""
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

def migrate_database():
    with app.app_context():
        try:
            # Check if column exists
            result = db.session.execute(text("PRAGMA table_info(user)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'profile_image' not in columns:
                # Add the column
                db.session.execute(text("ALTER TABLE user ADD COLUMN profile_image VARCHAR(255)"))
                db.session.commit()
                print("Successfully added 'profile_image' column to User table.")
            else:
                print("Column 'profile_image' already exists in User table.")
                
        except Exception as e:
            print(f"Error during migration: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_database()
