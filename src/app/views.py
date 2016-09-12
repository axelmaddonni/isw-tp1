from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import Form
from flask_bcrypt import Bcrypt
from wtforms import TextField, PasswordField, BooleanField, StringField, validators
from app import app
from app.bares import Direccion, Bar, BuscadorDeBares, buscador
from app.user import User, usuarios
import math

bcrypt = Bcrypt()
login_manager = LoginManager()

class BuscarForm(Form):
    direccion_actual = StringField('Direccion')

class AgregarForm(Form):
    direccion_dada = StringField('Direccion')
    nombre_dado = StringField("Nombre")

class LoginForm(Form):
    username = TextField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

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

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    form = AgregarForm(request.form)
    if request.method == 'POST' and form.validate():
        nombre_del_bar = str(form.nombre_dado.data)
        direccion_del_bar = Direccion(form.direccion_dada.data)
        buscador.losBares.append((Bar(nombre_del_bar, direccion_del_bar)))
        return render_template('agregar_resultado.html',
                           positivo = True)

    return render_template('agregar.html', form=form)

@app.route('/home', methods=['GET', 'POST'])
def accionesPosibles():
    if request.method == 'GET':
        user = user_loader(current_user.get_id())
        return render_template('home.html', 
                            anon = (user is None) or user.is_anonymous(),
                            mod = (user is not None) and user.is_mod())

@login_manager.user_loader
def user_loader(user_id):
    return usuarios.get(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        if form.validate_on_submit():
            user = user_loader(form.username.data)
            if user:
                if user.check_password(form.password.data):
                    user.authenticated = True
                    login_user(user)
                    return redirect(url_for("accionesPosibles"))
        else:
            pass
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for("accionesPosibles"))
