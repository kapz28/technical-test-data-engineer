# data_processing.py

import json
from datetime import datetime
from typing import List, Dict, Any
from kap_moovita_mix_pipeline.database.sql_commands import INSERT_SONG, INSERT_USER, INSERT_LISTENING_HISTORY, UPDATE_METADATA

def process_songs(cursor: Any, songs: Dict[str, Any]) -> None:
    """
    Process and store song data in the database.

    Args:
        cursor: Database cursor for executing SQL commands.
        songs: Dictionary containing song data and metadata.
    """
    # Insert or update song records
    cursor.executemany(INSERT_SONG, songs['items'])
    
    # Update metadata for songs
    update_metadata(cursor, 'songs', songs['total'], songs['pages'])
    
    print(f"Retrieved and stored {len(songs['items'])} songs")

def process_users(cursor: Any, users: Dict[str, Any]) -> None:
    """
    Process and store user data in the database.

    Args:
        cursor: Database cursor for executing SQL commands.
        users: Dictionary containing user data and metadata.
    """
    # Insert or update user records
    cursor.executemany(INSERT_USER, users['items'])
    
    # Update metadata for users
    update_metadata(cursor, 'users', users['total'], users['pages'])
    
    print(f"Retrieved and stored {len(users['items'])} users")

def process_listening_history(cursor: Any, listening_history: Dict[str, Any]) -> None:
    """
    Process and store listening history data in the database.

    Args:
        cursor: Database cursor for executing SQL commands.
        listening_history: Dictionary containing listening history data and metadata.
    """
    # Process listening history items
    processed_items = [
        {
            'user_id': item['user_id'],
            'items': json.dumps(item['items']),
            'created_at': item['created_at'],
            'updated_at': item['updated_at']
        }
        for item in listening_history['items']
    ]
    
    # Insert or update listening history records
    cursor.executemany(INSERT_LISTENING_HISTORY, processed_items)
    
    # Update metadata for listening history
    update_metadata(cursor, 'listening_history', listening_history['total'], listening_history['pages'])
    
    print(f"Retrieved and stored {len(listening_history['items'])} listening history records")

def update_metadata(cursor: Any, data_type: str, total_items: int, total_pages: int) -> None:
    """
    Update metadata for a specific data type in the database.

    Args:
        cursor: Database cursor for executing SQL commands.
        data_type: Type of data (e.g., 'songs', 'users', 'listening_history').
        total_items: Total number of items for this data type.
        total_pages: Total number of pages for this data type.
    """
    current_time = datetime.now().isoformat()
    cursor.execute(UPDATE_METADATA, (data_type, total_items, total_pages, current_time))

# Dictionary mapping data types to their processing functions
PROCESSORS = {
    'songs': process_songs,
    'users': process_users,
    'listening_history': process_listening_history
}

def process_data(cursor: Any, data_type: str, data: Dict[str, Any]) -> None:
    """
    Process data of a specific type using the appropriate processing function.

    Args:
        cursor: Database cursor for executing SQL commands.
        data_type: Type of data to process.
        data: Dictionary containing the data to process.
    """
    if data_type in PROCESSORS:
        PROCESSORS[data_type](cursor, data)
    else:
        print(f"No processor found for data type: {data_type}")