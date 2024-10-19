import schedule
import time
from datetime import datetime
import config
import argparse
import sqlite3
from database.sql_commands import CREATE_TABLE_COMMANDS
from data_processing import process_songs, process_users, process_listening_history
from api_interact import fetch_all_data_types

def init_database():
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    for table_name, create_command in CREATE_TABLE_COMMANDS.items():
        cursor.execute(create_command)
        print(f"Created or verified table: {table_name}")
    
    conn.commit()
    conn.close()

def daily_data_retrieval():
    print(f"Running daily data retrieval at {datetime.now()}")
    
    with sqlite3.connect(config.DATABASE_NAME) as conn:
        cursor = conn.cursor()
        
        all_data = fetch_all_data_types()
        
        processors = {
            'songs': process_songs,
            'users': process_users,
            'listening_history': process_listening_history
        }
        
        for data_type, data in all_data.items():
            if data:
                processors[data_type](cursor, data)
        
        conn.commit()

def run_test_mode():
    print("Running in test mode")
    daily_data_retrieval()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data retrieval script for MoovitaMix API")
    parser.add_argument("--test", action="store_true", help="Run in test mode (execute data retrieval once)")
    parser.add_argument("--info", action="store_true", help="Display configuration information")
    parser.add_argument("--help-config", action="store_true", help="Show help about configuration options")
    args = parser.parse_args()

    if args.help_config:
        print("\nConfiguration Help:")
        print("This script uses environment variables for configuration.")
        print("You can set these in a .env file or in your system environment.")
        print("\nAvailable configuration options:")
        print(f"  BASE_URL: The base URL of the API (default: {config.BASE_URL})")
        print(f"  SCHEDULED_TIME: The daily time to run data retrieval (default: {config.SCHEDULED_TIME})")
        print("\nExample .env file content:")
        print("BASE_URL=http://api.example.com")
        print("SCHEDULED_TIME=02:00")
        exit(0)

    if args.info or args.test:
        print("\nCurrent Configuration:")
        print(f"API Base URL: {config.BASE_URL}")
        print(f"Scheduled Run Time: {config.SCHEDULED_TIME}")

    init_database()

    if args.test:
        run_test_mode()
    elif not args.info:  # Run in normal mode if not test and not just showing info
        print("\nStarting data flow in production mode.")
        print(f"Scheduled to run daily at {config.SCHEDULED_TIME}.")
        print("Press Ctrl+C to exit.")
        schedule.every().day.at(config.SCHEDULED_TIME).do(daily_data_retrieval)
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nScript terminated by user.")