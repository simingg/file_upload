from http.client import REQUEST_ENTITY_TOO_LARGE
from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os

app = Flask(__name__)
#config variables
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MBs
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', 'jpeg', '.png', '.gif']

@app.route('/images', methods=['GET'])
def home():
    files = os.listdir(app.config['UPLOAD_DIRECTORY'])
    response_body = {
       "images" :[],
    }
    for file in files:
        extension = os.path.splitext(file)[1].lower()
        if extension in app.config['ALLOWED_EXTENSIONS']:
            response_body['images'].append(file)
    return response_body

@app.route('/upload', methods=['POST'])
def upload():
    try:
        #post request in html form -> files array -> item in array with 'file' name
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

    return redirect('/')

@app.route('/serve-image/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)
