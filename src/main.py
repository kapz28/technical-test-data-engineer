import argparse
from database import init_database
from scheduler import start_scheduler
from data_retrieval import daily_data_retrieval
from cli import setup_cli, display_config_help, display_current_config

def main():
    args = setup_cli()

    if args.help_config:
        display_config_help()
        return

    if args.info or args.test:
        display_current_config()

    init_database()

    if args.test:
        daily_data_retrieval()
    elif not args.info:
        start_scheduler()

if __name__ == "__main__":
    main()