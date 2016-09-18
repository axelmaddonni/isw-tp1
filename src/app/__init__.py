from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "EERTZUNIPPYPLD"
from app import views
views.login_manager.init_app(app)

from app import bares

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
# # Initialize the extension
GoogleMaps(app, key="AIzaSyCtcQ5Hb2wI4ubJjNSjz_mm_57MRU7IGS8")