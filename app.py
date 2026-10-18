import re
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

BASE = Path.home() / "soc-dashboard"
SSH_LOG = BASE / "ssh-events.log"
AUDIT_LOG = BASE / "file-events.log"
WATCHED_FILE = "/etc/soc-lab-test.conf"

st.set_page_config(
    page_title="SOC Security Monitoring",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ SOC Security Monitoring Dashboard")
st.caption("Ubuntu ARM64 | SSH Monitoring | Auditd File Integrity")


def read_ssh_events():
    events = []
    if not SSH_LOG.exists():
        return events

    for line in SSH_LOG.read_text(errors="replace").splitlines():
        if "Failed password" in line:
            event, severity = "Failed SSH Login", "Medium"
        elif "Accepted password" in line:
            event, severity = "Successful SSH Login", "Informational"
        else:
            continue

        events.append({
            "Timestamp": line.split(" ")[0],
            "Event": event,
            "Severity": severity,
            "Details": line
        })
    return events

def read_audit_events():
    events = []
    if not AUDIT_LOG.exists():
        return events

    content = AUDIT_LOG.read_text(errors="replace")

    for block in re.split(r"(?m)^----\s*$", content):
        if not block.strip():
            continue

        if "type=SYSCALL" not in block:
            continue
        if "success=yes" not in block:
            continue
        if "type=PATH" not in block:
            continue
        if f"name={WATCHED_FILE}" not in block:
            continue

        match = re.search(
            r"msg=audit\((\d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2}:\d{2}\.\d+):(\d+)\)",
            block
        )
        if not match:
            continue

        timestamp = match.group(1)
        command = re.search(r"proctitle=([^\n]+)", block)
        process = re.search(r"exe=([^\s]+)", block)

        events.append({
            "Event ID": match.group(2),
            "Timestamp": timestamp,
            "Event": "Monitored File Activity",
            "Severity": "Medium",
            "File": WATCHED_FILE,
            "Process": process.group(1) if process else "Unknown",
            "Command": command.group(1) if command else "Unavailable"
        })

    return events


def live_dashboard():
    ssh_events = read_ssh_events()
    audit_events = read_audit_events()

    st.subheader("Security Overview")

    a, b, c, d = st.columns(4)
    a.metric("SSH Events", len(ssh_events))
    b.metric(
        "Failed SSH Logins",
        sum(e["Event"] == "Failed SSH Login" for e in ssh_events)
    )
    c.metric(
        "Successful SSH Logins",
        sum(e["Event"] == "Successful SSH Login" for e in ssh_events)
    )
    d.metric("Auditd File Events", len(audit_events))

    st.divider()
    st.subheader("SSH Authentication Monitoring")

    if ssh_events:
        ssh_df = pd.DataFrame(ssh_events)
        st.dataframe(ssh_df, width="stretch", hide_index=True)
        st.bar_chart(ssh_df["Event"].value_counts())

    else:
        st.info("No exported SSH events found.")

    st.divider()
    st.subheader("File Integrity Monitoring")
    st.write("Monitored file:", WATCHED_FILE)

    if audit_events:
        audit_df = pd.DataFrame(audit_events)
        st.dataframe(audit_df, width="stretch", hide_index=True)
        st.success(
            f"{len(audit_events)} monitored file-access event(s) found."
        )
    else:
        st.info("No matching Auditd file events found.")

    st.caption(
        "Dashboard refreshes every 60 seconds. "
        "SSH exports update through cron; Auditd export "
        "currently requires a manual refresh."
    )


live_dashboard()
