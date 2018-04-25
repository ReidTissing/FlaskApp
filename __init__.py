from werkzeug.utils import secure_filename
from flask import Flask, render_template, json, flash, request, redirect, session, jsonify, url_for
from flaskext.mysql import MySQL


import flask_wtf
import os
import uuid

app = Flask(__name__)
app = app
app.config.from_object(__name__)
SECRET_KEY = 'peaches'
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['dbf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    error = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error = "No file selected."
        if file.filename != "*.dbf":
            error = "Only .dbf files are supported."
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('process.html')
    return render_template('index.html', error = error)

if __name__ == "__main__":
    app.secret_key = 'peaches'
    app.run(debug=True)