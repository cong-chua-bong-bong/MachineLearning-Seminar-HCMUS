from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
import os
import subprocess

IMG_FOLDER = os.path.join('static')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    file = request.files['image']
    filename = secure_filename(file.filename)
    test_folder = os.path.join(IMG_FOLDER, 'images', 'test')
    file.save(os.path.join(test_folder, filename))
    print(os.path.join(test_folder, filename))
    result = subprocess.run(['python', 'predict.py', '--test-image', f'{os.path.join(test_folder, filename)}'], capture_output=True)

    output = int(result.stdout.decode().splitlines()[-1])

    predicted_result = None
    if output == 0:
        predicted_result = 'máy bay'
    elif output == 1:
        predicted_result = 'mèo'
    else:
        predicted_result = 'chó'

    return render_template('index.html', predicted_result = predicted_result, filename = os.path.join(test_folder, filename))

if __name__ == '__main__':
    app.run()