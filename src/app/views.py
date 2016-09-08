from flask import render_template
from app import app
from app.bares import Direccion, Bar, BuscadorDeBares, buscador
import math


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/raiz_de_dos')
def raiz():
    return str(math.sqrt(2.0))

@app.route('/resultados/<posicion>')
def resultados_busqueda(posicion):
    global buscador
    posicion_del_usuario = Direccion(posicion)
    return render_template('resultados_busqueda.html',
                           bares=buscador.buscar(posicion_del_usuario),
                           dirusuario=posicion_del_usuario)

