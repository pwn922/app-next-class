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

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.urandom(24))
    JWT_ALGORITHMS = os.getenv('JWT_ALGORITHMS', 'RS256').split(",")
    

class ConfigGoogle:
    load_dotenv()

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    if not GOOGLE_CLIENT_ID:
        print("Error: GOOGLE_CLIENT_ID is not configured.")
        sys.exit(1)

    if not GOOGLE_CLIENT_SECRET:
        print("Error: GOOGLE_CLIENT_SECRET is not configured.")
        sys.exit(1)

    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]