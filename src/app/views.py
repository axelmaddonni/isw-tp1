from functools import wraps
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import Form
from flask_bcrypt import Bcrypt
from wtforms import TextField, PasswordField, BooleanField, IntegerField, StringField, SelectField, validators, ValidationError
from app import app
from app.bares import Ubicacion, Bar, BuscadorDeBares, buscador, PerfilDeBar, gmaps
from app.filtros import *
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
    valor1 = IntegerField('', [validators.Optional()])

    filtro2 = SelectField('', choices=choices_, default='default')
    valor2 = IntegerField('', [validators.Optional()])

    filtro3 = SelectField('', choices=choices_, default='default')
    valor3 = IntegerField('', [validators.Optional()])

    def validate_valor1(form, field):
        if form.filtro1.data == '':
            return
        if form.filtro1.data == 'distancia':
            if field.data <= 0:
                raise ValidationError('La distancia debe ser positiva.')
        else:
            if not (0 <= field.data <= 100):
                raise ValidationError('El puntaje va entre 0 y 100.')

    def validate_valor2(form, field):
        if form.filtro2.data == '':
            return
        if form.filtro2.data == 'distancia':
            if field.data <= 0:
                raise ValidationError('La distancia debe ser positiva.')
        else:
            if not (0 <= field.data <= 100):
                raise ValidationError('El puntaje va entre 0 y 100.')

    def validate_valor3(form, field):
        if form.filtro3.data == '':
            return
        if form.filtro3.data == 'distancia':
            if field.data <= 0:
                raise ValidationError('La distancia debe ser positiva.')
        else:
            if not (0 <= field.data <= 100):
                raise ValidationError('El puntaje va entre 0 y 100.')


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
        except:
            traceback.print_exc()
            return redirect(url_for("accionesPosibles"))
    return manejarError

# No se puede eliminar el if porque viene del html esto
def llenar_filtro(filtron, valorn, filtro, d_cache):
    if filtron == 'distancia':
        return FiltroDeDistancia(filtro, valorn, d_cache)
    elif filtron == 'wifi':
        return FiltroDeWifi(filtro, valorn)
    elif filtron == 'enchufes':
        return FiltroDeEnchufes(filtro, valorn)
    elif filtron == 'comida':
        return FiltroDeComida(filtro, valorn)
    elif filtron == 'servicio':
        return FiltroDeServicio(filtro, valorn)
    else:
        return filtro


# Probar con "Fitz Roy 1477, CABA, Argentina"
@app.route("/buscar/<error>", methods=['GET', 'POST'])
@app.route('/buscar', methods=['GET', 'POST'])
@homeRedirect
def buscar(error = False):
    form = BuscarForm(request.form)
    if request.method == 'POST' and form.validate():
        print('direccion_actual.data = ', form.direccion_actual.data)
        try:
            posicion_del_usuario = Ubicacion(form.direccion_actual.data)
            distancias_cache = buscador.distancias_cache(posicion_del_usuario)
            filtro = FiltroVacio()
            filtro = llenar_filtro(form.filtro1.data, form.valor1.data, filtro,
                    distancias_cache)
            filtro = llenar_filtro(form.filtro2.data, form.valor2.data, filtro,
                    distancias_cache)
            filtro = llenar_filtro(form.filtro3.data, form.valor3.data, filtro,
                    distancias_cache)
            baresEncontrados = buscador.buscar(filtro)
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
            colors = ["#FF0000", "#00FF00", "#0000FF",
                      "#FFFF00", "#00FFFF", "#FF00FF"]
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
        except:
            traceback.print_exc()
            return redirect(url_for("buscar") + "/True")
    return render_template('buscar.html', form = form, error = error)


@app.route('/agregar', methods=['GET', 'POST'])
@homeRedirect
@login_required
def agregar():
    form = AgregarForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            nombre_del_bar = str(form.nombre_dado.data)
            direccion_del_bar = Ubicacion(form.direccion_dada.data)
            buscador.obtenerBBDD().agregarBares([PerfilDeBar(Bar(nombre_del_bar, direccion_del_bar))])
            return render_template('agregar_resultado.html', positivo = True)
        except:
            traceback.print_exc()
            return render_template('agregar_resultado.html', positivo = False)

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

@app.route('/eliminar', methods=['GET', 'POST'])
@homeRedirect
@login_required
def eliminar():
    direccion = request.args.get('barDireccion')
    nombre = request.args.get('nombre')
    if request.method == 'POST':
        try:
            bar = buscador.obtenerBBDD().obtenerBar(direccion)
            buscador.obtenerBBDD().borrarBar(bar)
            return render_template('eliminar_resultado.html', positivo = True)
        except:
            traceback.print_exc()
            return render_template('eliminar_resultado.html', positivo = False)

    return render_template('eliminar_bar.html', direccion=direccion, nombre=nombre)

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
