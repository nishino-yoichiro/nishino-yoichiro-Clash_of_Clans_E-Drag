from flask import request, send_file, render_template
import os
from main import process_image
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        upload_folder = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER']))
        output_folder = os.path.abspath(os.path.join(app.config['OUTPUT_FOLDER']))
        input_path = os.path.join(upload_folder, file.filename)
        output_path = os.path.join(output_folder, 'output.jpg')
        file.save(input_path)
        
        process_image(input_path, output_path)
        
        return send_file(output_path, mimetype='image/jpeg')