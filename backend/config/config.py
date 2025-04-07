import os
import sys
from dotenv import load_dotenv

class ConfigFlask:
    load_dotenv()

    DB_USER = os.getenv('DB_USER', 'postgresql')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgresql')
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'flask_db')
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SWAGGER_TEMPLATE = {
        "swagger": "2.0",
        "info": {
            "title": "API - Next class",
            "description": "API to track a student's next class.",
            "version": "1.0.0"
        },
    }

