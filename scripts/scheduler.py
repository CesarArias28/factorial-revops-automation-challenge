import time
import logging
import schedule
from health_monitor import run_monitor

# Configure logging
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    print("Initializing RevOps Health Alert Scheduler...")
    print("Scheduled to run every Monday at 08:00.")
    
    # Configure the cron schedule simulator
    schedule.every().monday.at("08:00").do(run_monitor)
    
    # Daemon loop running pending tasks every 60 seconds
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
    except Exception as e:
        logging.error(f"Scheduler daemon crashed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
