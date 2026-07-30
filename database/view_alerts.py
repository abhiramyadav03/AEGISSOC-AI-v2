import sqlite3

conn = sqlite3.connect("database/aegis_soc.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, event_id, alert_name, severity, timestamp, computer, status
FROM alerts
ORDER BY id DESC
""")

rows = cursor.fetchall()

print("=" * 80)
print("ALERTS")
print("=" * 80)

for row in rows:
    print(row)

conn.close()