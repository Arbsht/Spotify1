from flask import Blueprint, render_template, session, redirect, url_for
import spotipy
from services.spotify_oauth import *
from services.charts import *
from flask_login import current_user
from models import *

compare_bp = Blueprint('compare', __name__)

@compare_bp.route('/comparison/<id1>/<id2>')
def comparison(id1, id2):
    token_info = session.get('token_info', None)
    
    if not token_info:
        sp = spotipy.Spotify(client_credentials_manager=get_credentials())
    else:
        sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Recupera i dettagli delle due playlist
    playlist1 = sp.playlist(id1)
    playlist2 = sp.playlist(id2)
    
    # Estrai i nomi delle tracce da entrambe le playlist
    tracks1 = [track['track']['name'] for track in playlist1['tracks']['items']]
    tracks2 = [track['track']['name'] for track in playlist2['tracks']['items']]
    
    # Trova le tracce comuni
    common_tracks = set(tracks1).intersection(tracks2)
    
    # Passa le playlist e le tracce comuni al template
    return render_template(
        'comparison.html', 
        id1=id1, 
        id2=id2, 
        playlist1=playlist1, 
        playlist2=playlist2,
        common_tracks=common_tracks
    )
