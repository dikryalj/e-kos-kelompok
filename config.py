import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-sangat-aman-sekali-12345'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ekost.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
