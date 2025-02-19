from flask import Blueprint, render_template, session, redirect, url_for, request
import spotipy

cerca_bp = Blueprint('cerca', __name__)

@cerca_bp.route('/cerca', methods=['POST','GET'])
def cerca():
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        return redirect(url_for('auth.login'))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    query = request.form['cerca']
    risultato = sp.search(q = query, type='playlist')
    return render_template('cerca.html', risultato = risultato)