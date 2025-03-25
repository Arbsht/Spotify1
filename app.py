from flask import Flask, redirect, request, url_for, render_template,session
from flask_login import LoginManager
from blueprints.auth import auth_bp
from blueprints.home import *
from blueprints.cerca import *
from blueprints.random import *
from models import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'chiave_per_session' #ci serve per identificare la sessione
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#inizializza db e flask-login
db.init_app(app)
login_manager = LoginManager() #inizializza flask-login
login_manager.init_app(app) #collega flask-login e fla  sk
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(cerca_bp)
app.register_blueprint(random_bp)

if __name__ == '__main__': #debug
    app.run(debug=True)