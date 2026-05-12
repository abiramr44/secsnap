import os

DAEMON_INTERVAL = 10

CPU_THRESHOLD = 85.0
MEMORY_THRESHOLD = 80.0
DISK_WRITE_THRESHOLD = 50

SUSPICIOUS_PORTS = [
    4444,
    1337,
    31337,
    9001,
    6667,
]

SNAPSHOT_DIR = "snapshots"
LOG_FILE = "secsnap.log"

COOLDOWN_SECONDS = 30

WHITELISTED_IPS = [
    "127.0.0.1",
    "10.0.2.2",
    "192.168.1.1",
]

WHITELISTED_PROCESSES = [
    "systemd",
    "kworker",
    "Xorg",
    "python3",
]

EMAIL_ENABLED = False
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', '')
EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER', '')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
EMAIL_SMTP = os.environ.get('EMAIL_SMTP', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
