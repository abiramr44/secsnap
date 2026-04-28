import psutil
import config

def collect():
    connections = []
    suspicious = []

    for conn in psutil.net_connections(kind='inet'):
        entry = {
            'fd': conn.fd,
            'type': 'TCP' if conn.type.name == 'SOCK_STREAM' else 'UDP',
            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
            'status': conn.status,
            'pid': conn.pid
        }
        connections.append(entry)

        if conn.raddr and conn.raddr.port in config.SUSPICIOUS_PORTS:
            suspicious.append({
                'remote_ip': conn.raddr.ip,
                'remote_port': conn.raddr.port,
                'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                'pid': conn.pid,
                'status': conn.status
            })

    io = psutil.net_io_counters()

    return {
        'active_connections': len(connections),
        'suspicious_connections': suspicious,
        'connections': connections,
        'io_counters': {
            'bytes_sent': io.bytes_sent,
            'bytes_recv': io.bytes_recv,
            'packets_sent': io.packets_sent,
            'packets_recv': io.packets_recv
        }
    }
