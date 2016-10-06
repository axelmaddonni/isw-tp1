from app.bares import Ubicacion, Bar, BuscadorDeBares, buscador, PerfilDeBar, gmaps
from app.filtros import *
import polyline as pline

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

class VisualizadorDeResultados:
    def __init__(self, form, current_user):
        self.current_user = current_user
        self.filtro = FiltroVacio()
        self.posicionDelUsuario = Ubicacion(form.direccion_actual.data)
        distancias_cache = buscador.distancias_cache(self.posicionDelUsuario)
        self.filtro = llenar_filtro(form.filtro1.data,
                form.valor1.data, self.filtro,
                distancias_cache)
        self.filtro = llenar_filtro(form.filtro2.data,
                form.valor2.data, self.filtro,
                distancias_cache)
        self.filtro = llenar_filtro(form.filtro3.data,
                form.valor3.data, self.filtro,
                distancias_cache)
    def visualizar(self):
        baresEncontrados = buscador.buscar(self.filtro)
        user = self.current_user
        markers = []
        misBares = []
        for bar in baresEncontrados:
            marker = {}
            marker['lat'] = bar[1].bar().ubicacion().latlong()[0]
            marker['lng'] = bar[1].bar().ubicacion().latlong()[1]
            marker['infobox'] = bar[1].bar().nombre()
            markers.append(marker)
            if bar[1].bar().esDuenio(user):
                misBares.append(bar[1].bar().ubicacion().direccion())
        marker_posicion_usuario = {}
        marker_posicion_usuario['lat'] = self.posicionDelUsuario.latlong()[0]
        marker_posicion_usuario['lng'] = self.posicionDelUsuario.latlong()[1]
        marker_posicion_usuario['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        marker_posicion_usuario['infobox'] = 'Tu Ubicacion'
        markers.append(marker_posicion_usuario)

        latlng_usuario = {'lat': self.posicionDelUsuario.latlong()[0],
                          'lng': self.posicionDelUsuario.latlong()[1]
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
        return baresEncontrados, self.posicionDelUsuario, markers, polylines, misBares
