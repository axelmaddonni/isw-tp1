from functools import wraps
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import Form
from flask_bcrypt import Bcrypt
from wtforms import TextField, PasswordField, BooleanField, IntegerField, StringField, SelectField, validators, ValidationError
from app import app
from app.bares import Ubicacion, Bar, BuscadorDeBares, buscador, PerfilDeBar, gmaps ,conjuntoDePerfiles, Valoracion, ValoradorDeBares
from app.filtros import *
from app.visualizador import *
from app.user import usuarios, Usuario, Renderer
import math

import traceback

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.anonymous_user = Usuario


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

class VistaDeBarForm(Form):
    direccion_data = StringField('Direccion')

class AgregarForm(Form):
    direccion_dada = StringField('Direccion')
    nombre_dado = StringField("Nombre")

class EditarForm(Form):
    nombre_dado = StringField("Nombre", [validators.required()])

class LoginForm(Form):
    username = TextField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

class RegistrarForm(Form):
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


# Probar con "Fitz Roy 1477, CABA, Argentina"
@app.route("/buscar/<error>", methods=['GET', 'POST'])
@app.route('/buscar', methods=['GET', 'POST'])
@homeRedirect
def buscar(error = False):
    form = BuscarForm(request.form)
    if request.method == 'POST' and form.validate():
        print('direccion_actual.data = ', form.direccion_actual.data)
        try:
            user = user_loader(current_user.get_id())
            visualizador = VisualizadorDeResultados(form, user)
            baresEncontrados, posicionDelUsuario, markers, polylines, misBares = visualizador.visualizar()
            return user.accept(Renderer())('resultados_busqueda.html',
                                           bares=baresEncontrados,
                                           dirusuario=posicionDelUsuario,
                                           markers=markers,
                                           polylines=polylines,
                                           misBares = misBares,
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
            conjuntoDePerfiles.agregarBares([Bar(nombre_del_bar, direccion_del_bar)])
            return render_template('agregar_resultado.html', positivo = True)
        except:
            traceback.print_exc()
            print("Estoy en agregar")
            return render_template('agregar_resultado.html', positivo = False)

    user = user_loader(current_user.get_id())
    return user.accept(Renderer())("agregar.html", form = form)


@app.route('/vista', methods=['GET', 'POST'])
@homeRedirect
def vista():
    barDireccion = request.args.get('barDireccion')
    posicionDelUsuario = Ubicacion(request.args.get('usuarioDireccion'))
    form = VistaDeBarForm(request.form)
    perfilDeBar = conjuntoDePerfiles.obtenerPerfilDeBar(barDireccion)
    user = user_loader(current_user.get_id())

    # Lo que viene a continuac
    markers = []
    # Marker del usuario
    marker_posicion_usuario = {}
    marker_posicion_usuario['lat'] = posicionDelUsuario.latlong()[0]
    marker_posicion_usuario['lng'] = posicionDelUsuario.latlong()[1]
    marker_posicion_usuario['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
    marker_posicion_usuario['infobox'] = 'Tu Ubicacion'
    markers.append(marker_posicion_usuario)

    # Marker del bar
    marker_posicion_bar = {}
    marker_posicion_bar['lat'] = perfilDeBar.bar().ubicacion().latlong()[0]
    marker_posicion_bar['lng'] = perfilDeBar.bar().ubicacion().latlong()[1]
    marker_posicion_bar['infobox'] = perfilDeBar.bar().nombre()
    markers.append(marker_posicion_bar)

    # Polyline
    latlng_usuario = dict(zip(('lat', 'lng'), posicionDelUsuario.latlong()))
    latlng_bar = dict(zip(('lat', 'lng'), perfilDeBar.bar().ubicacion().latlong()))

    legs = gmaps.directions(latlng_usuario, latlng_bar, mode='walking', units='metric')[0]['legs']

    polyline = {'stroke_color': "#FF0000",
                'stroke_opacity': 0.8,
                'stroke_weight': 4,
                'path': []}

    # Construimos el path del polyline
    for i in range(len(legs)):
        steps = legs[i]['steps'];
        for j in range(len(steps)):
            encodedPoints = steps[j]['polyline']['points']
            for lat, lng in pline.decode(encodedPoints):
                polyline['path'].append({'lat': lat, 'lng': lng})

    return user.accept(Renderer())('vista_de_bar.html', 
                                    form=form, 
                                    perfilDeBar=perfilDeBar,
                                    posicionDelUsuario=posicionDelUsuario,
                                    markers=markers,
                                    polyline=polyline, 
                                    usuarioDireccion=posicionDelUsuario.direccion())

@app.route('/editar', methods=['GET', 'POST'])
@homeRedirect
@login_required
def editar():
    direccion = request.args.get('barDireccion')
    form = EditarForm(request.form)
    if request.method == 'POST' and form.validate():

        conjuntoDePerfiles.modificarNombreBar(direccion,
                str(form.nombre_dado.data))
        return render_template('editar_resultado.html',
                           positivo = True)
    user = user_loader(current_user.get_id())
    esDuenio = conjuntoDePerfiles.obtenerBar(direccion).esDuenio(user)
    return user.accept(Renderer())('editar_bar.html', esDuenio=esDuenio, form=form, direccion=direccion, nombre=conjuntoDePerfiles.obtenerBar(direccion).nombre())


@app.route('/valorarBar', methods=['POST'])
@homeRedirect
def valorarBar():
    direccionBar = request.form['direccionBar']
    direccionUsuario = request.form['direccionUsuario']
    perfilDeBar = conjuntoDePerfiles.obtenerPerfilDeBar(direccionBar)
    votosPorFeature = {}
    for feature in ['wifi', 'enchufes', 'comida', 'precio']:
        voto = { feature: int(request.form[feature]) }
        votosPorFeature.update(voto)
    comentario = request.form['textoNuevoComentario']
    user = user_loader(current_user.get_id())
    nuevaValoracion = Valoracion (votosPorFeature, comentario, user)
    ValoradorDeBares.valorarBar(perfilDeBar, votosPorFeature, comentario, user)
    form = VistaDeBarForm(request.form)
    return redirect(url_for('vista')  + "?barDireccion=" + direccionBar + "&usuarioDireccion=" + direccionUsuario)

@app.route('/eliminar', methods=['GET', 'POST'])
@homeRedirect
@login_required
def eliminar():
    direccion = request.args.get('barDireccion')
    nombre = request.args.get('nombre')
    if request.method == 'POST':
        try:
            bar = conjuntoDePerfiles.obtenerBar(direccion)
            conjuntoDePerfiles.borrarBar(bar)
            return render_template('eliminar_resultado.html', positivo = True)
        except:
            traceback.print_exc()
            return render_template('eliminar_resultado.html', positivo = False)

    user = user_loader(current_user.get_id())
    esDuenio = conjuntoDePerfiles.obtenerBar(direccion).esDuenio(user)

    return user.accept(Renderer())('eliminar_bar.html', esDuenio=esDuenio, direccion=direccion, nombre=nombre)
    

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@homeRedirect
def accionesPosibles():
    if request.method == 'GET':
        user = user_loader(current_user.get_id())
        return user.accept(Renderer())("home.html")


@login_manager.user_loader
def user_loader(user_id):
    return usuarios[user_id]


@app.route("/login/<invalidCredentials>", methods=['GET', 'POST'])
@app.route("/login", methods=["GET", "POST"])
@homeRedirect
def login(invalidCredentials = False):
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        try:
            if not usuarios.autenticar(username, form.password.data):
                raise ValueError("Invalid Password")
            login_user(usuarios[username])
            return redirect(url_for("accionesPosibles"))
        except:
            traceback.print_exc()
            return redirect(url_for("login") + "/True")
    return render_template("login.html", form=form, invalidCredentials = invalidCredentials)


@app.route("/logout", methods=["GET"])
@homeRedirect
@login_required
def logout():
    usuarios.desautenticar(current_user.get_id())
    logout_user()
    return redirect(url_for("accionesPosibles"))

@app.route("/registrar/<invalidCredentials>", methods=['GET', 'POST'])
@app.route('/registrar', methods=['GET', 'POST'])
@homeRedirect
def registrar(invalidCredentials = False):
    form = RegistrarForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        try:
            usuarios[username] = form.password.data
            usuarios.autenticar(username, form.password.data)
            login_user(usuarios[username])
            return usuarios[username].accept(Renderer())("registrar_resultado.html", positivo = True)
        except:
            traceback.print_exc()
            return redirect(url_for("registrar") + "/True")

    user = user_loader(current_user.get_id())
    return user.accept(Renderer())("registrar.html", form = form, invalidCredentials = invalidCredentials)
