import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3
import pandas as pd
import plotly.express as px

# ==========================================
# Configuration
# ==========================================

DATABASE = "database/aegis_soc.db"

st.set_page_config(
    page_title="AEGIS SOC Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st_autorefresh(
    interval=3000,
    key="refresh"
)

# ==========================================
# Helper Functions
# ==========================================

def severity_color(level):

    if level == "CRITICAL":
        return "🔴"

    elif level == "HIGH":
        return "🟠"

    elif level == "MEDIUM":
        return "🟡"

    return "🟢"


def load_alerts():

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql_query("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
    """, conn)

    conn.close()

    return df


# ==========================================
# Load Database
# ==========================================

df = load_alerts()

# ==========================================
# Live Notifications
# ==========================================

if not df.empty:

    latest = df.iloc[0]

    if latest["severity"] == "CRITICAL":

        st.error(
            f"""
🔥 CRITICAL ALERT

Alert : {latest['alert_name']}

Computer : {latest['computer']}

Time : {latest['timestamp']}
"""
        )

    elif latest["severity"] == "HIGH":

        st.warning(
            f"""
🚨 HIGH ALERT

Alert : {latest['alert_name']}

Computer : {latest['computer']}

Time : {latest['timestamp']}
"""
        )

# ==========================================
# Dashboard Title
# ==========================================

st.title("🛡️ AEGIS SOC Dashboard")

st.caption("Real-Time Windows Security Monitoring Platform")

st.divider()

# ==========================================
# Metrics
# ==========================================

total_alerts = len(df)

high_alerts = len(
    df[df["severity"] == "HIGH"]
)

critical_alerts = len(
    df[df["severity"] == "CRITICAL"]
)

medium_alerts = len(
    df[df["severity"] == "MEDIUM"]
)

hosts = (
    df["computer"].nunique()
    if not df.empty else 0
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Alerts",
        total_alerts
    )

with col2:
    st.metric(
        "High",
        high_alerts
    )

with col3:
    st.metric(
        "Critical",
        critical_alerts
    )

with col4:
    st.metric(
        "Hosts",
        hosts
    )

with col5:

    if not df.empty:

        st.metric(
            "Latest Severity",
            f"{severity_color(df.iloc[0]['severity'])} {df.iloc[0]['severity']}"
        )

    else:

        st.metric(
            "Latest Severity",
            "None"
        )

st.divider()

# ==========================================
# Recent Alerts
# ==========================================

st.subheader("📋 Recent Alerts")

if not df.empty:

    columns = [

        "event_id",
        "alert_name",
        "severity",
        "computer",
        "timestamp",
        "status",

        # IOC Enrichment
        "source_ip",
        "abuse_score",
        "country",
        "isp",

        # MITRE ATT&CK
        "mitre_technique",
        "mitre_name",
        "mitre_tactic",

        # Risk Score
        "risk_score"

    ]

    available = [c for c in columns if c in df.columns]

    st.dataframe(
        df[available].head(20),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No alerts found.")

# ==========================================
# Charts
# ==========================================

if not df.empty:

    col1, col2 = st.columns(2)

    # ----------------------------
    # Alert Distribution
    # ----------------------------

    with col1:

        st.subheader("🥧 Alert Distribution")

        fig = px.pie(
            df,
            names="severity",
            hole=0.45,
            title="Alerts by Severity"
        )

        fig.update_traces(textposition="inside")

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ----------------------------
    # Alerts by Computer
    # ----------------------------

    with col2:

        st.subheader("💻 Alerts by Computer")

        computer = (
            df["computer"]
            .value_counts()
            .reset_index()
        )

        computer.columns = [
            "Computer",
            "Alerts"
        ]

        fig = px.bar(
            computer,
            x="Computer",
            y="Alerts",
            text="Alerts",
            color="Alerts"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==========================================
# Attack Timeline
# ==========================================

if not df.empty:

    st.subheader("📈 Attack Timeline")

    timeline = df.copy()

    timeline["timestamp"] = pd.to_datetime(
        timeline["timestamp"]
    )

    timeline = (
        timeline
        .set_index("timestamp")
        .resample("1min")
        .size()
        .reset_index(name="Alerts")
    )

    fig = px.line(
        timeline,
        x="timestamp",
        y="Alerts",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# Top Attack Types
# ==========================================

if not df.empty:

    st.subheader("🔥 Top Attack Types")

    attacks = (
        df["alert_name"]
        .value_counts()
        .reset_index()
    )

    attacks.columns = [
        "Attack",
        "Count"
    ]

    fig = px.bar(
        attacks,
        x="Attack",
        y="Count",
        text="Count",
        color="Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# Severity Breakdown
# ==========================================

if not df.empty:

    st.subheader("🎯 Severity Breakdown")

    severity = (
        df["severity"]
        .value_counts()
        .reset_index()
    )

    severity.columns = [
        "Severity",
        "Count"
    ]

    st.dataframe(
        severity,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==========================================
# Search Alerts
# ==========================================

st.subheader("🔍 Search Alerts")

search = st.text_input(
    "Search by Computer, Alert Name or Event ID"
)

if search:

    result = df[
        df["computer"].astype(str).str.contains(search, case=False, na=False)
        |
        df["alert_name"].astype(str).str.contains(search, case=False, na=False)
        |
        df["event_id"].astype(str).str.contains(search, case=False, na=False)
    ]

    st.dataframe(
    result[available],
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================
# Severity Filter
# ==========================================

st.subheader("🎯 Filter Alerts")

severity_filter = st.selectbox(
    "Select Severity",
    [
        "All",
        "CRITICAL",
        "HIGH",
        "MEDIUM"
    ]
)

if severity_filter == "All":

    filtered = df

else:

    filtered = df[
        df["severity"] == severity_filter
    ]

st.dataframe(
    filtered,
    use_container_width=True
)

st.divider()

# ==========================================
# High Severity Alerts
# ==========================================

st.subheader("🚨 High Severity Alerts")

high_df = df[
    df["severity"].isin(
        [
            "HIGH",
            "CRITICAL"
        ]
    )
]

if not high_df.empty:

   st.dataframe(
    high_df[available],
    use_container_width=True,
    hide_index=True
)

else:

    st.success("No HIGH or CRITICAL alerts.")

st.divider()

# ==========================================
# Latest Critical Alerts
# ==========================================

st.subheader("🔥 Latest Critical Alerts")

critical = df[
    df["severity"] == "CRITICAL"
].head(10)

if not critical.empty:

    st.dataframe(
    critical[available],
    use_container_width=True,
    hide_index=True
)

else:

    st.info("No Critical Alerts Found.")

st.divider()

# ==========================================
# Export Alerts
# ==========================================

st.subheader("📥 Export Alerts")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Alerts CSV",
    data=csv,
    file_name="aegis_alerts.csv",
    mime="text/csv"
)

st.divider()

# ==========================================
# Alert Summary
# ==========================================

st.subheader("📊 Alert Summary")

summary = pd.DataFrame({
    "Metric": [
        "Total Alerts",
        "Critical Alerts",
        "High Alerts",
        "Medium Alerts",
        "Unique Hosts"
    ],
    "Value": [
        len(df),
        len(df[df["severity"] == "CRITICAL"]),
        len(df[df["severity"] == "HIGH"]),
        len(df[df["severity"] == "MEDIUM"]),
        df["computer"].nunique() if not df.empty else 0
    ]
})

st.table(summary)

st.divider()

# ==========================================
# Footer
# ==========================================

st.markdown("---")

st.caption(
    "🛡️ AEGIS SOC AI v2 | Real-Time Security Monitoring Platform"
)

st.caption(
    "Developed using Python • Streamlit • SQLite • Windows Event Logs"
)