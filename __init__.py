#!/usr/bin/python3.5
from werkzeug.utils import secure_filename
from flask import Flask, render_template, json, flash, request, redirect, session, jsonify, url_for
# from flaskext.mysql import MySQL


import flask_wtf
import os
import uuid
from flask import render_template
from forms import LoginForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app = app
app.config.from_object(__name__)
app.SECRET_KEY = 'peaches'
UPLOAD_FOLDER = 'var/www/FlaskApp/FlaskApp/static/uploads'
ALLOWED_EXTENSIONS = set(['dbf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class ReusableForm(Form):
    name = TextField('Percent of value lost')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    form = ReusableForm(request.form)
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
       #if file.filename != "*.dbf":
       if "dbf" not in file.filename:
	   error = "Only .dbf files are supported."
	   return render_template('index.html', error=error)
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
	   #file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
           #file.save(['UPLOAD_FOLDER'], filename))
	   file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       return render_template('process.html', fname=filename)
    return render_template('index.html', error=error)



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login.html')

if __name__ == "__main__":
    app.secret_key = 'peaches'
    app.run()
