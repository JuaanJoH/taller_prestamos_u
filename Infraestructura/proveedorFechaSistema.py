from datetime import date
from Aplicacion.Puertos.proveedorFecha import ProveedorFecha

class ProveedorFechaSistema(ProveedorFecha):
    
    def hoy(self) -> date:
        return date.today()