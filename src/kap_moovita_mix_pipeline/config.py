# config.py

import os

# Default values for configuration
# These will be used if no environment variables are set
DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_SCHEDULED_TIME = "02:00"
DEFAULT_DATABASE_NAME = "music_data.db"

# Retrieve environment variables or use default values
# os.getenv() looks for an environment variable, and if not found, uses the provided default
BASE_URL = os.getenv('BASE_URL', DEFAULT_BASE_URL)
SCHEDULED_TIME = os.getenv('SCHEDULED_TIME', DEFAULT_SCHEDULED_TIME)
DATABASE_NAME = os.getenv('DATABASE_NAME', DEFAULT_DATABASE_NAME)

# List of variables to be exported when using 'from config import *'
# This controls what is imported when someone uses a wildcard import
__all__ = ['BASE_URL', 'SCHEDULED_TIME', 'DATABASE_NAME']

# Optional: Print configuration for debugging
# This block only runs if this script is executed directly (not imported)
if __name__ == "__main__":
    print("Current configuration:")
    print(f"BASE_URL: {BASE_URL}")
    print(f"SCHEDULED_TIME: {SCHEDULED_TIME}")
    print(f"DATABASE_NAME: {DATABASE_NAME}")