from math import sqrt
import googlemaps
from datetime import datetime

# Como usar: https://developers.google.com/maps/web-services/?hl=es
# Mas: https://github.com/googlemaps/google-maps-services-python
# Por favor no distribuir ni usar para otra cosa esta clave, porque es mia y
# su uso indiscriminado puede hacer que no pueda usar mas la api de gmaps :(
# max de requests por dia: 5000
# Si algo les da error que no anda, avisenme.
# Para sacar una clave para lo que quieran:
#    https://console.developers.google.com/?hl=es-419
GOOGLE_MAPS_KEY = "AIzaSyBN8fuLr8PXqvxNrZ_WtcIhqo9K5XKqWDw"
gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)

class Direccion:
    global gmaps
    def __init__(self, direccion):
        self.__direccion = direccion
        self.__latlong = (0, 0)
        try:
            result = gmaps.geocode(direccion)
            res = result[0]['geometry']['location']
            self.__latlong = (res["lat"], res["lng"])
        except:
            pass
    def direccion(self):
        return self.__direccion
    def latlong(self):
        return self.__latlong
        return distancia

class Bar:
    def __init__(self, nombre, direccion):
        self.__nombre = nombre
        self.__direccion = direccion
        self.__duenios = []
    def nombre(self):
        return self.__nombre
    def direccion(self):
        return self.__direccion
    def editarDireccion(nuevaDireccion):
        self.__direccion = nuevaDireccion
    def agregarDuenio(nuevoDuenio):
        self.__duenios.append(nuevoDuenio)

class PerfilDeBar:
    def __init__(self, bar):
        self.elBar = bar
        self.votos = {}
        self.comentarios = []
    def bar(self):
        return self.elBar

class BuscadorDeBares:
    def __init__(self, bares):
        self.losBares = bares
    def buscar(self, dir_usuario):
        direccionesDeLosBares = [bar.direccion().direccion() for bar in self.losBares]
        try:
            resultado = gmaps.distance_matrix(dir_usuario.direccion(), direccionesDeLosBares, units="metric", mode = "walking")
            return [PerfilDeBar(self.losBares[i]) for i in range(len(self.losBares)) if resultado["rows"][0]["elements"][i]["distance"]["value"] <= 400]
        except:
            pass


bar1 = Bar('Mumbai', Direccion('Honduras 5684, CABA, Argentina'))
bar2 = Bar('Niceto', Direccion('Av Cnel. Niceto Vega 5510, CABA, Argentina'))
buscador = BuscadorDeBares([bar1, bar2])
