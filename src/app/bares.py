from math import sqrt
import googlemaps
from datetime import datetime
import json

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

class Ubicacion:
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
  def __init__(self, nombre, ubicacion, tieneWifi = True, tieneEnchufes = True):
    self.__nombre = nombre
    self.__ubicacion = ubicacion
    self.__duenios = []
    self.__tieneWifi = tieneWifi
    self.__tieneEnchufes = tieneEnchufes
  def nombre(self):
    return self.__nombre
  def ubicacion(self):
    return self.__ubicacion
  def tieneWifi(self):
    return self.__tieneWifi
  def editarUbicacion(nuevaUbicacion):
    self.__ubicacion = nuevaUbicacion
  def agregarDuenio(nuevoDuenio):
    self.__duenios.append(nuevoDuenio)

class PerfilDeBar:
  def __init__(self, bar):
    self.elBar = bar
    self.__votos = { "Wifi": 80, "Comida": 30, "Precio": 50}
    self.__comentarios = [ 'Este bar es genial!', 'Un servicio de porqueria.' ]
  def bar(self):
    return self.elBar
  def votos(self, feature):
    return self.__votos[feature]
  def comentarios(self):
    return self.__comentarios

class BuscadorDeBares:
  def __init__(self, bbddBares):
    self.BBDDBares = bbddBares
  def obtenerBBDD(self):
    return self.BBDDBares
  def buscar(self, dir_usuario):
    direcciones = list(self.BBDDBares.direcciones())
    resultado = []
    distancias = []
    try:
      resultado = gmaps.distance_matrix(
              dir_usuario.direccion(),
              direcciones,
              units="metric",
              mode = "walking")
      distancias = [resultado["rows"][0]["elements"][i]["distance"]["value"] \
                  for i in range(len(direcciones))]
    except:
        raise RuntimeError("Fallo la busqueda en Google Maps.")
    return [(distancias[i], \
            self.BBDDBares.obtenerPerfilDeBar(direcciones[i])) \
                for i in range(len(direcciones)) if \
                    distancias[i] <= 400 and \
                    self.BBDDBares.obtenerBar(direcciones[i]).tieneWifi()]


class BaseDeDatosDeBares:
  def __init__(self, bares):
    self.losBaresPorDir = dict([(bar.bar().ubicacion().direccion(), bar) for bar in bares])
  def agregarBares(self, bares):
    for bar in bares:
      key = bar.bar().ubicacion().direccion()
      self.losBaresPorDir[key] = bar
  def borrarBar(self, bar):
    key = bar.ubicacion().direccion()
    if key in self.losBaresPorDir:
      del self.losBaresPorDir[key]
  def obtenerBar(self, direccion):
    return self.losBaresPorDir[direccion].bar()
  def obtenerPerfilDeBar(self, direccion):
    return self.losBaresPorDir[direccion]
  def direcciones(self):
    return self.losBaresPorDir.keys()
  def bares(self):
    return self.losBaresPorDir.values()

bar1 = Bar('Mumbai', Ubicacion('Honduras 5684, CABA, Argentina',), True, False)
bar2 = Bar('Niceto', Ubicacion('Av Cnel. Niceto Vega 5510, CABA, Argentina'), False, True)
bar3 = Bar('Bouquet', Ubicacion('Av Cabildo 1400, CABA, Argentina'), True, True)
bar4 = Bar('Omm Bar', Ubicacion('Honduras 5656, CABA, Argentina',), True, False)

# Ponele votaciones cualquiera.
bbddBares = BaseDeDatosDeBares([PerfilDeBar(bar1), PerfilDeBar(bar2), PerfilDeBar(bar3), PerfilDeBar(bar4)])
buscador = BuscadorDeBares(bbddBares)
