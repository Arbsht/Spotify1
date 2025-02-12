from flask import Flask, redirect, request, url_for, render_template,session
import spotipy
from blueprints.auth import *

app = Flask(__name__)
app.secret_key = 'chiave_per_session' #ci serve per identificare la sessione

app.register_blueprint(auth_bp)

@app.route('/home') 
def home():
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        return redirect(url_for('login'))
    sp = spotipy.Spotify(auth=token_info['access_token']) #usiamo il token per ottenere i dati del profilo
    user_info = sp.current_user()
    playlists = sp.current_user_playlists(limit=50)
    playlists_info = playlists['items']
    print("Playlist:")
    print(playlists)
    print("USER:")
    print(user_info) #capiamo la struttura di user_info per usarle nel frontend
    return render_template('home.html', user_info=user_info, playlists=playlists_info) #passo le info utente all'home.html 

@app.route('/playlist/<id>')
def playlist(id):
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        return redirect(url_for('login'))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist = sp.playlist(playlist_id = id)
    tracks = sp.playlist_tracks(playlist_id=id)
    return render_template('playlist.html', playlist = playlist, tracks = tracks)



if __name__ == '__main__': #debug
    app.run(debug=True)