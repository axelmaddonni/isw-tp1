import flask_login
from flask import render_template
from contextlib import suppress 
from collections import defaultdict
from functools import partial

class Usuario:

    privilegios = None

    def __init__(self, username = None):
        if (username is None):
            self.privilegios = UsuarioNoRegistrado()
        else:
            self.privilegios = UsuarioRegistrado(username)

    def get_id(self):
        return self.privilegios.get_id()

    def is_anonymous(self):
        return self.privilegios.is_anonymous()

    def is_authenticated(self):
        return self.privilegios.is_authenticated()

    def accept(self, visitor):
        return self.privilegios.accept(visitor)

    def is_active(self):
        return self.is_authenticated()

    def atributos(self):
        return self.privilegios.atributos()

class Privilegio:

    atr = None

    def get_id(self):
        return None

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return False

    def is_active(self):
        return self.is_authenticated()

    def atributos(self):
        return self.atr

    def accept(self, visitor):
        pass

class UsuarioNoRegistrado (Privilegio):

    def __init__(self):
        pass

    def accept(self, visitor):
        return visitor.renderNoRegistrado()

class UsuarioRegistrado (Privilegio):

    def __init__(self, username):
        self.atr = atributos(username)

    def get_id(self):
        return self.atr.username

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return usuarios.is_authenticated(self.atr.username)

    def accept(self, visitor):
        return visitor.renderRegistrado()

class Mod (Privilegio):

    atr = None

    def __init__(self, user):
        self.atr = user.atributos()

    def get_id(self):
        return self.atr.username

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return usuarios.is_authenticated(self.atr.username)

    def accept(self, visitor):
        return visitor.renderMod()

class atributos:

    username = None

    def __init__(self, username):
        self.username = username

class BaseDeDatosDeUsuarios:
    usuarios = {}
    auth = defaultdict(lambda: False)
    passwords = {}

    def __init__(self, usuarios = {}):
        for username, passWord in usuarios.items():
            self[username] = passWord

    def __delitem__(self, username):
        with suppress(KeyError):
            del self.usuarios[username]
            self.auth[username] = False

    def __getitem__(self, username):
        try:
            return self.usuarios[username]
        except KeyError:
            return Usuario()

    def __setitem__(self, username, passWord):
        if self.usuarios.get(username) is None:
            self.usuarios[username] = Usuario(username)
            self.passwords[username] = passWord
        else:
            raise KeyError("El usuario ya existe")
    
    def is_authenticated(self, username):
        return self.auth[username]

    def modear(self, username):
        try:
            usuarioAModear = self.usuarios[username]
            usuarioAModear.privilegios = Mod(usuarioAModear)
        except:
            raise KeyError("El usuario no existe")

    def autenticar(self, username, passWord):
        if username in self.usuarios:
            if self.passwords[username] == passWord:
                self.auth[username] = True
                return True
            else: 
                return False
        else:
            raise KeyError("El usuario no existe")

    def desautenticar(self, username):
        if username in self.usuarios:
            self.auth[username] = False
        else:
            raise KeyError("El usuario no existe")

#visitor
class Renderer:

    def __init__(self):
        pass

    def renderNoRegistrado(self):
        return partial(render_template, anon = True, mod = False)

    def renderRegistrado(self):
        return partial(render_template, anon = False, mod = False)

    def renderMod(self):
        return partial(render_template, anon = False, mod = True)

usuarios = BaseDeDatosDeUsuarios({"User": "User", "Mod": "Mod","Pedro": "Pedro"})
usuarios.modear("Mod")

if __name__ == "__main__":
    usuarios.modear("Mod")
    assert(type(usuarios["User"].privilegios == UsuarioRegistrado))
    assert(type(usuarios["Mod" ].privilegios == Mod))
    assert(usuarios["Mod" ].get_id() == "Mod")
    assert(usuarios["User" ].get_id() == "User")
    assert(usuarios["NoExiste"].is_authenticated() == False)
    assert(usuarios["NoExiste"].is_anonymous() == True)
    assert(usuarios[None].is_anonymous() == True)
    assert(usuarios[None].is_authenticated() == False)
    del usuarios["User"]
    assert(not usuarios["User" ].get_id() == "User")
    usuarios["User"] = "UserPass"
    assert(usuarios["User" ].get_id() == "User")
