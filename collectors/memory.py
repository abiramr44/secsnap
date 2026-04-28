import psutil

def collect():
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()

    top_processes = []
    for proc in sorted(psutil.process_iter(['pid', 'name', 'memory_percent']),
                       key=lambda p: p.info['memory_percent'] or 0,
                       reverse=True)[:5]:
        top_processes.append({
            'pid': proc.info['pid'],
            'name': proc.info['name'],
            'memory_percent': round(proc.info['memory_percent'], 2)
        })

    return {
        'ram': {
            'total_mb': round(ram.total / 1024 / 1024, 2),
            'used_mb': round(ram.used / 1024 / 1024, 2),
            'free_mb': round(ram.free / 1024 / 1024, 2),
            'percent_used': ram.percent
        },
        'swap': {
            'total_mb': round(swap.total / 1024 / 1024, 2),
            'used_mb': round(swap.used / 1024 / 1024, 2),
            'percent_used': swap.percent
        },
        'top_memory_processes': top_processes
    }
