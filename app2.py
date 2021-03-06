from werkzeug.utils import secure_filename
from flask import Flask, render_template, json, flash, request, redirect, session, jsonify, url_for
# from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy

import flask_wtf
import os
import uuid
from flask import render_template
from forms import LoginForm

app = Flask(__name__)
app = app
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
app.SECRET_KEY = 'peaches'
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['dbf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class User(db.Model):
	"""create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db..String(80))
	
	def __init__(self, username, password):
		self.username = username
		self.password = password

# begin routing. '/' goes to login first, checks case-insensitive logins
@app.route('/', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        nameinput = request.form.get('username')
        pwinput = request.form.get('password')
        if nameinput.lower() == 'aberdeen' and pwinput.lower() == 'aberdeen':
            return redirect(url_for('index'))
        if nameinput.lower() == 'public' and pwinput.lower() == 'public':
            return redirect(url_for('index'))
        else:
            flash('The login information you provided is invalid!')
            return redirect('/')

    return render_template('login.html', title='Sign In', form=form)


@app.route('/index', methods=['GET', 'POST'])
def index():
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
    return render_template('index.html', error=error)



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login.html')

if __name__ == "__main__":
    app.secret_key = 'peaches'
    app.run()
