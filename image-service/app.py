from flask import Flask, request, jsonify
from flask_cors import CORS
from image_generator import (
    ensure_output_directory,
    generate_high_resolution_image,
    generate_complex_pattern_image,
    generate_generative_art,
    generate_mandelbrot,
)
import psutil
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import signal
import sys
import os

OUTPUT_DIR = "/app/output"  # Definir o diretório de saída
COUNT_FILE = "image_count.txt"  # Define o caminho do arquivo que armazena a contagem

app = Flask(__name__)
CORS(app)  # This will allow CORS for all routes

# Defina o caminho do arquivo CSV para o diretório mapeado
csv_file_path = os.path.join(OUTPUT_DIR, "monitoramento_IMAGE_SERVICE_MEETING.csv")

# Inicializar o arquivo CSV
csv_file = open(csv_file_path, mode='w', newline='')
csv_writer = None  # Inicializa o escritor de CSV

def initialize_csv():
    global csv_writer
    # Cria o writer e escreve o cabeçalho
    csv_writer = pd.DataFrame(columns=["timestamp", "cpu_usage", "memory_usage", "disk_usage", "network_sent", "network_received"])
    csv_writer.to_csv(csv_file_path, index=False)

def collect_metrics():
    # Coletar métricas
    timestamp = datetime.now()
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net_io = psutil.net_io_counters()
    network_sent_bytes = net_io.bytes_sent
    network_received_bytes = net_io.bytes_recv

    # Adicionar os dados ao CSV
    new_data = {
        "timestamp": timestamp,
        "cpu_usage": cpu,
        "memory_usage": memory,
        "disk_usage": disk,
        "network_sent": network_sent_bytes,
        "network_received": network_received_bytes
    }
    
    # Escreve a nova linha no CSV
    csv_writer = pd.DataFrame([new_data])
    csv_writer.to_csv(csv_file_path, mode='a', header=False, index=False)

def signal_handler(sig, frame):
    print("Encerrando o programa...")
    csv_file.close()  # Fechar o arquivo CSV
    sys.exit(0)

# Inicializa o CSV
initialize_csv()

# Configuração do APScheduler para coletar as métricas a cada 2 segundos
scheduler = BackgroundScheduler()
scheduler.add_job(func=collect_metrics, trigger="interval", seconds=5)
scheduler.start()

# Capturar o sinal SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)
 
def get_image_count():
    """Lê a contagem de imagens do arquivo."""
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "r") as file:
            return int(file.read())
    return 0

def update_image_count():
    """Atualiza a contagem de imagens, incrementando-a em 1."""
    count = get_image_count() + 1
    with open(COUNT_FILE, "w") as file:
        file.write(str(count))
    return count
        
@app.route('/generate', methods=['POST'])
def generate():
    
    ensure_output_directory(OUTPUT_DIR)  # Garantir que o diretório existe
    
    data = request.json
    text = data.get('text', 'Hello World')
    num_images = data.get('numImages', 1)
    image_type = data.get('type')  # Obter o tipo selecionado da requisição

    image_paths = []

    for _ in range(int(num_images)):
        # Atualiza a contagem de imagens antes de gerar a nova imagem
        image_number = get_image_count()  # Lê a contagem atual
        update_image_count()  # Incrementa a contagem para a próxima chamada

        if image_type == 'high_resolution':
            image_path = generate_high_resolution_image(text, image_number)
        elif image_type == 'complex_patterns':
            image_path = generate_complex_pattern_image(text, image_number)
        elif image_type == 'generative_art':
            image_path = generate_generative_art(text, image_number)
        elif image_type == 'fractal_mandelbrot':
            image_path = generate_mandelbrot(image_number)

        image_paths.append(image_path)

    return jsonify({"image_paths": image_paths})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        scheduler.shutdown()  # Parar o scheduler ao encerrar