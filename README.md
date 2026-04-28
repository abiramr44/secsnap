# SecSnap — Live Forensic Snapshot Daemon

A Python-based background daemon that monitors system activity in real time and automatically captures forensic snapshots when suspicious behavior is detected. Built for SOC and DFIR workflows.

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

## Output
Each triggered snapshot generates two timestamped files in snapshots/:
- snapshot_YYYYMMDD_HHMMSS.txt — human-readable forensic report
- snapshot_YYYYMMDD_HHMMSS.json — structured data for downstream tooling

## Project Structure
secsnap/
├── daemon.py            # Main daemon loop and trigger logic
├── snapshot.py          # Snapshot assembler
├── reporter.py          # TXT + JSON output
├── config.py            # Thresholds and settings
├── collectors/
│   ├── cpu.py           # CPU data collector
│   ├── memory.py        # RAM data collector
│   ├── network.py       # Network connections collector
│   └── disk.py          # Disk activity collector
└── snapshots/           # Generated snapshots output here

## Usage
python3 daemon.py

## Configuration
Edit config.py to adjust thresholds:
- CPU_THRESHOLD — CPU % to trigger snapshot
- MEMORY_THRESHOLD — RAM % to trigger snapshot
- DISK_WRITE_THRESHOLD — MB/s write rate to trigger
- SUSPICIOUS_PORTS — list of ports to flag
- DAEMON_INTERVAL — seconds between checks
- COOLDOWN_SECONDS — minimum gap between snapshots

## Setup
pip install psutil

## Skills Demonstrated
- Python daemon architecture
- Real-time system monitoring with psutil
- Forensic data collection across CPU, RAM, network, and disk
- Threshold-based anomaly detection
- Dual format report generation (TXT + JSON)
- DFIR and SOC-relevant incident response workflows

## Author
Abiram R — Aspiring SOC Analyst | ISC2 CC Candidate
GitHub: https://github.com/abiramr44
Medium: https://medium.com/@abiramr44
LinkedIn: https://linkedin.com/in/abiramr44
