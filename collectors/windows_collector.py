import time
import win32evtlog

from database.db import insert_event
from config.settings import POLL_INTERVAL

SERVER = "localhost"
LOG_TYPE = "System"

hand = win32evtlog.OpenEventLog(SERVER, LOG_TYPE)

flags = (
    win32evtlog.EVENTLOG_BACKWARDS_READ
    | win32evtlog.EVENTLOG_SEQUENTIAL_READ
)

last_record = None

print("=" * 60)
print("AEGIS SOC Collector Started")
print("=" * 60)

while True:

    events = win32evtlog.ReadEventLog(hand, flags, 0)

    if events:

        events.reverse()

        for event in events:

            record = event.RecordNumber

            if last_record is None:
                last_record = record
                continue

            if record <= last_record:
                continue

            # ==========================================
            # Try to extract Source IP
            # ==========================================

            source_ip = "Unknown"

            if event.StringInserts:

                for value in event.StringInserts:

                    if value is None:
                        continue

                    value = str(value).strip()

                    # Very simple IPv4 check
                    if value.count(".") == 3:
                        source_ip = value
                        break

            # ==========================================
            # Store Event
            # ==========================================

            event_data = {
                "event_id": event.EventID & 0xFFFF,
                "timestamp": str(event.TimeGenerated),
                "username": "",
                "computer": event.ComputerName,
                "source_ip": source_ip,
                "log_source": event.SourceName,
                "event_type": LOG_TYPE,
                "raw_message": str(event.StringInserts),
            }

            insert_event(event_data)

            print(f"[+] New Event {event_data['event_id']}")
            print(f"Source IP : {source_ip}")

            last_record = record

    time.sleep(POLL_INTERVAL)