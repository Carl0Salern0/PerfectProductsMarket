from flask import Flask, render_template

# Importazione gestore DB e funzionalità crittografiche
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Importazione del login manager
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')

# Inizializzazione Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///negozio.db'
app.config['SECRET_KEY'] = '5c64655ed46ec9b8bd814c76'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Inizializzazione del login manager
login_manager = LoginManager(app)

# Requisito login per accedere a pagine protette
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from main import routes