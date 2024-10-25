from PIL import Image, ImageDraw
import numpy as np
import random
import os 

def ensure_output_directory(directory):
    """Verifica se o diretório de saída existe, se não, cria."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_high_resolution_image(text, image_number):
    width, height = 3840, 2160  # High resolution
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    draw.text((50, 50), text, fill="black")
    image_path = f"/app/output/high_res_image_{image_number}.png"
    image.save(image_path)
    return image_path

def generate_complex_pattern_image(text, image_number):
    width, height = 1920, 1080
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    for _ in range(1000):
        x0, y0 = random.randint(0, width), random.randint(0, height)
        x1, y1 = random.randint(0, width), random.randint(0, height)
        draw.line([x0, y0, x1, y1], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    image_path = f"/app/output/complex_pattern_image_{image_number}.png"
    image.save(image_path)
    return image_path

def generate_generative_art(text, image_number):
    width, height = 1920, 1080
    noise = np.random.rand(height, width, 3) * 255
    image = Image.fromarray(noise.astype('uint8'))
    image_path = f"/app/output/generative_art_image_{image_number}.png"
    image.save(image_path)
    return image_path

def mandelbrot(c, max_iter):
    z = complex(0, 0)  # Inicializa z como um número complexo
    for n in range(max_iter):
        if abs(z) > 2:  # Verifica se z saiu do conjunto
            return n
        z = z*z + c  # Calcula z
    return max_iter  # Retorna o máximo de iterações se não divergiu

def generate_mandelbrot(image_number, max_iter=100): #max_iter=1000
    # Baixa Resolução: 640, 360 
    # Meia Resolução: 1920, 1080 (Full HD)
    # Alta Resulução: 3840, 2160 (4K)
    width, height =  1920, 1080
    
    image = Image.new('RGB', (width, height))
    pixels = image.load()

    # Definindo os limites do plano complexo (espaço de zoom)
    xmin, xmax = -2.5, 1
    ymin, ymax = -1, 1

    total_pixels = width * height  # Total de pixels para cálculo de progresso
    
    # Gerando o fractal
    for x in range(width):
        for y in range(height):
            # Mapear coordenadas da tela para o plano complexo
            real = xmin + (x / width) * (xmax - xmin)
            imag = ymin + (y / height) * (ymax - ymin)
            c = complex(real, imag)
            
            # Determinar se o ponto c pertence ao conjunto de Mandelbrot
            m = mandelbrot(c, max_iter)
            
            # Colorir o pixel com base no número de iterações
            color_value = 255 - int(m * 255 / max_iter)
            pixels[x, y] = (color_value, color_value, color_value)
            
    # Salvando a imagem no caminho especificado
    image_path = f"/app/output/mandelbrot_{image_number}.png"
    image.save(image_path)

    return image_path