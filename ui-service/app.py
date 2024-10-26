from flask import Flask, render_template, request, jsonify, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest, start_http_server
import psutil
import os
import time

app = Flask(__name__)

# Registro de métricas personalizado
registry = CollectorRegistry()

# Registro personalizado para evitar conflitos
cpu_usage = Gauge('cpu_usage', 'CPU Usage (%)', registry=registry)
memory_usage = Gauge('memory_usage', 'Memory Usage (%)', registry=registry)
disk_usage = Gauge('disk_usage', 'Disk Usage (%)', registry=registry)
network_sent = Gauge('network_sent_bytes', 'Network Sent (Bytes)', registry=registry)
network_received = Gauge('network_received_bytes', 'Network Received (Bytes)', registry=registry)

def collect_metrics():
    # CPU e Memória
    cpu_usage.set(psutil.cpu_percent(interval=1))
    memory_usage.set(psutil.virtual_memory().percent)
    
    # Disco
    disk_usage.set(psutil.disk_usage('/').percent)
    
    # Rede
    net_io = psutil.net_io_counters()
    network_sent.set(net_io.bytes_sent)
    network_received.set(net_io.bytes_recv)

@app.route('/metrics')
def metrics():
    """Rota para expor as métricas customizadas."""
    collect_metrics()  # Atualiza as métricas
    return Response(generate_latest(registry), mimetype="text/plain")
    
# Serve the frontend HTML file
@app.route('/')
def index():
    return render_template('index.html')
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)