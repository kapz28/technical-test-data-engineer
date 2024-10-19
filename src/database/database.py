import sqlite3
import config
from .sql_commands import CREATE_TABLE_COMMANDS

def init_database():
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    
    for table_name, create_command in CREATE_TABLE_COMMANDS.items():
        cursor.execute(create_command)
        print(f"Created or verified table: {table_name}")
    
    conn.commit()
    conn.close()