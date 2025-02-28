import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
#oggi leak di chiavi api
sp_oauth = SpotifyOAuth(
    client_id='486292e9ce954bab9887cd9ffba68664',
    client_secret='6a427e3e440042a597cc1fc8e8e3e1fd',
    redirect_uri='http://127.0.0.1:5000/callback',
    scope="user-read-private", #permessi x informazioni dell'utente
    show_dialog=True
)

SPOTIFY_CLIENT_ID = "client_id"
SPOTIFY_CLIENT_SECRET = "client_secret"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:5000/callback" #dopo il login andiamo qui

def get_spotify_object(token_info):
    return spotipy.Spotify(auth=token_info['access_token']) 

def get_credentials():
    return SpotifyClientCredentials(client_id='486292e9ce954bab9887cd9ffba68664',client_secret='6a427e3e440042a597cc1fc8e8e3e1fd')