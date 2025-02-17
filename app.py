from flask import Flask, redirect, request, url_for, render_template,session
import spotipy
from blueprints.auth import *
from blueprints.home import *

app = Flask(__name__)
app.secret_key = 'chiave_per_session' #ci serve per identificare la sessione

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)

if __name__ == '__main__': #debug
    app.run(debug=True)