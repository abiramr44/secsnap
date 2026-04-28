import psutil

def collect():
    cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
    cpu_freq = psutil.cpu_freq()
    load_avg = psutil.getloadavg()

    return {
        'total_usage_percent': sum(cpu_percent_per_core) / len(cpu_percent_per_core),
        'per_core_usage': cpu_percent_per_core,
        'core_count': psutil.cpu_count(),
        'frequency_mhz': {
            'current': round(cpu_freq.current, 2) if cpu_freq else None,
            'min': round(cpu_freq.min, 2) if cpu_freq else None,
            'max': round(cpu_freq.max, 2) if cpu_freq else None,
        },
        'load_average_1_5_15': {
            '1min': load_avg[0],
            '5min': load_avg[1],
            '15min': load_avg[2],
        }
    }
