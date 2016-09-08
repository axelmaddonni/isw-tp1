from flask import render_template, request, redirect, url_for
from wtforms import Form, BooleanField, StringField
from app import app
from app.bares import Direccion, Bar, BuscadorDeBares, buscador
import math

class BuscarForm(Form):
    direccion_actual = StringField('Direccion')

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/raiz_de_dos')
def raiz():
    return str(math.sqrt(2.0))

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    form = BuscarForm(request.form)
    if request.method == 'POST' and form.validate():
        print('direccion_actual.data = ', form.direccion_actual.data)
        posicion_del_usuario = Direccion(form.direccion_actual.data)
        return render_template('resultados_busqueda.html',
                           bares=buscador.buscar(posicion_del_usuario),
                           dirusuario=posicion_del_usuario)

    return render_template('buscar.html', form=form)

