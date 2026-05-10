import time
import logging
import config
from detector import run_all_checks
from snapshot import take_snapshot
from reporter import save_snapshot
from notifier import send_alert

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

last_snapshot_time = 0

def should_snapshot():
    global last_snapshot_time
    now = time.time()
    if now - last_snapshot_time < config.COOLDOWN_SECONDS:
        return False
    last_snapshot_time = now
    return True

def run():
    print('[*] SecSnap daemon started')
    print(f'[*] Monitoring every {config.DAEMON_INTERVAL}s')
    print(f'[*] Whitelisted IPs: {config.WHITELISTED_IPS}')
    print(f'[*] Whitelisted Processes: {config.WHITELISTED_PROCESSES}')
    print('[*] Press Ctrl+C to stop\n')
    logging.info('SecSnap daemon started')

    while True:
        try:
            trigger = run_all_checks()

            if trigger and should_snapshot():
                logging.warning(trigger)
                snap, ts = take_snapshot(trigger)
                save_snapshot(snap, ts)
                print(f'[+] Snapshot saved — trigger: {trigger}\n')
                send_alert(trigger, ts)
            else:
                print(f'[.] System nominal', end='\r')

            time.sleep(config.DAEMON_INTERVAL)

        except KeyboardInterrupt:
            print('\n[*] SecSnap stopped')
            logging.info('SecSnap daemon stopped')
            break
        except Exception as e:
            logging.error(f'Error in daemon loop: {e}')
            time.sleep(config.DAEMON_INTERVAL)

if __name__ == '__main__':
    run()
