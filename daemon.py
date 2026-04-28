import time
import logging
import psutil
import config
from snapshot import take_snapshot
from reporter import save_snapshot

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

last_snapshot_time = 0

def should_snapshot(reason):
    global last_snapshot_time
    now = time.time()
    if now - last_snapshot_time < config.COOLDOWN_SECONDS:
        logging.info(f'Cooldown active — skipping snapshot for: {reason}')
        return False
    last_snapshot_time = now
    return True

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    if usage > config.CPU_THRESHOLD:
        reason = f'CPU_SPIKE: {usage:.2f}%'
        logging.warning(reason)
        return reason
    return None

def check_memory():
    mem = psutil.virtual_memory()
    if mem.percent > config.MEMORY_THRESHOLD:
        reason = f'MEMORY_SPIKE: {mem.percent:.2f}%'
        logging.warning(reason)
        return reason
    return None

def check_network():
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr and conn.raddr.port in config.SUSPICIOUS_PORTS:
            reason = f'SUSPICIOUS_CONNECTION: {conn.raddr.ip}:{conn.raddr.port} PID {conn.pid}'
            logging.warning(reason)
            return reason
    return None

def check_disk():
    io_start = psutil.disk_io_counters()
    time.sleep(1)
    io_end = psutil.disk_io_counters()
    write_mb = (io_end.write_bytes - io_start.write_bytes) / 1024 / 1024
    if write_mb > config.DISK_WRITE_THRESHOLD:
        reason = f'DISK_WRITE_SPIKE: {write_mb:.2f} MB/s'
        logging.warning(reason)
        return reason
    return None

def run():
    print('[*] SecSnap daemon started')
    print(f'[*] Monitoring every {config.DAEMON_INTERVAL}s')
    print(f'[*] Thresholds — CPU: {config.CPU_THRESHOLD}% | RAM: {config.MEMORY_THRESHOLD}% | Disk: {config.DISK_WRITE_THRESHOLD}MB/s')
    print(f'[*] Suspicious ports: {config.SUSPICIOUS_PORTS}')
    print('[*] Press Ctrl+C to stop\n')
    logging.info('SecSnap daemon started')

    while True:
        try:
            trigger = check_cpu() or check_memory() or check_network() or check_disk()

            if trigger and should_snapshot(trigger):
                snap, ts = take_snapshot(trigger)
                save_snapshot(snap, ts)
                print(f'[+] Snapshot saved — trigger: {trigger}\n')
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
