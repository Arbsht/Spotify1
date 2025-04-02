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

def get_genre_chart(sp, playlist_id):
    genre_count = {}

    playlist_tracks = sp.playlist_tracks(playlist_id)
    for track in playlist_tracks['items']:
        if track['track']:  
            artist = track['track']['artists'][0]
            artist_info = sp.artist(artist['id'])
            genres = artist_info.get('genres', [])
            
            if genres:
                genre = genres[0]  # Prendi solo il primo genere
                genre_count[genre] = genre_count.get(genre, 0) + 1
    
    df = pd.DataFrame(genre_count.items(), columns=['Genre', 'Count']).sort_values(by='Count', ascending=False)

    fig = px.pie(df, names='Genre', values='Count', title='Distribuzione dei generi musicali', color_discrete_sequence=px.colors.sequential.Viridis)
    
    return fig.to_html(full_html=False)

def get_tracks_per_year_chart(sp, playlist_id):
    year_count = {}

    playlist_tracks = sp.playlist_tracks(playlist_id)
    for track in playlist_tracks['items']:
        if track['track'] and 'album' in track['track'] and 'release_date' in track['track']['album']:
            release_date = track['track']['album']['release_date']
            year = release_date.split('-')[0]  # Prendi solo l'anno
            if year.isdigit():
                year_count[year] = year_count.get(year, 0) + 1
    
    df = pd.DataFrame(year_count.items(), columns=['Year', 'Count']).sort_values(by='Year', ascending=True)
    
    fig = px.bar(df, x='Year', y='Count', title='Distribuzione temporale dei brani', color='Year')
    
    return fig.to_html(full_html=False)
