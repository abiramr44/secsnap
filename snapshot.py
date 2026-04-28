import datetime
from collectors.cpu import collect as collect_cpu
from collectors.memory import collect as collect_memory
from collectors.network import collect as collect_network
from collectors.disk import collect as collect_disk

def take_snapshot(trigger_reason):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename_ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    print(f'[!] TRIGGER: {trigger_reason}')
    print(f'[*] Taking forensic snapshot at {timestamp}...')

    snapshot = {
        'timestamp': timestamp,
        'trigger': trigger_reason,
        'cpu': collect_cpu(),
        'memory': collect_memory(),
        'network': collect_network(),
        'disk': collect_disk()
    }

    print(f'[+] Snapshot captured successfully')
    return snapshot, filename_ts
