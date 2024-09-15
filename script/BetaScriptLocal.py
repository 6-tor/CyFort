import psutil
import logging
from datetime import datetime

# Configuração do logging
logging.basicConfig(filename='system_logs.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def collect_system_metrics():
    metrics = {
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'network_info': psutil.net_io_counters()._asdict()
    }
    return metrics

def display_metrics(metrics):
    print("System Metrics at", datetime.now())
    print(f"CPU Usage: {metrics['cpu_usage']}%")
    print(f"Memory Usage: {metrics['memory_usage']}%")
    print(f"Disk Usage: {metrics['disk_usage']}%")
    print("Network Info:")
    print(f"  Bytes Sent: {metrics['network_info']['bytes_sent']}")
    print(f"  Bytes Received: {metrics['network_info']['bytes_recv']}")
    print(f"  Packets Sent: {metrics['network_info']['packets_sent']}")
    print(f"  Packets Received: {metrics['network_info']['packets_recv']}")
    print(f"  Errors In: {metrics['network_info']['errin']}")
    print(f"  Errors Out: {metrics['network_info']['errout']}")
    print(f"  Drops In: {metrics['network_info']['dropin']}")
    print(f"  Drops Out: {metrics['network_info']['dropout']}")
    print("\n")

def main():
    logging.info('Starting system metrics collection...')
    while True:
        metrics = collect_system_metrics()
        logging.info(f'Collected metrics: {metrics}')
        display_metrics(metrics)

if __name__ == '__main__':
    main()
