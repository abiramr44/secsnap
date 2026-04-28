import json
import os
import config

def save_snapshot(snapshot, filename_ts):
    os.makedirs(config.SNAPSHOT_DIR, exist_ok=True)

    txt_path = os.path.join(config.SNAPSHOT_DIR, f'snapshot_{filename_ts}.txt')
    json_path = os.path.join(config.SNAPSHOT_DIR, f'snapshot_{filename_ts}.json')

    with open(json_path, 'w') as f:
        json.dump(snapshot, f, indent=4)
    print(f'[+] JSON snapshot saved: {json_path}')

    with open(txt_path, 'w') as f:
        f.write('=' * 60 + '\n')
        f.write('         SECSNAP FORENSIC SNAPSHOT\n')
        f.write(f'         {snapshot["timestamp"]}\n')
        f.write(f'         TRIGGER: {snapshot["trigger"]}\n')
        f.write('=' * 60 + '\n\n')

        f.write('[CPU]\n')
        f.write('-' * 40 + '\n')
        cpu = snapshot['cpu']
        f.write(f'  Total Usage    : {cpu["total_usage_percent"]:.2f}%\n')
        f.write(f'  Core Count     : {cpu["core_count"]}\n')
        f.write(f'  Per Core       : {cpu["per_core_usage"]}\n')
        f.write(f'  Frequency MHz  : {cpu["frequency_mhz"]["current"]}\n')
        f.write(f'  Load Avg 1m    : {cpu["load_average_1_5_15"]["1min"]}\n\n')

        f.write('[MEMORY]\n')
        f.write('-' * 40 + '\n')
        ram = snapshot['memory']['ram']
        f.write(f'  Total          : {ram["total_mb"]} MB\n')
        f.write(f'  Used           : {ram["used_mb"]} MB ({ram["percent_used"]}%)\n')
        f.write(f'  Free           : {ram["free_mb"]} MB\n')
        f.write('  Top Processes  :\n')
        for proc in snapshot['memory']['top_memory_processes']:
            f.write(f'    PID {proc["pid"]} {proc["name"]} — {proc["memory_percent"]}%\n')
        f.write('\n')

        f.write('[NETWORK]\n')
        f.write('-' * 40 + '\n')
        net = snapshot['network']
        f.write(f'  Active Connections : {net["active_connections"]}\n')
        f.write(f'  Suspicious         : {len(net["suspicious_connections"])}\n')
        if net['suspicious_connections']:
            for s in net['suspicious_connections']:
                f.write(f'    !! {s["remote_ip"]}:{s["remote_port"]} PID {s["pid"]}\n')
        f.write(f'  Bytes Sent         : {net["io_counters"]["bytes_sent"]}\n')
        f.write(f'  Bytes Received     : {net["io_counters"]["bytes_recv"]}\n\n')

        f.write('[DISK]\n')
        f.write('-' * 40 + '\n')
        for part in snapshot['disk']['partitions']:
            f.write(f'  {part["device"]} → {part["mountpoint"]} ({part["fstype"]})\n')
            f.write(f'  Used: {part["used_gb"]} GB / {part["total_gb"]} GB ({part["percent_used"]}%)\n')
        io = snapshot['disk']['io_counters']
        f.write(f'  Read             : {io["read_mb"]} MB\n')
        f.write(f'  Write            : {io["write_mb"]} MB\n\n')

        f.write('=' * 60 + '\n')
        f.write('  END OF SNAPSHOT\n')
        f.write('=' * 60 + '\n')

    print(f'[+] TXT snapshot saved: {txt_path}')
