from abc import ABC, abstractmethod
from Dominio.prestamo import Prestamo

class Notificaciones(ABC):
    
    @abstractmethod
    def notificarPrestamo(self, prestamo: Prestamo) -> None: ...


    @abstractmethod
    def notificarMulta(self, prestamo: Prestamo) -> None: ...