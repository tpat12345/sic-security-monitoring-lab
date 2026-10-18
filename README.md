# SOC Security Monitoring Home Lab

## Project Overview
Developed a Security Operations Center (SOC) monitoring lab using Ubuntu Server, Python, Streamlit, and Linux Auditd.

The project monitors SSH authentication activity and file-integrity events through a custom security dashboard.

## Technologies Used
- Ubuntu Server 24.04 LTS (ARM64)
- Python
- Streamlit
- Linux Auditd
- OpenSSH
- Bash scripting
- Linux systemd journal
- Cron
- UTM virtualization

## Key Features
- SSH authentication monitoring
- Failed and successful login detection
- File-integrity monitoring using Auditd
- Security event categorization
- Interactive dashboard and charts
- Automated SSH log exports using cron
- Controlled security-event simulations

## Lab Architecture
Mac Host
   |
   +-- UTM Virtual Machine
          |
          +-- Ubuntu SOC Server
                 |
                 +-- OpenSSH Logs
                 +-- Auditd File Monitoring
                 +-- Python Event Processing
                 +-- Streamlit Security Dashboard

## Validation Results
During lab testing, the dashboard successfully displayed:
- 7 SSH authentication events
- 4 failed SSH login attempts
- 3 successful SSH logins
- 2 Auditd file-integrity events

These are sample results from controlled testing, not permanent totals.

## Current Limitations
- Auditd log exports currently require manual updating.
- The dashboard is designed for a local lab, not production deployment.
- SSH logs are exported periodically rather than continuously streamed.

## Skills Demonstrated
- Linux server administration
- Security monitoring
- Log analysis
- SSH authentication investigation
- File-integrity monitoring
- Python development
- Bash automation
- Security dashboard development
- Troubleshooting and validation

## Future Improvements
- Automate Auditd event exports
- Add alert severity filtering
- Implement event retention and log rotation
- Add network traffic monitoring
- Integrate a SIEM platform

## SOC Dashboard Screenshot
![SOC Security Monitoring Dashboard](sic-dashboard.png)
