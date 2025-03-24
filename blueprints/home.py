from flask import Blueprint, render_template, session, redirect, url_for
import spotipy
from services.spotify_oauth import *
from services.charts import get_top_artists  # Importiamo la funzione per i grafici
from services.charts import get_top_albums

home_bp = Blueprint('home', __name__)




@home_bp.route('/home') 

def home():
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        return redirect(url_for('home.homenl'))
    sp = spotipy.Spotify(auth=token_info['access_token']) #usiamo il token per ottenere i dati del profilo
    user_info = sp.current_user()
    playlists = sp.current_user_playlists(limit=50)
    playlists_info = playlists['items']
    print("Playlist:")
    print(playlists)
    print("USER:")
    print(user_info) #capiamo la struttura di user_info per usarle nel frontend
    return render_template('home.html', user_info=user_info, playlists=playlists_info) #passo le info utente all'home.html 

    @home_bp.route('/charts')
    def show_charts():
        token_info = session.get('token_info', None)
        if not token_info:
            return redirect(url_for('home.homenl'))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])  
    top_artists_chart = get_top_artists(sp)  # Recupera il grafico

    # Passa il grafico al template
    return render_template('charts.html', top_artists_chart=top_artists_chart)

@home_bp.route('/playlist/<id>')
def playlist(id):
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist = sp.playlist(playlist_id = id)
    tracks = sp.playlist_tracks(playlist_id=id)
    return render_template('playlist.html', playlist = playlist, tracks = tracks, id= id, top_artists_chart = get_top_artists(sp, id), top_albums_chart = get_top_albums(sp, id))

@home_bp.route('/homenl')
def homenl():
    return render_template('homenl.html')