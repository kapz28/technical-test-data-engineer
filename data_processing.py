# data_processing.py

import json
from datetime import datetime
from sql_commands import INSERT_SONG, INSERT_USER, INSERT_LISTENING_HISTORY, UPDATE_METADATA

def process_songs(cursor, songs):
    cursor.executemany(INSERT_SONG, songs['items'])
    update_metadata(cursor, 'songs', songs['total'], songs['pages'])
    print(f"Retrieved and stored {len(songs['items'])} songs")

def process_users(cursor, users):
    cursor.executemany(INSERT_USER, users['items'])
    update_metadata(cursor, 'users', users['total'], users['pages'])
    print(f"Retrieved and stored {len(users['items'])} users")

def process_listening_history(cursor, listening_history):
    processed_items = [
        {
            'user_id': item['user_id'],
            'items': json.dumps(item['items']),
            'created_at': item['created_at'],
            'updated_at': item['updated_at']
        }
        for item in listening_history['items']
    ]
    cursor.executemany(INSERT_LISTENING_HISTORY, processed_items)
    update_metadata(cursor, 'listening_history', listening_history['total'], listening_history['pages'])
    print(f"Retrieved and stored {len(listening_history['items'])} listening history records")

def update_metadata(cursor, data_type, total_items, total_pages):
    cursor.execute(UPDATE_METADATA, (data_type, total_items, total_pages, datetime.now().isoformat()))