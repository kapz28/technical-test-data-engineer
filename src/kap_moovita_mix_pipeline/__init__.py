# src/kap_moovita_mix_pipeline/__init__.py

from .api_interact import fetch_all_data_types
from .cli import setup_cli, display_config_help, display_current_config
from .config import BASE_URL, SCHEDULED_TIME, DATABASE_NAME
from .data_processing import process_songs, process_users, process_listening_history
from .data_retrieval import daily_data_retrieval
from .database import init_database
from .scheduler import start_scheduler

# You might want to include a version number
__version__ = "0.1.0"

# Define what should be imported when using "from kap_moovita_mix_pipeline import *"
__all__ = [
    "fetch_all_data_types",
    "setup_cli",
    "display_config_help",
    "display_current_config",
    "BASE_URL",
    "SCHEDULED_TIME",
    "DATABASE_NAME",
    "process_songs",
    "process_users",
    "process_listening_history",
    "daily_data_retrieval",
    "init_database",
    "start_scheduler",
]