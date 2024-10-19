import argparse
import config

def setup_cli():
    parser = argparse.ArgumentParser(description="Data retrieval script for MoovitaMix API")
    parser.add_argument("--test", action="store_true", help="Run in test mode (execute data retrieval once)")
    parser.add_argument("--info", action="store_true", help="Display configuration information")
    parser.add_argument("--help-config", action="store_true", help="Show help about configuration options")
    return parser.parse_args()

def display_config_help():
    print("\nConfiguration Help:")
    print("This script uses environment variables for configuration.")
    print("You can set these in a .env file or in your system environment.")
    print("\nAvailable configuration options:")
    print(f"  BASE_URL: The base URL of the API (default: {config.BASE_URL})")
    print(f"  SCHEDULED_TIME: The daily time to run data retrieval (default: {config.SCHEDULED_TIME})")
    print("\nExample .env file content:")
    print("BASE_URL=http://api.example.com")
    print("SCHEDULED_TIME=02:00")

def display_current_config():
    print("\nCurrent Configuration:")
    print(f"API Base URL: {config.BASE_URL}")
    print(f"Scheduled Run Time: {config.SCHEDULED_TIME}")