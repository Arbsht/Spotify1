import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
#oggi leak di chiavi api
sp_oauth = SpotifyOAuth(
    client_id='c1e1e455737c44a5a404101c638179d8',
    client_secret='8f3955fa4f294df88e3bba9a64f74f8e',
    client_id='9f1ea3fb16f04a4fb1aaa3d4e87bc179',
    client_secret='ed3e093fc6ff4108a60ffd6a6cd521e2',
    redirect_uri='http://127.0.0.1:5000/callback',  

    scope="user-read-private user-read-email playlist-read-private", #permessi x informazioni dell'utente
    show_dialog=True
)

def get_spotify_object(token_info):
    return spotipy.Spotify(auth=token_info['access_token']) 

def get_credentials():
    return SpotifyClientCredentials(client_id='c1e1e455737c44a5a404101c638179d8',client_secret='8f3955fa4f294df88e3bba9a64f74f8e')
    return SpotifyClientCredentials(client_id='9f1ea3fb16f04a4fb1aaa3d4e87bc179',client_secret='ed3e093fc6ff4108a60ffd6a6cd521e2')