from flask import Blueprint, Flask, redirect, request, url_for, render_template,session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

auth_bp = Blueprint('auth', __name__) #creiamo il blueprint@app.route('/')

#oggi leak di chiavi api
sp_oauth = SpotifyOAuth(
    client_id='0',
    client_secret='0',
    redirect_uri='http://127.0.0.1:5000/callback',
    scope="user-read-private", #permessi x informazioni dell'utente
    show_dialog=True
)

SPOTIFY_CLIENT_ID = "client_id"
SPOTIFY_CLIENT_SECRET = "client_secret"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:5000/callback" #dopo il login andiamo qui

@auth_bp.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url() #login di spotify
    return redirect(auth_url)

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code') #recupero codice di autorizzazione
    token_info = sp_oauth.get_access_token(code) #uso il code per un codice di accesso
    session['token_info'] = token_info #salvo il token nella mia sessione x riutilizzarlo
    return redirect(url_for('home'))

@auth_bp.route('/logout')
def logout():
    session.clear() #cancelliamo l'access token salvato in session
    return redirect(url_for('auth.login'))