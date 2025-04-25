from flask import Blueprint, render_template, session
import spotipy
from services.spotify_oauth import *
from models import *
import pandas as pd
import plotly.express as px
from flask_login import current_user
from collections import Counter

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
    token_info = session.get('token_info', None)

    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
        return redirect('/')
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        playlist1 = sp.playlist(playlist_id=id1)
        playlist2 = sp.playlist(playlist_id=id2)

    tracks1 = [track['track'] for track in playlist1['tracks']['items'] if track['track']]
    tracks2 = [track['track'] for track in playlist2['tracks']['items'] if track['track']]

    # Brani in comune
    tracks1_names = set(track['name'] for track in tracks1)
    tracks2_names = set(track['name'] for track in tracks2)
    common_tracks = tracks1_names.intersection(tracks2_names)
    similarity_percentage = (len(common_tracks) / min(len(tracks1), len(tracks2))) * 100 if min(len(tracks1), len(tracks2)) > 0 else 0

    fig_common_tracks = px.bar(
        x=["Playlist 1", "Playlist 2", "Comuni"],
        y=[len(tracks1), len(tracks2), len(common_tracks)],
        labels={"x": "Playlist", "y": "Numero Brani"},
        title=f"Brani in Comune (Somiglianza: {similarity_percentage:.1f}%)"
    )

    # Artisti in comune
    artists1 = [artist['name'] for track in tracks1 for artist in track['artists']]
    artists2 = [artist['name'] for track in tracks2 for artist in track['artists']]
    common_artists = set(artists1).intersection(set(artists2))

    artists1_counter = Counter(artists1)
    artists2_counter = Counter(artists2)

    common_artists_freq = []
    for artist in common_artists:
        common_artists_freq.append({
            'artist': artist,
            'freq1': artists1_counter[artist],
            'freq2': artists2_counter[artist]
        })

    df_common_artists = pd.DataFrame(common_artists_freq)

    fig_common_artists = px.bar(
        df_common_artists,
        x="artist",
        y=["freq1", "freq2"],
        barmode="group",
        labels={"value": "Frequenza", "artist": "Artista", "variable": "Playlist"},
        title="Frequenza Artisti in Comune"
    )

    # Popolarità media
    popularity1 = [track['popularity'] for track in tracks1 if track['popularity'] is not None]
    popularity2 = [track['popularity'] for track in tracks2 if track['popularity'] is not None]
    average_popularity1 = sum(popularity1) / len(popularity1) if popularity1 else 0
    average_popularity2 = sum(popularity2) / len(popularity2) if popularity2 else 0

    fig_popularity = px.bar(
        x=['Playlist 1', 'Playlist 2'],
        y=[average_popularity1, average_popularity2],
        labels={'x': 'Playlist', 'y': 'Popolarità Media'},
        title="Confronto Popolarità Media"
    )

    # Generi musicali
    def get_artist_genres(artist_id):
        try:
            return sp.artist(artist_id)['genres']
        except:
            return []

    genres1 = []
    for track in tracks1:
        artist_id = track['artists'][0]['id']
        genres1 += get_artist_genres(artist_id)

    genres2 = []
    for track in tracks2:
        artist_id = track['artists'][0]['id']
        genres2 += get_artist_genres(artist_id)

    genres1_counter = Counter(genres1)
    genres2_counter = Counter(genres2)

    all_genres = list(set(genres1_counter.keys()).union(genres2_counter.keys()))
    genre_freqs = [{
        "genre": genre,
        "Playlist 1": genres1_counter.get(genre, 0),
        "Playlist 2": genres2_counter.get(genre, 0)
    } for genre in all_genres]

    df_genres = pd.DataFrame(genre_freqs)

    fig_genres = px.bar(
        df_genres,
        x="genre",
        y=["Playlist 1", "Playlist 2"],
        barmode="group",
        labels={"value": "Frequenza", "genre": "Genere"},
        title="Confronto Generi Musicali"
    )

    # Distribuzione temporale dei brani
    release_dates1 = [track['album']['release_date'] for track in tracks1 if 'release_date' in track['album']]
    release_dates2 = [track['album']['release_date'] for track in tracks2 if 'release_date' in track['album']]

    years1 = [date.split('-')[0] for date in release_dates1]
    years2 = [date.split('-')[0] for date in release_dates2]

    year_counts1 = pd.Series(years1).value_counts().sort_index()
    year_counts2 = pd.Series(years2).value_counts().sort_index()

    df_years1 = pd.DataFrame({"anno": year_counts1.index, "Playlist 1": year_counts1.values})
    df_years2 = pd.DataFrame({"anno": year_counts2.index, "Playlist 2": year_counts2.values})

    df_years = pd.merge(df_years1, df_years2, on="anno", how="outer").fillna(0).sort_values("anno")

    fig_years = px.bar(
        df_years,
        x="anno",
        y=["Playlist 1", "Playlist 2"],
        barmode="group",
        labels={"value": "Numero Brani", "anno": "Anno"},
        title="Distribuzione Temporale dei Brani"
    )

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
                           common_tracks_chart=fig_common_tracks.to_html(full_html=False),
                           common_artists_chart=fig_common_artists.to_html(full_html=False),
                           popularity_chart=fig_popularity.to_html(full_html=False),
                           genres_chart=fig_genres.to_html(full_html=False),
                           time_distribution_chart=fig_years.to_html(full_html=False))
