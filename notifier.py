import smtplib
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(trigger, timestamp):
    if not config.EMAIL_ENABLED:
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = config.EMAIL_SENDER
        msg['To'] = config.EMAIL_RECEIVER
        msg['Subject'] = f'[SecSnap ALERT] {trigger}'

        body = f"""
SecSnap Forensic Alert
======================
Trigger   : {trigger}
Snapshot  : snapshots/snapshot_{timestamp}.txt

Review the snapshot files immediately for forensic details.
        """

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(config.EMAIL_SMTP, config.EMAIL_PORT)
        server.starttls()
        server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f'[+] Alert email sent to {config.EMAIL_RECEIVER}')

    except Exception as e:
        print(f'[!] Email failed: {e}')
