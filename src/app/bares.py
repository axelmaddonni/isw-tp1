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
  def __init__(self, nombre, ubicacion):
    self.__nombre = nombre
    self.__ubicacion = ubicacion
    self.__duenios = []
  def nombre(self):
    return self.__nombre
  def ubicacion(self):
    return self.__ubicacion
  def editarUbicacion(nuevaUbicacion):
    self.__ubicacion = nuevaUbicacion
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
    self.BBDDBares = BaseDeDatosDeBares(bares)
  def agregarALaBBDD(self, bares):
    self.BBDDBares.agregarBares(bares)
  def removerDeLaBBDD(self, bar):
    self.BBDDBares.borrarBar(bar)
  def buscar(self, dir_usuario):
    direccionesDeLosBares = list(self.BBDDBares.direcciones())
    losBares = list(self.BBDDBares.bares())
    try:
      resultado = gmaps.distance_matrix(dir_usuario.direccion(), direccionesDeLosBares, units="metric", mode = "walking")
      return [PerfilDeBar(losBares[i]) for i in range(len(losBares)) if resultado["rows"][0]["elements"][i]["distance"]["value"] <= 400]
    except:
      pass


class BaseDeDatosDeBares:
  def __init__(self, bares):
    self.losBaresPorDir = dict([(bar.ubicacion().direccion(), bar) for bar in bares])
  def agregarBares(self, bares):
    for bar in bares:
      key = bar.ubicacion().direccion()
      self.losBaresPorDir[key] = bar   
  def borrarBar(self, bar):
    key = bar.ubicacion().direccion()
    if key in self.losBaresPorDir:
      del self.losBaresPorDir[key]
  def direcciones(self):
    return self.losBaresPorDir.keys()
  def bares(self):
    return self.losBaresPorDir.values()

bar1 = Bar('Mumbai', Ubicacion('Honduras 5684, CABA, Argentina'))
bar2 = Bar('Niceto', Ubicacion('Av Cnel. Niceto Vega 5510, CABA, Argentina'))
bar3 = Bar('Bouquet', Ubicacion('Av Cabildo 1400, CABA, Argentina'))
buscador = BuscadorDeBares([bar1, bar2])
buscador.agregarALaBBDD([bar3])


def hacerDictDeBares(perfiles):
  res = {}
  for perfil in perfiles:
    res[perfil.bar().nombre()] = [perfil.bar().ubicacion().direccion()]
  return json.dumps(res)