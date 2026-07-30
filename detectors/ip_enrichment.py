import requests
from config.api_keys import ABUSEIPDB_API_KEY

API_KEY = ABUSEIPDB_API_KEY

URL = "https://api.abuseipdb.com/api/v2/check"


def check_ip(ip):

    if ip in ("", "-", "Unknown", None):
        return {
            "abuse_score": 0,
            "country": "Unknown",
            "isp": "Unknown"
        }

    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(
            URL,
            headers=headers,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()["data"]

        return {
            "abuse_score": data.get("abuseConfidenceScore", 0),
            "country": data.get("countryCode", "Unknown"),
            "isp": data.get("isp", "Unknown")
        }

    except Exception:
        return {
            "abuse_score": 0,
            "country": "Unknown",
            "isp": "Unknown"
        }