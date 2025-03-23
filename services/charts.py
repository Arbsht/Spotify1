import plotly.express as px
import pandas as pd

def get_top_artists(sp):
    playlists = sp.current_user_playlists()
    artist_count = {}

    for playlist in playlists['items']:
        playlist_tracks = sp.playlist_tracks(playlist['id'])
        for track in playlist_tracks['items']:
            if track['track']:  # Controllo che la traccia esista
                artist_name = track['track']['artists'][0]['name']
                artist_count[artist_name] = artist_count.get(artist_name, 0) + 1

    # Convertiamo in DataFrame e selezioniamo i primi 5 artisti
    df = pd.DataFrame(artist_count.items(), columns=['Artist', 'Count']).sort_values(by='Count', ascending=False).head(5)

    # Creiamo il grafico con Plotly
    fig = px.bar(df, x='Artist', y='Count', title='Top 5 Artisti più presenti', color='Artist')
    
    # Restituiamo il grafico come HTML
    return fig.to_html(full_html=False)

def get_top_albums(sp):
    playlists = sp.current_user_playlists()
    album_count = {}

    for playlist in playlists['items']:
        playlist_tracks = sp.playlist_tracks(playlist['id'])
        for track in playlist_tracks['items']:
            if track['track']:  # Controllo che la traccia esista
                album_name = track['track']['album']['name']
                album_count[album_name] = album_count.get(album_name, 0) + 1

    # Convertiamo in DataFrame e selezioniamo i primi 5 album
    df = pd.DataFrame(album_count.items(), columns=['Album', 'Count']).sort_values(by='Count', ascending=False).head(5)

    # Creiamo il grafico con Plotly
    fig = px.bar(df, x='Album', y='Count', title='Top 5 Album più presenti', color='Album')
    
    # Restituiamo il grafico come HTML
    return fig.to_html(full_html=False)