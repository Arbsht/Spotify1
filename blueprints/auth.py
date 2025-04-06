from flask import Blueprint, Flask, redirect, request, url_for, render_template,session
from flask_login import login_required, login_user, logout_user, current_user
from models import *
from services.spotify_oauth import *
import os
import flask_bcrypt

auth_bp = Blueprint('auth', __name__) #creiamo il blueprint@app.route('/')

@auth_bp.route('/')
def blank():
    return redirect(url_for('home.homenl'))

@auth_bp.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url() #login di spotify
    return redirect(auth_url)

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code') #recupero codice di autorizzazione
    token_info = sp_oauth.get_access_token(code) #uso il code per un codice di accesso
    session['token_info'] = token_info #salvo il token nella mia sessione x riutilizzarlo
    return redirect(url_for('home.home'))

@auth_bp.route('/logout')
def logout():
    try:
        os.remove(".cache")
    except:
        print(".cache non esiste")
    logout_user() #logout user
    session.clear() #cancelliamo l'access token salvato in session
    
    return redirect(url_for('auth.blank'))

@auth_bp.route('/loginlocale', methods=['GET', 'POST'])
def loginlocale():
    if request.method == 'POST':
        username = request.form['username'] #prende dati dalle form
        password = request.form['password']
        #cerca user db
        user = User.query.filter_by(username=username).first()
        if user and flask_bcrypt.check_password_hash(user.password, password): #se user esiste
            login_user(user)
            return redirect(url_for('home.home'))
        return render_template('login.html', error="Credenziali non valide.") #errore se credenziali errate
    return render_template('login.html', error=None)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'] #prende dati dalle form
        password = request.form['password']
        #check se l'utente esiste nel db
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Questo username è già in uso.")
        if len(username) < 3 and len(password) < 7:
            return render_template('register.html', error="Lo username e la password usati sono troppo corti (min 4 per username, min 8 per password)")
        if len(username) < 3:
            return render_template('register.html', error="Lo username usato è troppo corto (minimo 4 caratteri)")
        if len(password) < 7:
            return render_template('register.html', error="La password usata è troppo corta (minimo 8 caratteri)")
        #crea user e lo salva nel db
        pw_hash = flask_bcrypt.generate_password_hash(password)
        new_user = User(username=username, password=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.loginlocale'))
    return render_template('register.html', error=None)

@auth_bp.route('/annullalogin')
def annullalogin():
    try:
        os.remove(".cache")
    except:
        print(".cache non esiste")
    session.clear() #cancelliamo l'access token salvato in session
    return redirect(url_for('home.homenl'))