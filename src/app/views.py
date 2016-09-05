from app import app
import math

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/raiz_de_dos')
def raiz():
    return str(math.sqrt(2.0))

