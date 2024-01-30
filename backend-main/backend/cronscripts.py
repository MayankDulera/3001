import psycopg2
import schedule
import time

from sqlalchemy import create_engine

HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"
PORT = "5432"
DATABASE = "newscraper"

# Flag to indicate whether the script has completed its execution
script_completed = False

def database_connection():
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE)
    return connection

def retrieve_script_from_database():
    conn = database_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT cron FROM cronscripts ORDER BY id DESC LIMIT 1")
        script = cursor.fetchone()[0]
        return script
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def job():
    global script_completed

    # Retrieve the latest script from the database
    latest_script = retrieve_script_from_database()

    # Execute the retrieved script
    execute_script(latest_script)

    # Set the flag to indicate completion
    script_completed = True

def execute_script(script):
    try:
        # Execute the retrieved script
        print(script)
        exec(script)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Set the time at which you want the script to run (in 24-hour format)
    scheduled_time = "15:13"

    # Schedule the job to run at the specified time
    schedule.every().day.at(scheduled_time).do(job)

    while not script_completed:
        schedule.run_pending()
        time.sleep(1)

    print("Script completed. Exiting.")
