import psutil
import os
import logging

def collect():
    partitions = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partitions.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total_gb': round(usage.total / 1024 / 1024 / 1024, 2),
                'used_gb': round(usage.used / 1024 / 1024 / 1024, 2),
                'free_gb': round(usage.free / 1024 / 1024 / 1024, 2),
                'percent_used': usage.percent
            })
        except PermissionError:
            continue
        except OSError as e:
            logging.warning(f'Could not read partition {partition.mountpoint}: {e}')
            continue

    io = psutil.disk_io_counters()

    recent_files = []
    tmp_path = os.path.realpath('/tmp')
    try:
        for root, dirs, files in os.walk(tmp_path, followlinks=False):
            real_root = os.path.realpath(root)
            if not real_root.startswith(tmp_path):
                logging.warning(f'Directory traversal attempt blocked: {root}')
                dirs.clear()
                continue
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    real_fpath = os.path.realpath(fpath)
                    if not real_fpath.startswith(tmp_path):
                        logging.warning(f'Symlink escape blocked: {fpath}')
                        continue
                    mtime = os.path.getmtime(fpath)
                    recent_files.append({'path': fpath, 'modified': mtime})
                except (OSError, PermissionError) as e:
                    logging.debug(f'Could not stat file {fpath}: {e}')
                    continue
        recent_files = sorted(recent_files, key=lambda x: x['modified'], reverse=True)[:10]
    except OSError as e:
        logging.error(f'Error walking /tmp directory: {e}')

    return {
        'partitions': partitions,
        'io_counters': {
            'read_mb': round(io.read_bytes / 1024 / 1024, 2) if io else None,
            'write_mb': round(io.write_bytes / 1024 / 1024, 2) if io else None,
            'read_count': io.read_count if io else None,
            'write_count': io.write_count if io else None
        },
        'recent_tmp_files': recent_files
    }
