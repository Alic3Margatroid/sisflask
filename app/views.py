from flask import render_template, flash, redirect, session, url_for, request, g, send_file
import flask
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from .forms import LoginForm, RegisterForm, EditForm, MessageForm, PhotoForm
from .models import User, Messages
from werkzeug import generate_password_hash, check_password_hash, secure_filename
import models
import os, re, hashlib


ALLOWED_EXTENSIONS = set(['txt'])
UPLOAD_FOLDER = os.path.join(app.instance_path,"ex")
CHALLENGE_FOLDER = os.path.join(app.instance_path,"ch")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.before_request
def before_request():
  g.user = current_user

@app.route('/')
@app.route('/index')
def index():
    user = g.user
    return render_template('index.html',
                           title='Home',
                           user = user
                           )

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
      user = User.query.get(form.username.data)
      if user:
        if check_password_hash(user.password, form.password.data):
          user.authenticated = True
          db.session.add(user)
          db.session.commit()
          login_user(user,remember=True)
          next = flask.request.args.get('next')
          return flask.redirect(next or flask.url_for('index'))
        else:
          flask.flash("Invalid combination of username-password")
          return flask.redirect(url_for('login'))
      else:
        flask.flash("Invalid username")
        return flask.redirect(url_for('login'))
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           )

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
  if g.user is not None and g.user.is_authenticated:
        flask.flash("Logout before register!")
        return redirect(url_for('index'))
  form = RegisterForm()
  if form.validate_on_submit():
    u = models.User(username = form.username.data, password = generate_password_hash(form.password.data), email = form.email.data, name = form.name.data, phoneno = form.phoneno.data)  
    next = flask.request.args.get('next')
    try:
      db.session.add(u)
      db.session.commit()
    except:
      print "Username or email existed"
      return flask.redirect(next or flask.url_for('index')) 
    flask.flash('Register Successfully') 
    return flask.redirect(next or flask.url_for('index'))
  return render_template('register.html',form=form)

@app.route('/user/<username>', methods = ['GET','POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    token = False
    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    messages = Messages.query.filter_by(username=username)
    form = MessageForm()
    if form.validate_on_submit():
      m = models.Messages(username = user.username, author=current_user.username, content = form.content.data)
      db.session.add(m)
      db.session.commit()
    if request.method == "POST" and request.values.get("delete"):
      delete = models.Messages.query.filter_by(id=request.form['id_message']).first()
      db.session.delete(delete)
      db.session.commit()
    if request.method == "POST" and request.values.get("edit"):
      token = True
    if request.method == "POST" and request.values.get("repost"):
      m = models.Messages.query.filter_by(id=request.form['id_message']).first()
      m.content = form.content.data
      db.session.commit()
      token = False
    return render_template('user.html',
                           user=user,
                           messages=messages,
                           form=form,
                           token=token)

@app.route('/edit', methods = ['GET','POST'])
@login_required
def edit():
  admin = False
  form = EditForm()
  if current_user.username == "admin":
    admin = True
  if form.validate_on_submit():
    g.user.password = generate_password_hash(form.password.data)
    g.user.email = form.email.data
    g.user.phoneno = form.phoneno.data
    if current_user.username == 'admin':
      g.user.username = form.username.data
      g.user.name = form.name.data
    db.session.add(g.user)
    db.session.commit()
    flash('Your changes have been saved.')
    
  return render_template('edit.html', form=form, admin=admin)

@app.route('/list')
def list():
  users = models.User.query.all()
  return render_template('list.html', users=users)

@app.route('/exercises',methods = ['GET','POST'])
@login_required
def upload():
  admin = False
  if current_user.username == "admin":
    admin = True
  fs = os.listdir(UPLOAD_FOLDER)
  files = []
  for f in fs:
    if re.search(".txt$",f):
      files.append(f)
  return render_template('exercises.html',files=files, title="Exercises",admin=admin)

@app.route('/getfile/<filename>', methods=["GET","POST"])
@login_required
def getfile(filename):
  return send_file('%s/%s' %(UPLOAD_FOLDER,filename,),
                  attachment_filename=filename,
                  as_attachment=True)

@app.route('/upfile/<fname>', methods=["GET","POST"])
@login_required
def upfile(fname):
  admin = False
  if current_user.username == "admin":
    admin = True
  upfolder = os.path.join(UPLOAD_FOLDER,fname[:len(fname)-4])
  file = request.files['file']
  if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(upfolder, filename))
      flask.flash("Upload Successfully!")
  fs = os.listdir(UPLOAD_FOLDER)
  files = []
  for f in fs:
    if re.search(".txt$",f):
      files.append(f)
  return render_template('exercises.html',files=files, title="Exercises", admin=admin)

@app.route('/upexercise', methods=["GET","POST"])
@login_required
def upexercise():
  upfolder = UPLOAD_FOLDER
  file = request.files['fileex']
  if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(upfolder, filename))
      flask.flash("Upload Successfully!")
  newfolder = os.path.join(UPLOAD_FOLDER,filename[:len(filename)-4])
  if not os.path.exists(newfolder):
    os.makedirs(newfolder)
  fs = os.listdir(UPLOAD_FOLDER)
  files = []
  for f in fs:
    if re.search(".txt$",f):
      files.append(f)
  return render_template('exercises.html',files=files, title="Exercises", admin=True)

@app.route('/uploadlist')
@login_required
def uploadlist():
  if current_user.username == 'admin':
    for dirname, dirnames, filenames in os.walk(UPLOAD_FOLDER):
      for subdirname in dirnames:
        flask.flash(os.path.join(dirname, subdirname))
    for filename in filenames:
        flask.flash(os.path.join(dirname, filename))
  return render_template('uploadlist.html',title="Upload list")

@app.route('/challenge', methods=["GET","POST"])
@login_required
def challenge():
  admin = False
  if current_user.username == "admin":
    admin = True  
    if request.method == "POST" and request.values.get("upchallenge"):  
      file = request.files['file']
      description = request.values.get('description')
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        newfolder = os.path.join(CHALLENGE_FOLDER,hashlib.md5(filename[:len(filename)-4]+description).hexdigest())
        if not os.path.exists(newfolder):
          os.makedirs(newfolder)
        file.save(os.path.join(newfolder, filename))
        desfile = os.path.join(newfolder,"description")
        f = open(desfile,"w+")
        f.write(description)
        f.close()
        flask.flash("Upload Successfully!")
  Description = []
  fs = os.listdir(CHALLENGE_FOLDER)
  for fd in fs:
    buf = ""
    desfile = os.path.join(CHALLENGE_FOLDER,fd)
    desfile = os.path.join(desfile,"description")
    f = open(desfile,"r")
    for line in f:
      buf += line
    Description.append(buf)
    f.close()
  if request.method == "POST" and request.values.get("Answer"):
    answer = hashlib.md5(request.values.get("answer")+request.values.get("desc")).hexdigest()
    if answer in fs:
      flask.flash("You get it right!")
      ans = os.path.join(CHALLENGE_FOLDER,answer)
      ans = os.path.join(ans,request.values.get("answer")+".txt")
      f = open(ans,"r")
      for line in f:
        flask.flash(line)
      f.close()
    else:
      flask.flash("Try again!")
  return render_template("challenge.html",admin=admin, title="Challenge", description = Description)
