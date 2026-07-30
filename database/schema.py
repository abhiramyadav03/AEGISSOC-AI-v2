DATABASE_SCHEMA = """
CREATE TABLE IF NOT EXISTS security_events (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    event_id INTEGER,
    timestamp TEXT,
    username TEXT,
    computer TEXT,
    source_ip TEXT,
    log_source TEXT,
    event_type TEXT,
    raw_message TEXT

);

CREATE TABLE IF NOT EXISTS alerts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    event_id INTEGER,
    alert_name TEXT,
    severity TEXT,
    timestamp TEXT,
    computer TEXT,
    status TEXT,

    mitre_technique TEXT,
    mitre_name TEXT,
    mitre_tactic TEXT,
    risk_score INTEGER

);
"""