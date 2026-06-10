import smtplib
import ssl
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(trigger, timestamp):
    if not config.EMAIL_ENABLED:
        return

    if not config.EMAIL_PASSWORD:
        print('[!] Email alert skipped: EMAIL_PASSWORD not set in environment')
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

        context = ssl.create_default_context()

        with smtplib.SMTP(config.EMAIL_SMTP, config.EMAIL_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.send_message(msg)

        print(f'[+] Alert email sent to {config.EMAIL_RECEIVER}')

    except smtplib.SMTPAuthenticationError:
        print('[!] Email authentication failed. Use a Gmail App Password, not your main account password.')
        print('[!] Generate one at: https://myaccount.google.com/apppasswords')
    except smtplib.SMTPException as e:
        print(f'[!] SMTP error: {e}')
    except Exception as e:
        print(f'[!] Email failed: {e}')
