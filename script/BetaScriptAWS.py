import psutil
import requests
import logging
from datetime import datetime
import json

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

def send_metrics_to_server(metrics):
    url = 'Futuro server na AWS'  # Substituir pelo endpoint real
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(metrics))
        if response.status_code == 200:
            logging.info('Metrics sent successfully.')
        else:
            logging.error(f'Failed to send metrics. Status code: {response.status_code}')
    except Exception as e:
        logging.error(f'Error sending metrics: {e}')

def main():
    logging.info('Starting system metrics collection...')
    while True:
        metrics = collect_system_metrics()
        logging.info(f'Collected metrics: {metrics}')
        send_metrics_to_server(metrics)

if __name__ == '__main__':
    main()
