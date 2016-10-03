import flask_login

class User:
    authenticated = False
    __isMod = False

    def __init__(self, username = None, password = None):
        self.__username = username
        self.__password = password
        if (username is None or password is None):
            print("True")
            self.__anon = True
        else:
            self.__anon = False

    def is_active(self):
        return True

    def get_id(self):
        return self.__username

    def is_authenticated(self):
        return self.__authenticated

    def is_anonymous(self):
        return self.__anon

    def check_password(self, otraPass):
        return self.__password == otraPass

    def modear(self):
        self.__isMod = True

    def is_mod(self):
        return self.__isMod

usuarios = {"Darien": User("Darien", "m5"), "Diamondprox": User("Diamondprox", "m5"), "Admin": User("Admin", "Admin"), "User": User("User", "User"), "Pedro": User("Pedro","1234")}
usuarios["Diamondprox"].modear()
usuarios["Admin"].modear()
