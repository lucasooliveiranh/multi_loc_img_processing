from flask import Flask, request, jsonify
from flask_cors import CORS
from image_generator import (
    ensure_output_directory,
    generate_high_resolution_image,
    generate_complex_pattern_image,
    generate_generative_art,
    generate_mandelbrot,
)

app = Flask(__name__)
CORS(app)  # This will allow CORS for all routes

OUTPUT_DIR = "/app/output"  # Definir o diretório de saída
        
@app.route('/generate', methods=['POST'])
def generate():
    
    ensure_output_directory(OUTPUT_DIR)  # Garantir que o diretório existe
    
    data = request.json
    text = data.get('text', 'Hello World')
    num_images = data.get('numImages', 1)
    image_type = data.get('type')  # Get the selected type from the request

    image_paths = []

    for i in range(int(num_images)):
        if image_type == 'high_resolution':
            image_path = generate_high_resolution_image(text, i)
        elif image_type == 'complex_patterns':
            image_path = generate_complex_pattern_image(text, i)
        elif image_type == 'generative_art':
            image_path = generate_generative_art(text, i)
        elif image_type == 'fractal_mandelbrot':
            image_path = generate_mandelbrot(i)
        else:
            image_path = generate_high_resolution_image(text, i)  # Default option

        image_paths.append(image_path)

    return jsonify({"image_paths": image_paths})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)