from werkzeug.utils import secure_filename
from flask import Flask, render_template, json, flash, request, redirect, session, jsonify, url_for
from flaskext.mysql import MySQL
import flask_wtf
import os
import uuid

app = Flask(__name__)
app = app
SECRET_KEY = 'development'
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/')
def index():
    return render_template('index.html')
	
	
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        app.config['UPLOAD_FOLDER'] = 'static/Uploads'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        print(f_name)
        print('extension: ' + extension + " f_name: " + f_name)
        return json.dumps({'filename': f_name})

if __name__ == "__main__":
    app.run()