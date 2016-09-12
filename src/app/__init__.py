from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "EERTZUNIPPYPLD"
from app import views
views.login_manager.init_app(app)

from app import bares
