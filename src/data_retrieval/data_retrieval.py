from datetime import datetime
import sqlite3
import config
from api_interact import fetch_all_data_types
from data_processing import process_songs, process_users, process_listening_history

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