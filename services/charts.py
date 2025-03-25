import plotly.express as px
import pandas as pd

def get_top_artists(sp, playlist_id):
    artist_count = {}

    playlist_tracks = sp.playlist_tracks(playlist_id)
    for track in playlist_tracks['items']:
        if track['track']:  
            artist_name = track['track']['artists'][0]['name']
            artist_count[artist_name] = artist_count.get(artist_name, 0) + 1

    df = pd.DataFrame(artist_count.items(), columns=['Artist', 'Count']).sort_values(by='Count', ascending=False).head(5)

    fig = px.bar(df, x='Artist', y='Count', title='Top 5 Artisti più presenti', color='Artist')
    
    return fig.to_html(full_html=False)

def get_top_albums(sp, playlist_id):
    album_count = {}

    playlist_tracks = sp.playlist_tracks(playlist_id)
    for track in playlist_tracks['items']:
        if track['track']:  
            album_name = track['track']['album']['name']
            album_count[album_name] = album_count.get(album_name, 0) + 1

    df = pd.DataFrame(album_count.items(), columns=['Album', 'Count']).sort_values(by='Count', ascending=False).head(5)

    fig = px.bar(df, x='Album', y='Count', title='Top 5 Album più presenti', color='Album')
    
    return fig.to_html(full_html=False)