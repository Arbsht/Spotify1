import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
#oggi leak di chiavi api
sp_oauth = SpotifyOAuth(
    client_id='486292e9ce954bab9887cd9ffba68664',
    client_secret='9feaa821d3ff457ea40b6f68f03133a9',
    redirect_uri='http://127.0.0.1:5000/callback',  

    scope="user-read-private user-read-email playlist-read-private", #permessi x informazioni dell'utente
    show_dialog=True
)

def get_spotify_object(token_info):
    return spotipy.Spotify(auth=token_info['access_token']) 

def get_credentials():
    return SpotifyClientCredentials(client_id='486292e9ce954bab9887cd9ffba68664',client_secret='9feaa821d3ff457ea40b6f68f03133a9')