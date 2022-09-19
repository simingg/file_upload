from http.client import REQUEST_ENTITY_TOO_LARGE
from flask import Flask, request, send_from_directory, redirect
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import io
from base64 import b64encode
from PIL import Image

app = Flask(__name__)
#config variables
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MBs
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = b64encode(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@app.route('/images', methods=['GET'])
def home():
    files = os.listdir(app.config['UPLOAD_DIRECTORY'])
    data = []
    for file in files:
        extension = os.path.splitext(file)[1].lower()
        if extension in app.config['ALLOWED_EXTENSIONS']:
            data.append(get_response_image(app.config['UPLOAD_DIRECTORY'] + file))
    return data

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        print(file)
        extension = os.path.splitext(file.filename)[1].lower()
        #ensuring therer is a file
        if file: 
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return 'File is not an image'
            #potential interfere w webserver -> spaces or slashes may throw an error
            file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'], secure_filename(file.filename)
            ))
    except RequestEntityTooLarge:
        return 'File is larger than 16MB'
    return redirect("/")

@app.route('/serve-image/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)
