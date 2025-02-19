import spotipy
from spotipy.oauth2 import SpotifyOAuth

#oggi leak di chiavi api
sp_oauth = SpotifyOAuth(
    client_id='486292e9ce954bab9887cd9ffba68664',
    client_secret='7a8214985e004e9d8928bd9ba0f4ff0a',
    redirect_uri='https://5000-arbsht-spotify1-c6seb8y5yf8.ws-eu117.gitpod.io/callback',
    scope="user-read-private", #permessi x informazioni dell'utente
    show_dialog=True
)

SPOTIFY_CLIENT_ID = "client_id"
SPOTIFY_CLIENT_SECRET = "client_secret"
SPOTIFY_REDIRECT_URI = "https://5000-arbsht-spotify1-c6seb8y5yf8.ws-eu117.gitpod.io/callback" #dopo il login andiamo qui

def get_spotify_object(token_info):
    return spotipy.Spotify(auth=token_info['access_token']) 