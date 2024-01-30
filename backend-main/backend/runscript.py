import psycopg2
from sqlalchemy import create_engine

HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"
PORT = "5432"
DATABASE = "newscraper"

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

def execute_script(script):
    try:
        # Execute the retrieved script
        print(script)
        exec(script)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Retrieve the latest script from the database
    latest_script = retrieve_script_from_database()

    # Execute the retrieved script
    execute_script(latest_script)
