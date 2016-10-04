from functools import wraps
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import Form
from flask_bcrypt import Bcrypt
from wtforms import TextField, PasswordField, BooleanField, IntegerField, StringField, SelectField, validators
from app import app
from app.bares import Ubicacion, Bar, BuscadorDeBares, buscador, PerfilDeBar, gmaps
from app.user import User, usuarios
import math
import polyline as pline

import traceback

bcrypt = Bcrypt()
login_manager = LoginManager()

class BuscarForm(Form):
    choices_ = [
        ('default', ''),
        ('distancia', 'Distancia Maxima (m.)'),
        ('wifi', 'Puntaje Wifi Minimo'),
        ('enchufes', 'Puntaje Enchufes Minimo'),
        ('comida', 'Puntaje Comida Minimo'),
        ('servicio', 'Puntaje Servicio Minimo')
    ]
    mensaje_error = 'No es un numero entero, por favor intente de nuevo.'
    direccion_actual = StringField('Direccion', [validators.required()])

    filtro1 = SelectField('', choices=choices_, default='default')
    valor1 = IntegerField('',
            [validators.Regexp('\d', message=mensaje_error),
            validators.Optional()])

    filtro2 = SelectField('', choices=choices_, default='default')
    valor2 = IntegerField('',
            [validators.Regexp('\d', message=mensaje_error),
            validators.Optional()])

    filtro3 = SelectField('', choices=choices_, default='default')
    valor3 = IntegerField('',
            [validators.Regexp('\d', message=mensaje_error),
            validators.Optional()])

class AgregarForm(Form):
    direccion_dada = StringField('Direccion')
    nombre_dado = StringField("Nombre")

class EditarForm(Form):
    direccion_dada = StringField('Direccion')

class LoginForm(Form):
    username = TextField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

def homeRedirect(func):
    @wraps(func)
    def manejarError(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return redirect(url_for("accionesPosibles"))
    return manejarError

# Probar con "Fitz Roy 1477, CABA, Argentina"
@homeRedirect
@app.route("/buscar/<error>", methods=['GET', 'POST'])
@app.route('/buscar', methods=['GET', 'POST'])
def buscar(error = False):
    form = BuscarForm(request.form)
    if request.method == 'POST' and form.validate():
        print('direccion_actual.data = ', form.direccion_actual.data)
        posicion_del_usuario = Ubicacion(form.direccion_actual.data)
        try:
            baresEncontrados = buscador.buscar(posicion_del_usuario)
        except Exception as e:
            traceback.print_exc()
            return redirect(url_for("buscar") + "/True")
        user = user_loader(current_user.get_id())
        markers = []
        misBares = []
        for bar in baresEncontrados:
            marker = {}
            marker['lat'] = bar[1].bar().ubicacion().latlong()[0]
            marker['lng'] = bar[1].bar().ubicacion().latlong()[1]
            marker['infobox'] = bar[1].bar().nombre()
            markers.append(marker)
            if bar[1].bar().esDuenio(user):
                misBares.append(bar[1].ubicacion().direccion())
        marker_posicion_usuario = {}
        marker_posicion_usuario['lat'] = posicion_del_usuario.latlong()[0]
        marker_posicion_usuario['lng'] = posicion_del_usuario.latlong()[1]
        marker_posicion_usuario['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        marker_posicion_usuario['infobox'] = 'Tu Ubicacion'
        markers.append(marker_posicion_usuario)

        latlng_usuario = {'lat': posicion_del_usuario.latlong()[0],
                          'lng': posicion_del_usuario.latlong()[1]
                          }
        polylines = []
        colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFFFF",
                  "#000000", "#FFFF00", "#00FFFF", "#FF00FF"]
        for i in range(len(baresEncontrados)):
            bar = baresEncontrados[i]
            latlng_bar = {'lat': bar[1].bar().ubicacion().latlong()[0],
                          'lng': bar[1].bar().ubicacion().latlong()[1]
                          }

            legs = gmaps.directions(latlng_usuario, latlng_bar, mode='walking', units='metric')[0]['legs']

            #overview_polyline
            polyline = {'stroke_color': colors[i%len(colors)],
                        'stroke_opacity': 0.8,
                        'stroke_weight': 4,
                        'path': []}

            for i in range(len(legs)):
                steps = legs[i]['steps'];
                for j in range(len(steps)):
                    encodedPoints = steps[j]['polyline']['points']
                    for lat, lng in pline.decode(encodedPoints):
                        polyline['path'].append({'lat': lat, 'lng': lng})

            polylines.append(polyline)

        return render_template('resultados_busqueda.html',
                           bares=baresEncontrados,
                           dirusuario=posicion_del_usuario,
                           locations=markers,
                           polylines=polylines,
                           misBares = misBares,
                           mod = (user is not None) and user.is_mod()
                           )
    return render_template('buscar.html', form = form, error = error)


@app.route('/agregar', methods=['GET', 'POST'])
@homeRedirect
@login_required
def agregar():
    form = AgregarForm(request.form)
    if request.method == 'POST' and form.validate():
        nombre_del_bar = str(form.nombre_dado.data)
        direccion_del_bar = Ubicacion(form.direccion_dada.data)
        buscador.obtenerBBDD().agregarBares([PerfilDeBar(Bar(nombre_del_bar, direccion_del_bar))])
        return render_template('agregar_resultado.html',
                           positivo = True)

    return render_template('agregar.html', form=form)

@app.route('/editar', methods=['GET', 'POST'])
@homeRedirect
@login_required

def editar():
    direccion = request.args.get('barDireccion')

    form = EditarForm(request.form)
    if request.method == 'POST' and form.validate():
        bar = buscador.obtenerBBDD().obtenerBar(direccion)
        bar.editarUbicacion(Ubicacion(str(form.direccion_dada.data)))

        return render_template('editar_resultado.html',
                           positivo = True)
    return render_template('editar_bar.html', form=form, direccion=direccion)


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@homeRedirect
def accionesPosibles():
    if request.method == 'GET':
        user = user_loader(current_user.get_id())
        return render_template('home.html',
                            anon = (user is None) or user.is_anonymous(),
                            mod = (user is not None) and user.is_mod())

@login_manager.user_loader
def user_loader(user_id):
    return usuarios.get(user_id)

@app.route("/login/<invalidCredentials>", methods=['GET', 'POST'])
@app.route("/login", methods=["GET", "POST"])
@homeRedirect
def login(invalidCredentials = False):
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = user_loader(form.username.data)
        if user and user.check_password(form.password.data):
            user.authenticated = True
            login_user(user)
            return redirect(url_for("accionesPosibles"))
        else:
            return redirect(url_for("login") + "/True")
    return render_template("login.html", form=form, invalidCredentials = invalidCredentials)


@app.route("/logout", methods=["GET"])
@homeRedirect
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for("accionesPosibles"))
