# 🛡️ AEGIS SOC AI v2

Real-Time Windows SOC Monitoring Platform built with **Python**, **Streamlit**, and **SQLite**.

## 🚀 Features

- Real-time Windows Event Log Collection
- Security Event Detection
- MITRE ATT&CK Mapping
- IOC Enrichment (AbuseIPDB)
- Risk Scoring
- Alert Correlation
- Incident Response Recommendations
- Interactive Streamlit Dashboard
- CSV Export
- Search & Filter Alerts

---

## 🏗️ Project Architecture

```
Windows Event Logs
        │
        ▼
Windows Collector
        │
        ▼
SQLite Database
        │
        ▼
Detection Engine
        │
 ┌───────────────┐
 │ MITRE Mapping │
 │ Risk Scoring  │
 │ IOC Lookup    │
 │ Correlation   │
 └───────────────┘
        │
        ▼
Streamlit Dashboard
```

---

## 📂 Project Structure

```
AEGISSOC-AI-v2/
│
├── collectors/
├── config/
├── dashboard/
├── database/
├── detectors/
├── docs/
├── logs/
├── tests/
├── utils/
├── main.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Plotly
- Pandas
- Requests
- pywin32
- AbuseIPDB API

---

## 📊 Dashboard

The dashboard includes:

- Live Alerts
- Severity Distribution
- Attack Timeline
- Alerts by Host
- Search & Filter
- Risk Score
- IOC Information
- CSV Export

---

## 🧠 Detection Rules

Current detections include:

- Failed Login
- Brute Force Attack
- Admin Privilege Assigned
- New User Created

---

## 🎯 MITRE ATT&CK

Examples:

| Event | Technique |
|--------|-----------|
| Failed Login | T1110 |
| Admin Privilege | T1078 |

---

## ⚙️ Installation

```bash
git clone https://github.com/abhiramyadav03/AEGISSOC-AI-v2.git

cd AEGISSOC-AI-v2

pip install -r requirements.txt
```

Run the project:

```bash
python -m database.db

python -m collectors.windows_collector

python -m detectors.windows_detector

streamlit run dashboard/dashboard.py
```

---

## 📌 Future Improvements

- PDF Incident Reports
- Email Notifications
- Sysmon Integration
- Sigma Rule Engine
- Docker Support
- AI SOC Copilot

---

## 👨‍💻 Author

**Abhiram Rapothula**

- GitHub: https://github.com/abhiramyadav03
- LinkedIn: https://www.linkedin.com/in/rapothulaabhiram/
