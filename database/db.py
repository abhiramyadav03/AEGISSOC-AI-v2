import sqlite3
from database.schema import DATABASE_SCHEMA

DATABASE_NAME = "database/aegis_soc.db"


# ==========================================
# Database Connection
# ==========================================

import os

def get_connection():
    db_path = os.path.abspath(DATABASE_NAME)
    print(f"Using database: {db_path}")
    return sqlite3.connect(db_path)
# ==========================================
# Create Database
# ==========================================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript(DATABASE_SCHEMA)

    conn.commit()
    conn.close()

    print("[+] Database created successfully.")


# ==========================================
# Insert Security Event
# ==========================================

def insert_event(event):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO security_events (
            event_id,
            timestamp,
            username,
            computer,
            source_ip,
            log_source,
            event_type,
            raw_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        event["event_id"],
        event["timestamp"],
        event["username"],
        event["computer"],
        event["source_ip"],
        event["log_source"],
        event["event_type"],
        event["raw_message"]
    ))

    conn.commit()
    conn.close()


# ==========================================
# Insert Alert
# ==========================================

def insert_alert(alert):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (

            event_id,
            alert_name,
            severity,
            timestamp,
            computer,
            status,

            source_ip,

            mitre_technique,
            mitre_name,
            mitre_tactic,
            risk_score,

            abuse_score,
            country,
            isp

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """,

    (

        alert["event_id"],
        alert["alert_name"],
        alert["severity"],
        alert["timestamp"],
        alert["computer"],
        alert["status"],

        alert["source_ip"],

        alert["mitre_technique"],
        alert["mitre_name"],
        alert["mitre_tactic"],
        alert["risk_score"],

        alert["abuse_score"],
        alert["country"],
        alert["isp"]

    ))

    conn.commit()
    conn.close()

# ==========================================
# Main
# ==========================================

if __name__ == "__main__":
    create_database()