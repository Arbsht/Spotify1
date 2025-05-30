from flask import Blueprint, render_template, session, redirect, url_for, request
import spotipy
from services.spotify_oauth import *

cerca_bp = Blueprint('cerca', __name__)

@cerca_bp.route('/cerca', methods=['POST','GET'])
def cerca():
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
    query = request.form['cerca']
    risultato = sp.search(q = query, type='playlist', limit=20)
    return render_template('cerca.html', risultato = risultato, query = query)

@cerca_bp.route('/compare/<id>/cerca', methods=['POST','GET'])
def cercapercompare(id):
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
    query = request.form['cerca']
    risultato = sp.search(q = query, type='playlist', limit=20)
    playlist = sp.playlist(playlist_id=id)
    return render_template('cercacompare.html', risultato = risultato, query = query, playlist = playlist)