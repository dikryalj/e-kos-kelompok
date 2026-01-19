"""
Script to fix existing profile image paths in database
Converts backslashes to forward slashes for URL compatibility
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def fix_profile_paths():
    with app.app_context():
        users = User.query.filter(User.profile_image.isnot(None)).all()
        
        for user in users:
            if user.profile_image and '\\' in user.profile_image:
                old_path = user.profile_image
                new_path = user.profile_image.replace('\\', '/')
                user.profile_image = new_path
                print(f"Fixed user {user.id}: {old_path} -> {new_path}")
        
        db.session.commit()
        print(f"\nFixed {len(users)} user(s) profile image paths.")

if __name__ == "__main__":
    fix_profile_paths()
