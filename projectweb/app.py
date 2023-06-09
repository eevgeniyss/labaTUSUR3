from flask import Flask, render_template, request
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Получение загруженного файла из формы
    image_file = request.files['image']
    scale = float(request.form['scale'])

    # Сохранение загруженного файла на сервере
    image_path = 'static/uploads/original_image.jpg'
    image_file.save(image_path)

    # Загрузка и изменение размера изображения с помощью библиотеки Pillow
    image = Image.open(image_path)
    width, height = image.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = image.resize((new_width, new_height))
    resized_image_path = 'static/uploads/resized_image.jpg'
    resized_image.save(resized_image_path)

    # Анализ цветов исходного и полученного изображений с помощью библиотеки OpenCV
    original_colors = analyze_colors(image)
    resized_colors = analyze_colors(resized_image)

    # Создание графиков распределения цветов с помощью библиотеки Matplotlib
    plot_original_colors(original_colors)
    plot_resized_colors(resized_colors)

    return render_template('result.html', original_image=image_path, resized_image=resized_image_path)

def analyze_colors(image):
    image_array = np.array(image)
    b, g, r = cv2.split(image_array)
    colors = [b.flatten(), g.flatten(), r.flatten()]
    return colors

def plot_original_colors(colors):
    plt.hist(colors, bins=256, color=['b', 'g', 'r'], alpha=0.7, label=['Blue', 'Green', 'Red'])
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.title('Color Distribution - Original Image')
    plt.legend()
    plt.savefig('static/uploads/original_histogram.png')
    plt.clf()

def plot_resized_colors(colors):
    plt.hist(colors, bins=256, color=['b', 'g', 'r'], alpha=0.7, label=['Blue', 'Green', 'Red'])
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.title('Color Distribution - Resized Image')
    plt.legend()
    plt.savefig('static/uploads/resized_histogram.png')
    plt.clf()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# cd D:\IT\mainpy\projectweb
# pip install -r requirements.txt
# python app.py