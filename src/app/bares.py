from math import sqrt
import googlemaps
from datetime import datetime
import json
from app.filtros import *
from app.user import usuarios, Usuario

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
  #puede fallar
  def __init__(self, direccion):
    self.__direccion = direccion
    self.__latlong = (0, 0)
    result = gmaps.geocode(address = direccion)
    if (len(result) < 1):
        raise ValueError("No hubo resultados de Google Maps")
    res = result[0]['geometry']['location']
    self.__latlong = (res["lat"], res["lng"])
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
  def esDuenio(self, usuario):
    return usuario in self.__duenios
  def editarUbicacion(self, nuevaUbicacion):
    self.__ubicacion = nuevaUbicacion
  def editarNombre(self, nuevoNombre):
    self.__nombre = nuevoNombre
  def agregarDuenio(self, nuevoDuenio):
    self.__duenios.append(nuevoDuenio)

class PerfilDeBar:
  def __init__(self, bar):
    self.elBar = bar
    self.__valoraciones = [ Valoracion( { "wifi":8, "comida":10, "enchufes":3, "precio":4 }, "Este bar tiene buen morfi pero no tiene muchos enchufes. Lo recomiendo", Usuario("Goloso") ) ]
  def bar(self):
    return self.elBar
  def valoraciones(self):
    return self.__valoraciones
  def valoracionPorcentualPorFeature(self, feature):
    promedio = 0;
    for valoracion in self.__valoraciones:
      promedio = promedio + valoracion.votos(feature)
    return (promedio / len(self.__valoraciones)) * 10

class Valoracion:
  def __init__(self, votosPorFeature, comentario, usuario):
    self.__usuario = usuario
    self.__votos = votosPorFeature
    self.__comentario = comentario
  def usuario(self):
    return self.__usuario
  def votos(self, feature):
    return self.__votos[feature]
  def comentario(self):
    return self.__comentario

class ValoradorDeBares:
  def valorarBar(perfilDeBar, votos, comentario, usuario):
    nuevaValoracion = Valoracion(votos, comentario, usuario)
    perfilDeBar.valoraciones().append(nuevaValoracion)

class BuscadorDeBares:
  def __init__(self, conj):
    self.elConjunto = conj
    self.distanciasCache = { }
  def distancias_cache(self, dir_usuario):
    direcciones = list(self.elConjunto.direcciones())
    try:
        resultado = gmaps.distance_matrix(
                dir_usuario.direccion(),
                direcciones,
                units="metric",
                mode = "walking")
        self.distanciasCache = { \
                direcciones[i] :\
                resultado["rows"][0]["elements"][i]["distance"]["value"] \
                for i in range(len(direcciones))}
    except:
        self.distanciasCache ={ direcciones[i] : 0 \
                for i in range(len(direcciones))}
    return self.distanciasCache

  def buscar(self, filtro):
    direcciones = list(self.elConjunto.direcciones())

    direccionesYPerfiles = [ \
        (self.distanciasCache[direcciones[i]], \
        self.elConjunto.obtenerPerfilDeBar(direcciones[i])) \
        for i in range(len(direcciones))]

    return sorted(list(filter(lambda x: filtro.cumple(x[1]), direccionesYPerfiles)), key=lambda x: x[0])


class ConjuntoDePerfiles:
  def __init__(self, bares):
    self.losBaresPorDir = dict([(bar.bar().ubicacion().direccion(), bar) for bar in bares])
  def agregarBares(self, bar):
    key = bar.ubicacion().direccion()
    if key not in self.losBaresPorDir:
        self.losBaresPorDir[key] = PerfilDeBar(bar)
    else:
        raise KeyError("Ya existe esa direccion")
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
  def modificarDirBar(self, direccionVieja, direccionNueva):
    if len(direccionNueva) != 0:
      bar = self.obtenerBar(direccionVieja)
      self.losBaresPorDir[direccionNueva] = self.losBaresPorDir.pop(direccionVieja)
      bar.editarUbicacion(Ubicacion(direccionNueva))
  def modificarNombreBar(self, direccion, nombreNuevo):
    if len(nombreNuevo) != 0:
      bar = self.obtenerBar(direccion)
      bar.editarNombre(nombreNuevo)

bar1 = Bar('Mumbai', Ubicacion('Honduras 5684, CABA, Argentina',), True, False)
bar2 = Bar('Niceto', Ubicacion('Av Cnel. Niceto Vega 5510, CABA, Argentina'), False, True)
bar3 = Bar('Bouquet', Ubicacion('Av Cabildo 1400, CABA, Argentina'), True, True)
bar4 = Bar('Omm Bar', Ubicacion('Honduras 5656, CABA, Argentina',), True, False)

bar1.agregarDuenio(usuarios["Pedro"])

# Ponele votaciones cualquiera.

conjuntoDePerfiles = ConjuntoDePerfiles([PerfilDeBar(bar1), PerfilDeBar(bar2), PerfilDeBar(bar3), PerfilDeBar(bar4)])
buscador = BuscadorDeBares(conjuntoDePerfiles)
