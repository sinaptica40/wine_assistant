import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')


# Database configurations
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', '')