from datetime import datetime
import sqlite3
from kap_moovita_mix_pipeline import config
from kap_moovita_mix_pipeline.api_interact import fetch_all_data_types
from kap_moovita_mix_pipeline.data_processing import process_songs, process_users, process_listening_history

def daily_data_retrieval():
    """
    Perform the daily data retrieval and processing routine.
    
    This function fetches data from all API endpoints, processes it,
    and stores it in the database.
    """
    # Log the start time of the data retrieval process
    print(f"Running daily data retrieval at {datetime.now()}")
    
    # Connect to the SQLite database
    with sqlite3.connect(config.DATABASE_NAME) as conn:
        cursor = conn.cursor()
        
        # Fetch data from all API endpoints
        all_data = fetch_all_data_types()
        
        # Define a mapping of data types to their respective processing functions
        processors = {
            'songs': process_songs,
            'users': process_users,
            'listening_history': process_listening_history
        }
        
        # Process each type of data
        for data_type, data in all_data.items():
            if data:
                # Call the appropriate processing function for each data type
                print(f"Processing {data_type} data...")
                processors[data_type](cursor, data)
            else:
                print(f"No data received for {data_type}")
        
        # Commit all changes to the database
        conn.commit()
        print("All data processed and saved to the database.")

    print("Daily data retrieval completed.")