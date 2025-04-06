from flask import Blueprint, render_template, session, redirect, url_for
import spotipy
from services.spotify_oauth import *
from services.charts import *
from flask_login import current_user
from models import *

home_bp = Blueprint('home', __name__)




@home_bp.route('/home') 

def home():
    if current_user.is_authenticated == False:
        return(redirect(url_for('home.homenl')))
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    salvati = ListaPlaylist.query.filter_by(utente = current_user.username).all()
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
        spotifynolog = True
        user_info = {}
        playlists = {}
        playlists_info = {}
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        spotifynolog = False
        user_info = sp.current_user()
        playlists = sp.current_user_playlists(limit=50)
        playlists_info = playlists['items']
    return render_template('home.html', user_info=user_info, playlists=playlists_info, username = current_user.username, salvati = salvati, spotifynolog = spotifynolog) #passo le info utente all'home.html 

@home_bp.route('/playlist/<id>')
def playlist(id):
    if current_user.is_authenticated:
        hologgato = True
    else:
        hologgato = False
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
    try:
        playlist = sp.playlist(playlist_id = id)
    except:
        return(redirect(url_for('home.home')))
    tracks = sp.playlist_tracks(playlist_id=id)
    return render_template('playlist.html', playlist = playlist, tracks = tracks, id= id, top_artists_chart = get_top_artists(tracks), top_albums_chart = get_top_albums(tracks), 
    top_genres_chart = get_genre_chart(sp, tracks), tracks_per_year_chart = get_tracks_per_year_chart(tracks), tracks_duration = get_tracks_duration(tracks), hologgato = hologgato,
    tracks_popularity = get_tracks_popularity(tracks))
    #except:
     #   return(redirect(url_for('home.home')))

@home_bp.route('/homenl')
def homenl():
    if current_user.is_authenticated:
        return(redirect(url_for('home.home')))
    return render_template('homenl.html')

@home_bp.route('/playlist/<id>/aggiungi')
def aggiungi(id):
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist = sp.playlist(playlist_id=id)
    nome = playlist['name']
    nuovoelemento = ListaPlaylist(utente = current_user.username, nome = nome, elemento = id)
    db.session.add(nuovoelemento)
    db.session.commit()
    return redirect(url_for('home.home'))

@home_bp.route('/rimuovi/<id>')
def rimuovi(id):
    elemento = ListaPlaylist.query.get_or_404(id)
    db.session.delete(elemento)
    db.session.commit()
    return redirect(url_for('home.home'))