import schedule
import time
import config
from data_retrieval import daily_data_retrieval

def start_scheduler():
    """
    Start the scheduler for daily data retrieval.

    This function sets up a daily schedule for data retrieval and
    runs continuously until interrupted by the user.
    """
    # Print information about the scheduler starting
    print("\nStarting data flow in production mode.")
    print(f"Scheduled to run daily at {config.SCHEDULED_TIME}.")
    print("Press Ctrl+C to exit.")

    # Schedule the daily_data_retrieval function to run at the specified time
    schedule.every().day.at(config.SCHEDULED_TIME).do(daily_data_retrieval)

    try:
        # Keep the script running indefinitely
        while True:
            # Check if there are any scheduled tasks to run
            schedule.run_pending()
            # Sleep for 1 second to prevent excessive CPU usage
            time.sleep(1)
    except KeyboardInterrupt:
        # Handle the case when the user interrupts the script (Ctrl+C)
        print("\nScript terminated by user.")
    finally:
        # Perform any necessary cleanup here
        print("Shutting down scheduler...")

if __name__ == "__main__":
    # This allows the script to be run directly to start the scheduler
    start_scheduler()