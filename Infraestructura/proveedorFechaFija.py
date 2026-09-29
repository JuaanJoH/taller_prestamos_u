from datetime import date
from Aplicacion.Puertos.proveedorFecha import ProveedorFecha

class ProveedorFechaFija(ProveedorFecha):
    def __init__(self, fecha: date):
        self._fecha = fecha

    def hoy(self) -> date:
        return self._fecha