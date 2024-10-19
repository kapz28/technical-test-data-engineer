# config.py
import os

# Default values
DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_SCHEDULED_TIME = "02:00"
DEFAULT_DATABASE_NAME = "music_data.db"

# Retrieve environment variables or use default values
BASE_URL = os.getenv('BASE_URL', DEFAULT_BASE_URL)
SCHEDULED_TIME = os.getenv('SCHEDULED_TIME', DEFAULT_SCHEDULED_TIME)
DATABASE_NAME = os.getenv('DATABASE_NAME', DEFAULT_DATABASE_NAME)

# List of variables to be exported when using 'from config import *'
__all__ = ['BASE_URL', 'SCHEDULED_TIME', 'DATABASE_NAME']

# Optional: Print configuration for debugging
if __name__ == "__main__":
    print("Current configuration:")
    print(f"BASE_URL: {BASE_URL}")
    print(f"SCHEDULED_TIME: {SCHEDULED_TIME}")
    print(f"DATABASE_NAME: {DATABASE_NAME}")