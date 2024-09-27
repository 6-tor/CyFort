import psutil
import socket
import boto3
import subprocess
import os
import time
import json
from datetime import datetime

# Função para coletar detalhes da CPU e Memória
def get_cpu_memory_details():
    cpu_info = {
        'cpu_count': psutil.cpu_count(logical=False),
        'cpu_logical_count': psutil.cpu_count(logical=True),
        'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else 'N/A',
        'total_memory': psutil.virtual_memory().total
    }
    return cpu_info

# Função para monitorar estado do Disco (incluindo SMART)
def get_disk_status():
    disk_usage = psutil.disk_usage('/')._asdict()
    
    # Verificar status SMART se disponível (para Linux)
    try:
        smart_data = subprocess.check_output(['sudo', 'smartctl', '-a', '/dev/sda']).decode()
    except Exception as e:
        smart_data = str(e)
    
    return {
        'disk_usage': disk_usage,
        'smart_data': smart_data
    }

# Função para coletar dados de rede (uso de largura de banda, IP e conexões)
def get_network_info():
    net_io = psutil.net_io_counters()._asdict()
    connections = psutil.net_connections()
    active_connections = [
        {
            'fd': conn.fd, 'family': conn.family, 'type': conn.type,
            'laddr': conn.laddr, 'raddr': conn.raddr, 'status': conn.status
        }
        for conn in connections if conn.status == 'ESTABLISHED'
    ]
    
    # Coletar IP e MAC address
    interfaces = psutil.net_if_addrs()
    net_info = {}
    for iface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                net_info[iface] = {'ip_address': addr.address}
            elif addr.family == psutil.AF_LINK:
                if iface not in net_info:
                    net_info[iface] = {}
                net_info[iface]['mac_address'] = addr.address

    return {
        'net_io': net_io,
        'active_connections': active_connections,
        'net_info': net_info
    }


# Função para coletar eventos críticos do sistema (logs de eventos)
def get_system_events():
    logs = []
    
    # Windows Event Viewer (se estiver no Windows)
    if os.name == 'nt':
        try:
            import win32evtlog
            server = 'localhost'  # servidor local
            log_type = 'System'
            hand = win32evtlog.OpenEventLog(server, log_type)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            total = win32evtlog.GetNumberOfEventLogRecords(hand)

            events = win32evtlog.ReadEventLog(hand, flags, 0)
            for event in events:
                logs.append({
                    'source': event.SourceName,
                    'event_id': event.EventID,
                    'time_generated': event.TimeGenerated.Format(),
                    'event_type': event.EventType,
                })
        except Exception as e:
            logs.append(str(e))
    
    # Linux Syslog (se estiver no Linux)
    elif os.name == 'posix':
        try:
            syslog_output = subprocess.check_output(['tail', '-n', '50', '/var/log/syslog']).decode()
            logs.append(syslog_output)
        except Exception as e:
            logs.append(str(e))
    
    return logs

# Função para coletar status de atualizações do sistema e patches (exemplo para Linux)
def get_system_updates():
    updates = []
    
    if os.name == 'posix':
        try:
            updates_info = subprocess.check_output(['apt', 'list', '--upgradable']).decode()
            updates.append(updates_info)
        except Exception as e:
            updates.append(str(e))
    
    return updates

# Função para coletar processos em execução com consumo de CPU, memória e disco
def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'io_counters']):
        try:
            proc_info = proc.info
            processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

# Função para coletar o tempo de atividade desde a última reinicialização
def get_uptime():
    boot_time = psutil.boot_time()
    uptime = datetime.now() - datetime.fromtimestamp(boot_time)
    return str(uptime)

# Função para coletar tempo ocioso e de utilização
def get_idle_and_usage_times():
    idle_time = psutil.cpu_times().idle
    active_time = psutil.cpu_times().user + psutil.cpu_times().system
    return {
        'idle_time': idle_time,
        'active_time': active_time
    }

# Função para enviar logs para o AWS S3 no formato JSON
def send_to_aws_s3(log_data, bucket_name, file_name):
    s3 = boto3.client('s3')
    
    # Convertendo os dados coletados para JSON formatado
    log_data_json = json.dumps(log_data, indent=4)
    
    # Enviar o log no formato JSON para o S3
    s3.put_object(
        Body=log_data_json,
        Bucket=bucket_name,
        Key=file_name
    )
    print(f"Log enviado para {bucket_name}/{file_name}")

# Coleta geral de métricas e logs
def collect_system_metrics():
    metrics = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_memory_details': get_cpu_memory_details(),
        'disk_status': get_disk_status(),
        'network_info': get_network_info(),
        'system_events': get_system_events(),
        'system_updates': get_system_updates(),
        'running_processes': get_running_processes(),
        'uptime': get_uptime(),
        'idle_and_usage_times': get_idle_and_usage_times()
    }
    return metrics

# Configurações do AWS e nome do bucket
bucket_name = 'cf-data-storage'
file_prefix = 'system_metrics'

# Loop para coleta e envio de logs
while True:
    metrics = collect_system_metrics()
    
    # Nome do arquivo baseado na data/hora
    file_name = f"system_metrics_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    
    # Enviar o log no formato JSON para AWS S3
    send_to_aws_s3(metrics, bucket_name, file_name)
    
    # Esperar 60 segundos antes de coletar novamente
    time.sleep(60)
