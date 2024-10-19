# sql_commands.py

# SQL command to create the songs table
CREATE_SONGS_TABLE = '''
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    artist TEXT,
    songwriters TEXT,
    duration TEXT,
    genres TEXT,
    album TEXT,
    created_at TEXT,
    updated_at TEXT
)
'''

# SQL command to create the users table
CREATE_USERS_TABLE = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    gender TEXT,
    favorite_genres TEXT,
    created_at TEXT,
    updated_at TEXT
)
'''

# SQL command to create the listening history table
CREATE_LISTENING_HISTORY_TABLE = '''
CREATE TABLE IF NOT EXISTS listening_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    items TEXT,
    created_at TEXT,
    updated_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
'''

# SQL command to create the data metadata table
CREATE_DATA_METADATA_TABLE = '''
CREATE TABLE IF NOT EXISTS data_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_type TEXT UNIQUE,
    total_items INTEGER,  
    total_pages INTEGER,    
    last_updated TEXT       
)
'''

# SQL command to insert or update a song record
INSERT_SONG = '''
INSERT OR REPLACE INTO songs 
(id, name, artist, songwriters, duration, genres, album, created_at, updated_at)
VALUES (:id, :name, :artist, :songwriters, :duration, :genres, :album, :created_at, :updated_at)
'''

# SQL command to insert or update a user record
INSERT_USER = '''
INSERT OR REPLACE INTO users 
(id, first_name, last_name, email, gender, favorite_genres, created_at, updated_at)
VALUES (:id, :first_name, :last_name, :email, :gender, :favorite_genres, :created_at, :updated_at)
'''

# SQL command to insert or update a listening history record
INSERT_LISTENING_HISTORY = '''
INSERT OR REPLACE INTO listening_history 
(user_id, items, created_at, updated_at)
VALUES (:user_id, :items, :created_at, :updated_at)
'''

# SQL command to update metadata for a specific data type
UPDATE_METADATA = '''
INSERT OR REPLACE INTO data_metadata 
(data_type, total_items, total_pages, last_updated)
VALUES (?, ?, ?, ?)
'''

# A dictionary to easily access all table creation commands
CREATE_TABLE_COMMANDS = {
    'songs': CREATE_SONGS_TABLE,
    'users': CREATE_USERS_TABLE,
    'listening_history': CREATE_LISTENING_HISTORY_TABLE,
    'data_metadata': CREATE_DATA_METADATA_TABLE
}