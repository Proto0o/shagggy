import os
import secrets
from PIL import Image,ImageGrab
from flask import render_template, url_for, flash, redirect, request,Response
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm,  LoginFor
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import cv2
import sys
import numpy as np


z=0
@app.route("/")
@app.route("/home")
def home():
    x=7
    return render_template('home.html')
@app.route("/#stop")
def stop1():
    stop()
    return redirect(url_for('home'))
def stop():
    global z
    z=10

@app.route("/register", methods=['GET', 'POST'])
def register():
    x=7
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = LoginFor()
    if form.validate_on_submit():
        return render_template('ind.html',form=form,z=form.email.data)
    else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('ind.html',form=form)




@app.route("/login", methods=['GET', 'POST'])
def login():
    x=7
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    x=7
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    x=7
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



def gen():
    i=1
    while i<10:
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+str(i)+b'\r\n')
        i+=1


def get_frame():
    i=1 
    while(True):
         # 1800x600 windowed mode
        if z==10:
            break
        printscreen =  np.array(ImageGrab.grab(bbox=(0,0,1250,700)))
        x=cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
        imgencode=cv2.imencode('.jpg',x)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1
        

    del(camera)



@app.route('/calc/<username>')
def calc(username):

    return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/wathc')
def wathc():
    global z
    z=0
    return  render_template('watch.html')