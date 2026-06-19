import os
import sqlite3
import requests

def load_env(filepath=".env"):
    """
    Loads environment variables from a .env file.
    Fills os.environ if the file exists.
    """
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

def get_db_connection(db_path):
    """
    Creates and returns a connection to the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_activity_drops(conn, threshold_percentage):
    """
    Queries the database using raw SQL to find clients with a activity drop
    greater than or equal to the threshold percentage.
    
    Compares:
    - Current week: Last 7 days (days 0 to 6)
    - Previous week: The 7 days prior (days 7 to 13)
    """
    query = """
        WITH current_week AS (
            SELECT client_id, SUM(login_count) AS current_logins
            FROM usage_logs
            WHERE log_date >= date('now', '-6 days') AND log_date <= date('now')
            GROUP BY client_id
        ),
        previous_week AS (
            SELECT client_id, SUM(login_count) AS previous_logins
            FROM usage_logs
            WHERE log_date >= date('now', '-13 days') AND log_date <= date('now', '-7 days')
            GROUP BY client_id
        )
        SELECT 
            c.id AS client_id,
            c.name,
            c.am_slack_id,
            COALESCE(pw.previous_logins, 0) AS previous_logins,
            COALESCE(cw.current_logins, 0) AS current_logins,
            CASE 
                WHEN COALESCE(pw.previous_logins, 0) = 0 THEN 0.0
                ELSE ((pw.previous_logins - COALESCE(cw.current_logins, 0)) * 100.0) / pw.previous_logins
            END AS drop_percentage
        FROM clients c
        LEFT JOIN previous_week pw ON c.id = pw.client_id
        LEFT JOIN current_week cw ON c.id = cw.client_id
        WHERE CASE 
            WHEN COALESCE(pw.previous_logins, 0) = 0 THEN 0.0
            ELSE ((pw.previous_logins - COALESCE(cw.current_logins, 0)) * 100.0) / pw.previous_logins
        END >= ?;
    """
    cursor = conn.cursor()
    cursor.execute(query, (threshold_percentage,))
    return cursor.fetchall()

def send_slack_alert(webhook_url, client_name, drop_percentage, am_slack_id):
    """
    Dispatches a Slack alert payload to the specified webhook URL.
    """
    message = (
        f"🚨 Alerta de RevOps: El cliente {client_name} ha reducido su actividad "
        f"un {drop_percentage:.1f}%. {am_slack_id}, por favor revisar de inmediato."
    )
    payload = {"text": message}
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Alert sent successfully for client: {client_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send alert for client {client_name}. Error: {e}")

def main():
    load_env()
    
    webhook_url = os.getenv("WEBHOOK_URL")
    threshold = float(os.getenv("DROP_THRESHOLD", "40"))
    db_path = os.getenv("DATABASE_PATH", "db/revops.db")
    
    if not webhook_url:
        print("Error: WEBHOOK_URL is not configured in the environment or .env file.")
        return

    try:
        conn = get_db_connection(db_path)
        try:
            flagged_clients = fetch_activity_drops(conn, threshold)
            for row in flagged_clients:
                send_slack_alert(
                    webhook_url=webhook_url,
                    client_name=row["name"],
                    drop_percentage=row["drop_percentage"],
                    am_slack_id=row["am_slack_id"]
                )
        finally:
            conn.close()
    except sqlite3.Error as db_err:
        print(f"Database error occurred: {db_err}")

if __name__ == "__main__":
    main()
