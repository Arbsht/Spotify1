import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
#oggi leak di chiavi api
sp_oauth = SpotifyOAuth(
    client_id='9f1ea3fb16f04a4fb1aaa3d4e87bc179',
    client_secret='ed3e093fc6ff4108a60ffd6a6cd521e2',
    redirect_uri='https://arbsht-spotify1-ko8ieryoys0.ws-eu118.gitpod.io/callback',  

    scope="user-read-private", #permessi x informazioni dell'utente
    show_dialog=True
)

SPOTIFY_CLIENT_ID = "client_id"
SPOTIFY_CLIENT_SECRET = "client_secret"
SPOTIFY_REDIRECT_URI = "https://arbsht-spotify1-ko8ieryoys0.ws-eu118.gitpod.io/callback" #dopo il login andiamo qui

def get_spotify_object(token_info):
    return spotipy.Spotify(auth=token_info['access_token']) 

def get_credentials():
    return SpotifyClientCredentials(client_id='c1e1e455737c44a5a404101c638179d8',client_secret='e4d8a63e280e4fe5aa5cb455555c6808')