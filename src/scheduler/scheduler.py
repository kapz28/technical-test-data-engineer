import schedule
import time
import config
from data_retrieval import daily_data_retrieval

def start_scheduler():
    print("\nStarting data flow in production mode.")
    print(f"Scheduled to run daily at {config.SCHEDULED_TIME}.")
    print("Press Ctrl+C to exit.")
    schedule.every().day.at(config.SCHEDULED_TIME).do(daily_data_retrieval)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScript terminated by user.")