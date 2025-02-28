from flask import Blueprint, render_template, session, redirect, url_for
import spotipy
from services.spotify_oauth import *
import random as rand

random_bp = Blueprint('random', __name__)

@random_bp.route('/playlist/<id>/random')
def random(id):
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
    tracks = sp.playlist_tracks(playlist_id=id)
    track = tracks['items'][rand.randint(0, len(tracks['items']))]
    print(track['track'])
    return render_template('playlistrnd.html', track = track, id = id)