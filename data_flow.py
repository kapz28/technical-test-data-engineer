import requests
import schedule
import time
from datetime import datetime
import config
import os
import argparse
import json
import sqlite3

# Get BASE_URL and SCHEDULED_TIME from environment variables, with default values
BASE_URL = os.getenv('BASE_URL', "http://127.0.0.1:8000")
SCHEDULED_TIME = os.getenv('SCHEDULED_TIME', "14:00")

def init_database():
    conn = sqlite3.connect('music_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS songs
                      (id INTEGER PRIMARY KEY,
                       name TEXT,
                       artist TEXT,
                       songwriters TEXT,
                       duration TEXT,
                       genres TEXT,
                       album TEXT,
                       created_at TEXT,
                       updated_at TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY,
                       first_name TEXT,
                       last_name TEXT,
                       email TEXT,
                       gender TEXT,
                       favorite_genres TEXT,
                       created_at TEXT,
                       updated_at TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS listening_history
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       items TEXT,
                       created_at TEXT,
                       updated_at TEXT,
                       FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS data_metadata
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       data_type TEXT UNIQUE,
                       total_items INTEGER,
                       total_pages INTEGER,
                       last_updated TEXT)''')
    
    conn.commit()
    conn.close()

def fetch_data(endpoint):
    response = requests.get(f"{BASE_URL}{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {endpoint}: {response.status_code}")
        return None

def fetch_all_data(endpoint):
    all_data = {'items': [], 'total': 0, 'pages': 0}
    page = 1
    while True:
        data = fetch_data(f"{endpoint}?page={page}")
        if not data or 'items' not in data or not data['items']:
            break
        all_data['items'].extend(data['items'])
        all_data['total'] = data['total']
        all_data['pages'] = data['pages']
        if page >= data['pages']:
            break
        page += 1
    return all_data

def update_metadata(cursor, data_type, total_items, total_pages):
    cursor.execute('''INSERT OR REPLACE INTO data_metadata 
                      (data_type, total_items, total_pages, last_updated)
                      VALUES (?, ?, ?, ?)''', 
                   (data_type, total_items, total_pages, datetime.now().isoformat()))

def daily_data_retrieval():
    print(f"Running daily data retrieval at {datetime.now()}")
    
    conn = sqlite3.connect('music_data.db')
    cursor = conn.cursor()
    
    # Fetch and store songs
    songs = fetch_all_data("/tracks")
    if songs:
        cursor.executemany('''INSERT OR REPLACE INTO songs 
                              (id, name, artist, songwriters, duration, genres, album, created_at, updated_at)
                              VALUES (:id, :name, :artist, :songwriters, :duration, :genres, :album, :created_at, :updated_at)''', 
                              songs['items'])
        update_metadata(cursor, 'songs', songs['total'], songs['pages'])
        print(f"Retrieved and stored {len(songs['items'])} songs")
    
    # Fetch and store users
    users = fetch_all_data("/users")
    if users:
        cursor.executemany('''INSERT OR REPLACE INTO users 
                              (id, first_name, last_name, email, gender, favorite_genres, created_at, updated_at)
                              VALUES (:id, :first_name, :last_name, :email, :gender, :favorite_genres, :created_at, :updated_at)''', 
                              users['items'])
        update_metadata(cursor, 'users', users['total'], users['pages'])
        print(f"Retrieved and stored {len(users['items'])} users")
    
    # Fetch and store listening history
    listening_history = fetch_all_data("/listen_history")
    if listening_history:
        cursor.executemany('''INSERT OR REPLACE INTO listening_history 
                              (user_id, items, created_at, updated_at)
                              VALUES (:user_id, :items, :created_at, :updated_at)''', 
                              [{'user_id': item['user_id'], 
                                'items': json.dumps(item['items']), 
                                'created_at': item['created_at'], 
                                'updated_at': item['updated_at']} 
                               for item in listening_history['items']])
        update_metadata(cursor, 'listening_history', listening_history['total'], listening_history['pages'])
        print(f"Retrieved and stored {len(listening_history['items'])} listening history records")
    
    conn.commit()
    conn.close()

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
        print(f"  BASE_URL: The base URL of the API (default: {BASE_URL})")
        print(f"  SCHEDULED_TIME: The daily time to run data retrieval (default: {SCHEDULED_TIME})")
        print("\nExample .env file content:")
        print("BASE_URL=http://api.example.com")
        print("SCHEDULED_TIME=02:00")
        exit(0)

    if args.info or args.test:
        print("\nCurrent Configuration:")
        print(f"API Base URL: {BASE_URL}")
        print(f"Scheduled Run Time: {SCHEDULED_TIME}")

    init_database()

    if args.test:
        run_test_mode()
    elif not args.info:  # Run in normal mode if not test and not just showing info
        print("\nStarting data flow in production mode.")
        print(f"Scheduled to run daily at {SCHEDULED_TIME}.")
        print("Press Ctrl+C to exit.")
        schedule.every().day.at(SCHEDULED_TIME).do(daily_data_retrieval)
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nScript terminated by user.")