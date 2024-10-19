import argparse
from kap_moovita_mix_pipeline import config

def setup_cli():
    """
    Set up the command-line interface for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    # Create an ArgumentParser object with a description of the script
    parser = argparse.ArgumentParser(description="Data retrieval script for MoovitaMix API")

    # Add command-line arguments
    parser.add_argument("--test", action="store_true", help="Run in test mode (execute data retrieval once)")
    parser.add_argument("--info", action="store_true", help="Display configuration information")
    parser.add_argument("--help-config", action="store_true", help="Show help about configuration options")

    # Parse and return the command-line arguments
    return parser.parse_args()

def display_config_help():
    """
    Display help information about the configuration options.
    """
    print("\nConfiguration Help:")
    print("This script uses environment variables for configuration.")
    print("You can set these in a .env file or in your system environment.")
    
    print("\nAvailable configuration options:")
    # Display information about each configuration option
    print(f"  BASE_URL: The base URL of the API (default: {config.BASE_URL})")
    print(f"  SCHEDULED_TIME: The daily time to run data retrieval (default: {config.SCHEDULED_TIME})")
    
    print("\nExample .env file content:")
    # Provide an example of how to set configuration in a .env file
    print("BASE_URL=http://api.example.com")
    print("SCHEDULED_TIME=02:00")

def display_current_config():
    """
    Display the current configuration settings.
    """
    print("\nCurrent Configuration:")
    # Display the current values of configuration options
    print(f"API Base URL: {config.BASE_URL}")
    print(f"Scheduled Run Time: {config.SCHEDULED_TIME}")

if __name__ == "__main__":
    # This allows the script to be run directly to test CLI functionality
    args = setup_cli()
    if args.help_config:
        display_config_help()
    elif args.info:
        display_current_config()
    else:
        print("No specific action requested. Use --help for usage information.")