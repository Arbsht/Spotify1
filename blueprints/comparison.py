from flask import Blueprint, render_template, session, redirect, url_for
import spotipy
from services.spotify_oauth import *
from services.charts import *
from flask_login import current_user
from models import *
import pandas as pd
import plotly.express as px

compare_bp = Blueprint('compare', __name__)

@compare_bp.route('/compare/<id>')
def compare(id):
    if current_user.is_authenticated:
        salvati = ListaPlaylist.query.filter_by(utente=current_user.username).all()
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
    
    return render_template('compare.html', 
                           user_info=user_info, 
                           playlists=playlists_info, 
                           username=current_user.username, 
                           salvati=salvati, 
                           playlist=playlist)

@compare_bp.route('/comparison/<id1>/<id2>')
def comparison(id1, id2):
    # Ottieni le informazioni per playlist1 e playlist2
    token_info = session.get('token_info', None)
    
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
        playlist1 = {}
        playlist2 = {}
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        # Recupera le informazioni per la playlist 1
        playlist1 = sp.playlist(playlist_id=id1)
        
        # Recupera le informazioni per la playlist 2
        playlist2 = sp.playlist(playlist_id=id2)
    
    # Recupera le tracce delle playlist
    tracks1 = [track['track'] for track in playlist1['tracks']['items']]
    tracks2 = [track['track'] for track in playlist2['tracks']['items']]
    
    # Trova i brani in comune
    tracks1_names = set(track['name'] for track in tracks1)
    tracks2_names = set(track['name'] for track in tracks2)
    common_tracks = tracks1_names.intersection(tracks2_names)
    similarity_percentage = (len(common_tracks) / min(len(tracks1), len(tracks2))) * 100
    
    # Trova gli artisti in comune
    artists1 = [artist['name'] for track in tracks1 for artist in track['artists']]
    artists2 = [artist['name'] for track in tracks2 for artist in track['artists']]
    common_artists = set(artists1).intersection(set(artists2))
    
    # Trova i generi comuni
    genres1 = []
    for track in tracks1:
        try:
            genres = track['artists'][0].get('genres', [])
            genres1.extend(genres)
        except KeyError:
            continue

    genres2 = []
    for track in tracks2:
        try:
            genres = track['artists'][0].get('genres', [])
            genres2.extend(genres)
        except KeyError:
            continue

    common_genres = set(genres1).intersection(set(genres2))
    
    # Confronto popolarità media
    popularity1 = [track['popularity'] for track in tracks1]
    popularity2 = [track['popularity'] for track in tracks2]
    average_popularity1 = sum(popularity1) / len(popularity1) if popularity1 else 0
    average_popularity2 = sum(popularity2) / len(popularity2) if popularity2 else 0
    
    # Distribuzione temporale dei brani
    release_dates1 = [track['album']['release_date'] for track in tracks1]
    release_dates2 = [track['album']['release_date'] for track in tracks2]
    
    years1 = [date.split('-')[0] for date in release_dates1]
    years2 = [date.split('-')[0] for date in release_dates2]
    
    # Genera grafico per la distribuzione temporale dei brani
    year_counts1 = pd.Series(years1).value_counts().sort_index()
    year_counts2 = pd.Series(years2).value_counts().sort_index()

    # Crea grafici con Plotly
    fig1 = px.bar(x=list(year_counts1.index), y=list(year_counts1.values), labels={'x': 'Anno', 'y': 'Numero di Brani'}, title="Distribuzione Temporale Playlist 1")
    fig2 = px.bar(x=list(year_counts2.index), y=list(year_counts2.values), labels={'x': 'Anno', 'y': 'Numero di Brani'}, title="Distribuzione Temporale Playlist 2")
    
    # Grafici di popolarità e similitudini
    fig3 = px.bar(x=['Playlist 1', 'Playlist 2'], y=[average_popularity1, average_popularity2], labels={'x': 'Playlist', 'y': 'Popolarità Media'}, title="Confronto Popolarità Media")
    fig4 = px.pie(names=['Playlist 1', 'Playlist 2', 'Generi Comuni'], values=[len(genres1), len(genres2), len(common_genres)], title="Confronto Generi Musicali")

    # Passa le informazioni al template
    return render_template('comparison.html', 
                           id1=id1, 
                           id2=id2, 
                           playlist1=playlist1, 
                           playlist2=playlist2,
                           common_tracks=common_tracks,
                           similarity_percentage=similarity_percentage,
                           common_artists=common_artists,
                           average_popularity1=average_popularity1,
                           average_popularity2=average_popularity2,
                           fig1=fig1.to_html(full_html=False),
                           fig2=fig2.to_html(full_html=False),
                           fig3=fig3.to_html(full_html=False),
                           fig4=fig4.to_html(full_html=False))
