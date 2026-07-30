import sqlite3
import time

from detectors.mitre import MITRE_MAPPING
from detectors.risk_score import calculate_risk
from detectors.ip_enrichment import check_ip
from detectors.correlation import correlate_failed_login
from detectors.response import RESPONSE_ACTIONS
from database.db import insert_alert

DATABASE = "database/aegis_soc.db"

last_id = 0

print("=" * 60)
print("AEGIS SOC Detection Engine Started")
print("=" * 60)

while True:

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            event_id,
            timestamp,
            computer,
            source_ip
        FROM security_events
        WHERE id > ?
        ORDER BY id
    """, (last_id,))

    rows = cursor.fetchall()

    for row in rows:

        db_id = row[0]
        event_id = row[1]
        timestamp = row[2]
        computer = row[3]
        source_ip = row[4]

        severity = "INFO"
        alert = None

        # =====================================
        # Detection Rules
        # =====================================

        if event_id == 4625:

            severity = "MEDIUM"
            alert = "Failed Login"

            if correlate_failed_login(source_ip, timestamp):

                severity = "CRITICAL"
                alert = "Brute Force Attack"

        elif event_id == 4672:

            severity = "HIGH"
            alert = "Admin Privilege Assigned"

        elif event_id == 4720:

            severity = "CRITICAL"
            alert = "New User Created"

        if not alert:
            last_id = db_id
            continue
                # =====================================
        # MITRE ATT&CK Mapping
        # =====================================

        mitre = MITRE_MAPPING.get(
            event_id,
            {
                "technique": "Unknown",
                "name": "Unknown",
                "tactic": "Unknown"
            }
        )

        # =====================================
        # Risk Score
        # =====================================

        risk = calculate_risk(severity)

        # =====================================
        # IOC Enrichment
        # =====================================

        if not source_ip or source_ip == "Unknown":
            ioc = {
                "abuse_score": 0,
                "country": "Unknown",
                "isp": "Unknown"
            }
        else:
            ioc = check_ip(source_ip)

        # =====================================
        # Create Alert Object
        # =====================================

        alert_data = {

            "event_id": event_id,
            "alert_name": alert,
            "severity": severity,
            "timestamp": timestamp,
            "computer": computer,
            "status": "Open",

            "source_ip": source_ip,

            "mitre_technique": mitre["technique"],
            "mitre_name": mitre["name"],
            "mitre_tactic": mitre["tactic"],

            "risk_score": risk,

            "abuse_score": ioc["abuse_score"],
            "country": ioc["country"],
            "isp": ioc["isp"]

        }

        # =====================================
        # Save Alert
        # =====================================

        insert_alert(alert_data)
                # =====================================
        # Response Recommendations
        # =====================================

        actions = RESPONSE_ACTIONS.get(alert, [])

        # =====================================
        # Console Output
        # =====================================

        print("\n" + "=" * 60)
        print(f"[{severity}] {alert}")
        print("=" * 60)

        print(f"Time        : {timestamp}")
        print(f"Computer    : {computer}")
        print(f"Source IP   : {source_ip}")

        print("-" * 60)

        print("MITRE ATT&CK")
        print(f"Technique ID : {mitre['technique']}")
        print(f"Technique    : {mitre['name']}")
        print(f"Tactic       : {mitre['tactic']}")

        print("-" * 60)

        print("RISK")
        print(f"Risk Score   : {risk}")

        print("-" * 60)

        print("IOC ENRICHMENT")
        print(f"Abuse Score  : {ioc['abuse_score']}")
        print(f"Country      : {ioc['country']}")
        print(f"ISP          : {ioc['isp']}")

        print("-" * 60)

        print("RECOMMENDED RESPONSE")

        if actions:
            for index, action in enumerate(actions, start=1):
                print(f"{index}. {action}")
        else:
            print("No response playbook available.")

        print("=" * 60)

        # Update last processed record
        last_id = db_id

    conn.close()

    time.sleep(3)