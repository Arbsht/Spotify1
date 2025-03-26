import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
#oggi leak di chiavi api
sp_oauth = SpotifyOAuth(
    client_id='c1e1e455737c44a5a404101c638179d8',
    client_secret='ffc8c6493d9c4984967c88c244ce49b6',
    redirect_uri='http://127.0.0.1:5000/callback',  

    scope="user-read-private user-read-email playlist-read-private", #permessi x informazioni dell'utente
    show_dialog=True
)

def get_spotify_object(token_info):
    return spotipy.Spotify(auth=token_info['access_token']) 

def get_credentials():
    return SpotifyClientCredentials(client_id='c1e1e455737c44a5a404101c638179d8',client_secret='ffc8c6493d9c4984967c88c244ce49b6')