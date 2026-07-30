from collections import defaultdict
from datetime import datetime, timedelta

failed_logins = defaultdict(list)


def correlate_failed_login(source_ip, timestamp):

    try:
        now = datetime.fromisoformat(timestamp)
    except:
        return False

    failed_logins[source_ip].append(now)

    window = now - timedelta(minutes=5)

    failed_logins[source_ip] = [
        t for t in failed_logins[source_ip]
        if t >= window
    ]

    return len(failed_logins[source_ip]) >= 5