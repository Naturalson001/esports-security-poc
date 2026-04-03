import datetime
import os

LOG_FILE ="bin/logs.txt"

def log(error, source, level="ERROR"):
    try:

        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

        with open(LOG_FILE, "a") as log:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log.write(f"[{timestamp}] [{level}] [{source}] {str(error)}\n")

    except Exception as e:
        print("logging error:", e)
