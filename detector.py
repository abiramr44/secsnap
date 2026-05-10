import psutil
import config

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    if usage > config.CPU_THRESHOLD:
        return f'CPU_SPIKE: {usage:.2f}%'
    return None

def check_memory():
    mem = psutil.virtual_memory()
    if mem.percent > config.MEMORY_THRESHOLD:
        return f'MEMORY_SPIKE: {mem.percent:.2f}%'
    return None

def check_network():
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr and conn.raddr.port in config.SUSPICIOUS_PORTS:
            if conn.raddr.ip in config.WHITELISTED_IPS:
                continue
            return f'SUSPICIOUS_CONNECTION: {conn.raddr.ip}:{conn.raddr.port} PID {conn.pid}'
    return None

def check_disk():
    io_start = psutil.disk_io_counters()
    import time
    time.sleep(1)
    io_end = psutil.disk_io_counters()
    write_mb = (io_end.write_bytes - io_start.write_bytes) / 1024 / 1024
    if write_mb > config.DISK_WRITE_THRESHOLD:
        return f'DISK_WRITE_SPIKE: {write_mb:.2f} MB/s'
    return None

def check_processes():
    alerts = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            if proc.info['name'] in config.WHITELISTED_PROCESSES:
                continue
            if (proc.info['memory_percent'] or 0) > 50:
                alerts.append(f'HIGH_MEMORY_PROCESS: {proc.info["name"]} PID {proc.info["pid"]} ({proc.info["memory_percent"]:.1f}%)')
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return alerts[0] if alerts else None

def run_all_checks():
    return (
        check_cpu() or
        check_memory() or
        check_network() or
        check_disk() or
        check_processes()
    )
