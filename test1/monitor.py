import subprocess
import json
import socket
from datetime import datetime
import os

OUTPUT_DIR = "/var/log/monitor"

SERVICE_MAPPING = {
    "httpd": "apache2",
    "rabbitMQ": "rabbitmq-server",
    "postgreSQL": "postgresql"
}

def check_service_status(service_name):
    system_service_name = SERVICE_MAPPING.get(service_name, service_name)
    
    try:
        result = subprocess.run(
            ['service', system_service_name, 'status'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return "UP" if result.returncode == 0 else "DOWN"

    except Exception as e:
        print(f"Error checking service {service_name}: {e}")
        return "DOWN"


def get_hostname():
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"Error getting hostname: {e}")
        return "unknown"


def create_service_json(service_name, service_status, host_name):
    return {
        "service_name": service_name,
        "service_status": service_status,
        "host_name": host_name,
        "timestamp": datetime.utcnow().isoformat()
    }


def write_json_to_file(service_name, json_data):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{service_name}-status-{timestamp}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(json_data, f, indent=2)
        print(f"Wrote status to {filepath}")
    except Exception as e:
        print(f"Error writing file {filepath}: {e}")


def monitor_all_services():
    host_name = get_hostname()
    
    for service_name in SERVICE_MAPPING.keys():
        status = check_service_status(service_name)
        json_data = create_service_json(service_name, status, host_name)
        write_json_to_file(service_name, json_data)

if __name__ == "__main__":
    monitor_all_services()