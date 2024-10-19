import sqlite3
from kap_moovita_mix_pipeline import config
from .sql_commands import CREATE_TABLE_COMMANDS

def init_database():
    """
    Initialize the database by creating all necessary tables.

    This function connects to the SQLite database specified in the config,
    and creates all tables defined in CREATE_TABLE_COMMANDS if they don't already exist.
    """
    # Establish a connection to the SQLite database
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    # Iterate through all table creation commands
    for table_name, create_command in CREATE_TABLE_COMMANDS.items():
        try:
            # Execute the CREATE TABLE command
            cursor.execute(create_command)
            print(f"Created or verified table: {table_name}")
        except sqlite3.Error as e:
            # Log any errors that occur during table creation
            print(f"Error creating table {table_name}: {e}")
    
    # Commit all changes to the database
    conn.commit()
    print("All tables have been created or verified.")

    # Close the database connection
    conn.close()
    print("Database initialization complete.")

if __name__ == "__main__":
    # This allows the script to be run directly for database initialization
    init_database()