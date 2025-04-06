from flask import Blueprint, render_template, session, redirect, url_for
import spotipy
from services.spotify_oauth import *
from services.charts import *
from flask_login import current_user
from models import *

compare_bp = Blueprint('compare', __name__)

@compare_bp.route('/compare/<id>')
def compare(id):
    if current_user.is_authenticated == True:
        salvati = ListaPlaylist.query.filter_by(utente = current_user.username).all()
    else:
        salvati = {}
    token_info = session.get('token_info', None)
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
        user_info = {}
        playlists = {}
        playlists_info = {}
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_info = sp.current_user()
        playlists = sp.current_user_playlists(limit=50)
        playlists_info = playlists['items']
    playlist = sp.playlist(playlist_id=id)
    return render_template('compare.html', user_info=user_info, playlists=playlists_info, username = current_user.username, salvati = salvati, playlist = playlist)

@compare_bp.route('/comparison/<id1>/<id2>')
def comparison(id1, id2):
    return render_template('comparison.html', id1 = id1, id2 = id2)