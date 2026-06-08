# SecSnap — Live Forensic Snapshot Daemon

A Python-based background daemon that monitors system activity in real time and automatically captures forensic snapshots when suspicious behavior is detected. Built for SOC and DFIR workflows.

## Features
- Real-time system monitoring across CPU, RAM, network, and disk
- Threshold-based anomaly detection with configurable triggers
- Configurable whitelist for trusted IPs and processes to reduce false positives
- Email alerting when a forensic snapshot is triggered
- Dual format report generation (TXT + JSON)
- Cooldown mechanism to prevent snapshot flooding
- Automatic snapshots directory creation on first run

## What It Monitors
- CPU usage per core and frequency
- RAM consumption and top memory processes
- Active network connections and outbound connections to known malicious ports
- Disk I/O rates and recently modified files in /tmp

## Trigger Conditions
- CPU usage exceeds threshold (default 85%)
- RAM usage exceeds threshold (default 80%)
- Outbound connection to suspicious port (4444, 1337, 31337, 9001, 6667)
- Disk write rate exceeds threshold (default 50 MB/s)

## Whitelist Configuration
To reduce false positives, you can configure trusted IPs and processes that should be ignored during monitoring:

- Whitelisted IPs — Outbound connections to these IPs will not trigger snapshots
- Whitelisted Processes — System or trusted processes can be excluded from triggering alerts
- Whitelisted Ports — Safe ports that should not be treated as suspicious

Edit config.py to define whitelists with examples like localhost IPs, system processes, and common web ports.

## Email Alerting
When a snapshot is triggered, SecSnap can send email alerts.

### Setup
Set environment variables before running:

export EMAIL_ENABLED=true
export EMAIL_SENDER=your@gmail.com
export EMAIL_RECEIVER=your@gmail.com
export EMAIL_PASSWORD=your_app_password_here
export EMAIL_SMTP=smtp.gmail.com
export EMAIL_PORT=587

### Important — Use App Passwords, Not Your Main Password
Never use your main Gmail password. Generate a dedicated App Password:
1. Go to myaccount.google.com/apppasswords
2. Select "Mail" and your device
3. Copy the generated 16-character password
4. Use that as EMAIL_PASSWORD

App Passwords are revocable and isolated — if compromised, revoke without affecting your main account.

### Why Not OAuth2?
OAuth2 is the most secure option for production deployments. For a local forensic tool, App Passwords provide a reasonable security tradeoff. If deploying SecSnap in a team or enterprise environment, implement OAuth2 via the gmail-python library.

### Configuration
Add settings to config.py including enable toggle, SMTP server details, port, authentication credentials, and recipient address.

### Alert Content
Each email includes the timestamp of the trigger, the trigger condition (CPU, RAM, network, or disk), snapshot file paths for both TXT and JSON formats, and key metrics at the time of detection.

## Output
Each triggered snapshot generates two timestamped files in snapshots/ (auto-created if missing):
- snapshot_YYYYMMDD_HHMMSS.txt — human-readable forensic report
- snapshot_YYYYMMDD_HHMMSS.json — structured data for downstream tooling

## Project Structure
secsnap/
├── daemon.py            # Main daemon loop and trigger logic
├── snapshot.py          # Snapshot assembler
├── reporter.py          # TXT + JSON output
├── notifier.py          # Email alerting module
├── config.py            # Thresholds, whitelists, and email settings
├── collectors/
│   ├── cpu.py           # CPU data collector
│   ├── memory.py        # RAM data collector
│   ├── network.py       # Network connections collector
│   └── disk.py          # Disk activity collector
└── snapshots/           # Generated snapshots output here

## Usage
python3 daemon.py

## Configuration
Edit config.py to adjust thresholds, whitelists, and email settings including CPU threshold, RAM threshold, disk write threshold, suspicious ports list, whitelisted IPs, whitelisted processes, whitelisted ports, email alerts toggle, daemon interval, and cooldown seconds.

## Setup
pip install psutil

For email alerts, additional dependencies may be required though smtplib is standard.

## Skills Demonstrated
- Python daemon architecture
- Real-time system monitoring with psutil
- Forensic data collection across CPU, RAM, network, and disk
- Threshold-based anomaly detection
- Whitelist filtering for false positive reduction
- Email alerting integration for SOC workflows
- Dual format report generation (TXT + JSON)
- DFIR and SOC-relevant incident response workflows

## Author
Abiram R — Aspiring SOC Analyst | ISC2 CC Candidate
GitHub: https://github.com/abiramr44
Medium: https://medium.com/@abiramr44
LinkedIn: https://linkedin.com/in/abiramr44
