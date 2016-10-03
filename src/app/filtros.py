class FiltroVacio:
    def cumple(self, perfilDeBar):
        return True


class FiltroExtra:
    def __init__(self, elFiltro):
        self.elFiltro = elFiltro

class FiltroDeDistancia(FiltroExtra):
    def __init__(self, elFiltro, distancia, direccionUsuario, dCache):
        FiltroExtra.__init__(self, elFiltro)
        self.distancia = distancia
        self.distanciasCache = dCache

    def cumple(self, bar):
        try:
            return (self.distanciasCache[bar.bar().ubicacion().direccion()] \
                    < self.distancia) and \
                    (self.elFiltro.cumple(bar))
        except:
            return False

class FiltroDeEnchufes(FiltroExtra):
    def __init__(self, elFiltro, minimo):
        FiltroExtra.__init__(self, elFiltro)
        self.minimo = minimo
    def cumple(self, bar):
        return bar.votos("Enchufes") >= self.minimo and \
               self.elFiltro.cumple(bar)


class FiltroDeWifi(FiltroExtra):
    def __init__(self, elFiltro, minimo):
        FiltroExtra.__init__(self, elFiltro)
        self.minimo = minimo
    def cumple(self, bar):
        return bar.votos("Wifi") >= self.minimo and self.elFiltro.cumple(bar)

class FiltroDeComida(FiltroExtra):
    def __init__(self, elFiltro, minimo):
        FiltroExtra.__init__(self, elFiltro)
        self.minimo = minimo
    def cumple(self, bar):
        return bar.votos("Comida") >= self.minimo and self.elFiltro.cumple(bar)

class FiltroDePrecio(FiltroExtra):
    def __init__(self, elFiltro, minimo):
        FiltroExtra.__init__(self, elFiltro)
        self.minimo = minimo
    def cumple(self, bar):
        return bar.votos("Precio") >= self.minimo and self.elFiltro.cumple(bar)


