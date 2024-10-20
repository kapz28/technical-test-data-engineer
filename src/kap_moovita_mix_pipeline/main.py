import argparse
from .database import init_database
from .scheduler import start_scheduler
from .data_retrieval import daily_data_retrieval
from .cli import setup_cli, display_config_help, display_current_config

def main():
    """
    Main function to orchestrate the data retrieval process.
    Handles command-line arguments and executes appropriate actions.
    """
    # Parse command-line arguments
    args = setup_cli()

    # If --help-config flag is used, display configuration help and exit
    if args.help_config:
        display_config_help()
        return

    # If --info or --test flags are used, display current configuration
    if args.info or args.test:
        display_current_config()

    # Initialize the database (create tables if they don't exist)
    init_database()

    # Execute actions based on command-line arguments
    if args.test:
        # If in test mode, run data retrieval once
        daily_data_retrieval()
    elif not args.info:
        # If not in info mode and not in test mode, start the scheduler
        start_scheduler()

if __name__ == "__main__":
    # Execute the main function when the script is run
    main()